import glob
import os
import re
import shutil
import subprocess
import tempfile
import time
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import List, Optional

import click
import gitlab
from git import Repo
from ogr import get_instances_from_dict, GitlabService
from ogr.abstract import PullRequest
from ogr.services.gitlab import GitlabProject
from yaml import safe_load

from figitool.exception import FigitoolException

FIGITOOL_CONFIG_FILE = "~/.figitool.yaml"


@dataclass
class Student:
    name: str
    uco: str


class FiGiTool(object):
    def __init__(self, subject, name=None):
        self.subject = subject
        self.name = name

    @property
    @lru_cache()
    def config(self) -> dict:
        config_file = Path(FIGITOOL_CONFIG_FILE).expanduser()
        if not config_file.exists():
            raise FileExistsError(f"Config file does not exists: {config_file}")

        with config_file.open() as config_file_obj:
            content = safe_load(config_file_obj)

        return content

    @property
    def service(self) -> GitlabService:
        services = get_instances_from_dict(instances=self.config["authentication"])
        if not services:
            raise Exception("Please, set the authentication in the config file.")
        if len(services) != 1:
            raise Exception(
                "Please, user only one authentication entry in you config file."
            )
        return list(services)[0]

    @property
    @lru_cache()
    def username(self):
        return self.service.user.get_username()

    @property
    @lru_cache()
    def repo(self):
        return Repo(path=".")

    @property
    def namespace(self) -> Optional[str]:
        return self.config["namespace"] if "namespace" in self.config else None

    def delete_branch(self, uco):
        branch_name = "{}-{}".format(self.name, uco)

        try:
            branch = self.repo.branches[branch_name]
        except:
            click.echo("X> {} (not present)".format(branch_name))
            return

        click.echo("X> {}".format(branch_name))
        self.repo.delete_head(branch, force=True)

    def get_gitlab_project(self, student: Student) -> GitlabProject:
        repo_name_format = self.config.get("repo-name-format", "{subject}-{uco}")
        repo_name = repo_name_format.format(
            subject=self.subject, uco=student.uco, student=student.name
        )
        return self.service.get_project(
            repo=repo_name, namespace=self.namespace or self.username
        )

    def get_prs(self, student: Student) -> List[PullRequest]:
        gitlab_repo = self.get_gitlab_project(student=student)
        return gitlab_repo.get_pr_list()

    def get_pr_title(self, student: Student):
        pr_title_format = self.config.get("pr-title-format", "{name} {student} ({uco})")
        pr_title = pr_title_format.format(
            subject=self.subject,
            name=self.name.upper(),
            uco=student.uco,
            student=student.name,
        )
        return pr_title

    def get_pr(self, student: Student):
        mrs = self.get_prs(student=student)
        title = self.get_pr_title(student=student)

        for mr in mrs:
            if mr.title == title:
                return mr
        return None

    @staticmethod
    def read_students(file, start_with=0, use_filter=None):
        students = []

        start = 1 + start_with
        for row in file.readlines()[start:]:
            uco_raw, name_raw = row.split(";")[1:3]
            uco = str(uco_raw)
            name = " ".join(reversed(name_raw[1:-1].split(", ")))
            if (
                use_filter
                and use_filter not in name.lower()
                and use_filter not in uco.lower()
            ):
                continue
            students.append(Student(name=name, uco=uco))

        return students

    @staticmethod
    def get_students(file=None, start_with=0, use_filter=None):
        if file:
            return FiGiTool.read_students(file)

        if not Path("seznam_export.csv").exists():
            raise FigitoolException(
                "You need to set a csv file with the info about students."
                " The default location is  `seznam_export.csv`."
            )

        with open(file="seznam_export.csv") as default_file:
            return FiGiTool.read_students(
                file=default_file, start_with=start_with, use_filter=use_filter
            )

    def checkout_master(self):
        self.repo.heads.master.checkout()

    def copy_and_add_solution(self, file_with_solution: Path, new_name: str = None):
        new_name = new_name or file_with_solution.name
        new_solution = str(Path.cwd() / new_name)
        shutil.copy(str(file_with_solution), new_solution)
        subprocess.check_call(["git", "add", new_solution])

    def create_and_checkout_new_branch(self, uco):
        new_branch = self.create_students_branch(uco)

        # click.echo("-> {}".format(new_branch))

        temp_dir = tempfile.mkdtemp()
        files = glob.glob(f"./{uco}*")
        for f in files:
            shutil.move(f, os.path.join(temp_dir, f))
        new_branch.checkout()
        for f in files:
            shutil.move(os.path.join(temp_dir, f), f)
        shutil.rmtree(temp_dir)

        return bool(files)

    def create_students_branch(self, uco):
        branch_name = "{}-{}".format(self.name, uco)
        try:
            new_branch = self.repo.branches[branch_name]
        except:
            # click.echo("* {}".format(branch_name))
            new_branch = self.repo.create_head(branch_name)
        return new_branch

    def git_add_student_files(self, student: Student, rename_if_one=True):
        """
        student_files = glob.glob('./{}*'.format(uco))
        click.echo("+ {}".format(student_files))
        repo.index.add(student_files)
        """
        student_files = glob.glob(f"./{student.uco}*")
        if not student_files:
            return False

        if rename_if_one and len(student_files) == 1:
            old_name = student_files[0]
            filename, file_extension = os.path.splitext(old_name)
            student_convert = (
                student.name.lower()
                .replace(" ", "_")
                .encode("ascii", errors="ignore")
                .decode()
            )
            new_name = f"{student_convert}{file_extension}"
            click.echo(f"Rename: {old_name} -> {new_name}")
            shutil.move(old_name, new_name)
            student_files = [new_name]

        try:
            cmd = ["git", "add"] + student_files
            click.echo(f"cmd: {cmd}")
            subprocess.check_call(cmd)
            self.repo.index.update()
            return True

        except Exception as ex:
            return False

    def create_remote(self, student: "Student"):
        remote_name = "fi-{}".format(student.uco)
        if remote_name in [r.name for r in self.repo.remotes]:
            return (
                f"{remote_name} (present)",
                list(self.repo.remote(name=remote_name).urls)[0],
            )

        students_project = self.get_gitlab_project(student=student)
        remote_url = students_project.get_git_urls()["ssh"]
        remote = self.repo.create_remote(remote_name, remote_url)
        return remote, remote_url

    def get_mrs_link(self, uco):
        result = (
            "https://gitlab.fi.muni.cz/xlachma1/ib111-{uco}/"
            "merge_requests/".format(uco=uco)
        )
        return result

    def create_merge_request(self, student: "Student", description) -> PullRequest:
        mr = self.get_pr(student=student)
        if mr:
            return mr

        repo = self.get_gitlab_project(student=student)

        mr = repo.pr_create(
            title=self.get_pr_title(student=student),
            source_branch=f"{self.name}-{student.uco}",
            target_branch="master",
            body=description,
        )
        return mr

    def get_students_solution(self, list_txt, student: "Student", name):
        with open(list_txt) as list_file:
            for line in list_file.readlines():
                if student.name in line:
                    line_split = line.split(" ")
                    xname, last_solution = line_split[0], line_split[4].strip()
                    break
            else:
                return None, None

        return (
            Path(list_txt).parent / f"{xname}_{last_solution}" / f"{name}.py",
            last_solution,
        )

    def get_students_xname(self, list_txt, student) -> Optional[str]:
        with open(list_txt) as list_file:
            for line in list_file.readlines():
                if student.name in line:
                    line_split = line.split(" ")
                    return line_split[0]

        return None

    def git_commit(self, student: "Student", solution: str = None):
        if solution:
            msg = f"Add solution {solution} for {self.name} by student {student.name} ({student.uco})"
        else:
            msg = f"Update solution"
        # click.echo("! {}".format(msg))
        self.repo.index.commit(msg)

    def git_push(self, student):
        try:
            remote = self.repo.remotes["fi-{}".format(student.uco)]
        except:
            remote = self.create_remote(student=student)

        for push_info in remote.push(force=True):
            click.echo(push_info.summary)

    def get_points(self, mr, point_identifier="Body", sum_only=False, get_max=True):
        points = []
        points_max = 0
        if get_max:
            pattern = re.compile(f"# {point_identifier}: (\d+(\.\d*)?)/(\d+)")
        else:
            pattern = re.compile(f"# {point_identifier}: (\d+(\.\d*)?)")

        for note in mr.notes.list():
            if note.author["username"] != self.username.username:
                # Note from someone else.
                continue

            if note.type != "DiffNote":
                continue

            for match in re.findall(pattern, note.body):
                points.append(match[0])
                if get_max:
                    points_max += float(match[2])
            else:
                # print(f"no points:\n{note.body}")
                pass

        starred_points = [f"*{i}" for i in points]

        points_sum = sum([float(i) for i in points])
        if sum_only:
            return str(points_sum)

        result = "+".join(starred_points) + f"={points_sum}"
        if get_max:
            result += f" /{points_max}"
        return result

    def get_line_project(self, student: Student):
        try:
            project = self.get_gitlab_project(student=student)
            return student.name, project.full_repo_name, project.get_web_url()

        except gitlab.GitlabGetError:
            return student.name, "no project", "?"

    def get_line_create_project(self, student: "Student", course):
        name_of_the_newly_crated_project = f"{course.subject}-{student.uco}"
        try:
            project = self.service.project_create(
                repo=name_of_the_newly_crated_project, namespace=self.namespace
            )
            return student.name, project.full_repo_name
        except gitlab.GitlabError as ex:
            return student.name, f"Cannot create project: {ex}"

    def get_line_add_maintainer(self, student: "Student", ids_to_add):
        try:
            project = self.get_gitlab_project(student=student)
        except gitlab.GitlabGetError:
            return student.name, "no project"

        try:
            for user_id in ids_to_add:
                project.gitlab_repo.members.create(
                    {"user_id": user_id, "access_level": gitlab.MAINTAINER_ACCESS}
                )
            return student.name, f"added ({len(ids_to_add)})"
        except gitlab.GitlabError as ex:
            return student.name, str(ex)

    def get_line_add_student(self, student: "Student", list_txt):
        try:
            project = self.get_gitlab_project(student=student)
        except gitlab.GitlabGetError:
            return student.name, "no project"

        xname = self.get_students_xname(list_txt=list_txt, student=student)

        try:
            found_users = self.service.gitlab_instance.users.list(username=xname)
            if not found_users:
                return student.name, "user not found"
            id_to_add = found_users[0].id
            try:
                project.gitlab_repo.members.create(
                    {"user_id": id_to_add, "access_level": gitlab.REPORTER_ACCESS}
                )
                return student.name, f"added ({xname}, {id_to_add})"
            except:
                member = project.gitlab_repo.members.get(id_to_add)
                member.access_level = gitlab.REPORTER_ACCESS
                member.save()
                return student.name, f"updated ({xname}, {id_to_add})"
        except gitlab.GitlabError as ex:
            return student.name, str(ex)

    def get_line_export(self, student: "Student", path):
        try:
            project = self.get_gitlab_project(student=student)
            export = project.gitlab_repo.exports.create({})

            # Wait for the 'finished' status
            export.refresh()
            while export.export_status != "finished":
                time.sleep(1)
                export.refresh()

            # Download the result
            archive_path = Path(path) / f"{student.uco}.tgz"
            with open(archive_path, "wb") as f:
                export.download(streamed=True, action=f.write)

            return student.name, archive_path
        except gitlab.GitlabGetError:
            return student.name, "no project"

    def get_line_project_delete(self, student):
        try:
            project = self.get_gitlab_project(student=student)
            project.gitlab_repo.delete()
            return student.name, "deleted"
        except gitlab.GitlabGetError:
            return student.name, "no project"

    def get_line_add_remote(self, student: "Student"):
        remote, remote_url = self.create_remote(student=student)
        return student.name, remote, remote_url

    def get_line_task_delete(self, student: "Student"):
        self.delete_branch(student.uco)
        return student.name, "removed"

    def get_line_mrs(
        self,
        student: "Student",
        correction: bool,
        diffs: bool,
        show_link: bool,
        show_assignee: bool,
        assignee: str,
        open_link: str,
        mark: bool,
        is_msg: bool,
    ):
        try:
            mr = self.get_pr(student=student)
        except gitlab.GitlabGetError:
            return student.name, "project not found"

        if not mr:
            return student.name, "merge-request not found"

        link = mr.url

        if diffs:
            link += "/diffs#diffs"

        table_line = [mr.title]
        if show_link:
            table_line.append(link)

        if assignee or show_assignee:
            project = self.get_gitlab_project(student=student)
            mr_gitlab = project.gitlab_repo.mergerequests.get(mr.id)

            mr_assignee = mr_gitlab.assignee["name"] if mr_gitlab.assignee else None
            if assignee and (not mr_assignee or assignee not in mr_assignee):
                return None
            if show_assignee:
                table_line.append(mr_assignee if mr_assignee else "-")

        if mark or is_msg:
            project = self.get_gitlab_project(student=student)
            comments = project.get_pr_comments(pr_id=mr.id, filter_regex="# Známka")

            if correction and (
                not comments or "oprava" not in comments[0].comment.lower()
            ):
                return None

            if not comments:
                table_line.append("-")
            elif is_msg:
                table_line.append(comments[0].comment)
            else:
                table_line.append(comments[0].comment[2:11])

        if open_link:
            subprocess.check_call(["firefox", link])

        return table_line

    @staticmethod
    def for_each_student(course, fce, *args, **kwargs):
        table = []
        for student in course.students_generator_progressbar:
            try:
                one_line = fce(student, *args, **kwargs)
                if one_line:
                    table.append(one_line)
            except KeyboardInterrupt:
                break
        return table


class Course:
    def __init__(
        self,
        file_with_students,
        student_filter,
        start_with,
        subject: Optional[str] = None,
    ) -> None:
        self.subject = subject or Path().cwd().name
        self._file_with_students = file_with_students
        self._student_filter = student_filter
        self._start_with = start_with

    @property
    @lru_cache()
    def students(self):
        return FiGiTool.get_students(
            file=self._file_with_students,
            use_filter=self._student_filter,
            start_with=self._start_with,
        )

    @property
    def students_generator_progressbar(self):
        with click.progressbar(
            self.students,
            item_show_func=lambda student: str(student.name if student else "-"),
        ) as students_list:
            for student_obj in students_list:
                yield student_obj


pass_course = click.make_pass_decorator(Course)
