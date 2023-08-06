#!/usr/bin/python3
import csv
import subprocess
from pathlib import Path

import click
import git
import yaml
from tabulate import tabulate

from figitool.exception import cover_figtool_exception
from figitool.utils import FiGiTool, Course, pass_course, Student, FIGITOOL_CONFIG_FILE


@click.group("figitool")
@click.option(
    "-f",
    "--filter",
    "use_filter",
    type=click.STRING,
    help="Filter -- name/uco substring",
)
@click.option("-s", "--start-with", type=click.INT, default=0)
@click.option(
    "--students-file",
    type=click.File(),
    help="csv with students (default 'seznam_export.csv')",
)
@click.option(
    "--subject",
    type=click.STRING,
    default=None,
    help="Name of the subject, defaults to the dir name. "
    "It is used for various naming like project name.",
)
@cover_figtool_exception
@click.pass_context
def figitool(ctx, use_filter, start_with, students_file, subject):
    """Tool for helping teachers to automate the code-review workflow."""
    ctx.obj = Course(
        file_with_students=students_file,
        student_filter=use_filter,
        start_with=start_with,
        subject=subject,
    )


@figitool.command()
def init():
    """Setup the environment."""
    if not Path("./.git").exists():
        if click.confirm(
            "We need to work in a git repository. Do you want to setup it now?"
        ):
            repo = git.repo.Repo.init(".")
            repo.index.commit("Initial commit")

    config_file = Path(FIGITOOL_CONFIG_FILE).expanduser()
    if not config_file.exists():
        if click.confirm(
            f"We cannot find the config file (`{FIGITOOL_CONFIG_FILE}). "
            f"Do you want to setup it now?"
        ):
            instance = click.prompt(
                "Please enter a gitlab instance url",
                type=str,
                default="https://gitlab.fi.muni.cz",
            )
            token = click.prompt(
                "Please enter a gitlab authentication token "
                "(see https://gitlab.fi.muni.cz/profile/personal_access_tokens)",
                type=str,
            )
            content = {
                "authentication": {"gitlab": {"token": token, "instance_url": instance}}
            }

            if click.confirm(
                f"Do you want to place the students' projects in the different namespace?"
            ):
                namespace = click.prompt(
                    "Please enter a gitlab namespace you want to work in "
                    "(leave empty for the user namespace)",
                    type=str,
                )
                content["namespace"] = namespace

            config_file.touch()
            yaml_content = yaml.safe_dump(content)
            click.echo(f"Created config file:\n{yaml_content}\n")
            config_file.write_text(yaml_content)


@figitool.command()
@pass_course
def check(course):
    """Print the info about config and current environment."""
    click.echo(
        tabulate([(course.subject,)], headers=["Course subject"], tablefmt="fancy_grid")
    )
    fig = FiGiTool(subject=course.subject)
    click.echo(
        tabulate(
            [
                (
                    f"Authentication:\n{fig.service}",
                    str(fig.service.user.get_username()),
                ),
                (),
            ],
            headers=["Authentication", "username"],
            tablefmt="fancy_grid",
        )
    )


@figitool.group("students")
def students():
    """Manage students of your course."""
    pass


@students.command("list")
@pass_course
def students_list(course):
    """List the students according to the csv file."""
    student_list = [(student.uco, student.name) for student in course.students]
    click.echo(tabulate(student_list, headers=("uco", "name"), tablefmt="fancy_grid"))


@figitool.group("project")
def project():
    """Manage the students' projects."""
    pass


@project.command()
@pass_course
def create(course):
    """Create a project for each student."""
    fig = FiGiTool(subject=course.subject)
    projects_table = fig.for_each_student(course, fig.get_line_create_project, course)
    click.echo(
        tabulate(projects_table, headers=("name", "project"), tablefmt="fancy_grid")
    )


@project.command("list")
@pass_course
def project_list(course):
    """List the students' projects."""
    fig = FiGiTool(subject=course.subject)
    projects_table = fig.for_each_student(course, fig.get_line_project)
    click.echo(
        tabulate(
            projects_table,
            headers=("name", "project", "web_url"),
            tablefmt="fancy_grid",
        )
    )


@project.command()
@click.argument("user", type=click.STRING)
@pass_course
def add_maintainer(course, user):
    """Add a user as a maintainer to the students' projects."""
    fig = FiGiTool(subject=course.subject)

    users_to_add = fig.service.gitlab_instance.users.list(username=user)
    ids_to_add = [usr.id for usr in users_to_add]
    project_list = fig.for_each_student(
        course, fig.get_line_add_maintainer, ids_to_add=ids_to_add
    )
    click.echo(
        tabulate(project_list, headers=("name", "member"), tablefmt="fancy_grid")
    )


@project.command()
@click.argument("list-txt", type=click.Path())
@pass_course
def add_student(course, list_txt):
    """Add student as a collaborator to his/her project."""
    fig = FiGiTool(subject=course.subject)

    project_table = fig.for_each_student(
        course, fig.get_line_add_student, list_txt=list_txt
    )
    click.echo(
        tabulate(project_table, headers=("name", "member"), tablefmt="fancy_grid")
    )


@project.command()
@click.option(
    "-p",
    "--path",
    type=click.Path(dir_okay=True, file_okay=False, writable=True),
    help="Filter -- name/uco substring",
    default=Path.cwd(),
)
@pass_course
def export(course, path):
    """Export the students' projects."""
    fig = FiGiTool(subject=course.subject)
    project_list = fig.for_each_student(course, fig.get_line_export, path=path)
    click.echo(
        tabulate(project_list, headers=("name", "export"), tablefmt="fancy_grid")
    )


@project.command()
@pass_course
def delete(course):
    """Delete the students' projects."""
    fig = FiGiTool(subject=course.subject)
    project_list = fig.for_each_student(course, fig.get_line_project_delete)
    click.echo(
        tabulate(project_list, headers=("name", "project"), tablefmt="fancy_grid")
    )


@project.command("add-remote")
@pass_course
def add_remote(course):
    """Add a remote to the students' projects."""
    fig = FiGiTool(subject=course.subject)
    table = fig.for_each_student(course, fig.get_line_add_remote)
    click.echo(
        tabulate(table, headers=("name", "remote", "remote_url"), tablefmt="fancy_grid")
    )


@figitool.group("task")
def task():
    """Manage the task(s) for the students."""
    pass


@task.command("add-using-uco")
@click.argument("name")
@pass_course
def add_using_uco(course, name):
    """Use students' uco to add the solutions."""
    fig = FiGiTool(subject=course.subject, name=name)

    output_table = []
    for student in course.students_generator_progressbar:
        fig.checkout_master()

        new_files_present = fig.create_and_checkout_new_branch(student.uco)
        if not new_files_present:
            output_table.append((student.name, "No new files"))
            continue

        files_present = fig.git_add_student_files(student.uco, student.name)
        if files_present:
            fig.git_commit(student.name, student.uco)
        else:
            output_table.append((student.name, "No files to add."))

    fig.checkout_master()
    click.echo(tabulate(output_table, headers=("uco", "file"), tablefmt="fancy_grid"))


@task.command("add-using-list")
@click.argument("name")
@click.argument("list-txt", type=click.Path())
@pass_course
def add_using_list(course, name, list_txt):
    """Use file structure from provided archive to add the solutions."""
    fig = FiGiTool(subject=course.subject, name=name)

    output_table = []
    for student in course.students_generator_progressbar:
        fig.checkout_master()
        branch = fig.create_students_branch(uco=student.uco)
        branch.checkout()
        students_file, last_solution = fig.get_students_solution(
            list_txt=list_txt, student=student, name=name
        )
        if not students_file:
            output_table.append((student.name, "Not found in the list."))
        if not students_file.exists():
            output_table.append((student.name, f"File '{students_file}` not found."))

        fig.copy_and_add_solution(file_with_solution=students_file)
        fig.git_commit(student, solution=last_solution)
        output_table.append((student.name, str(students_file)))
    fig.checkout_master()
    click.echo(tabulate(output_table, headers=("uco", "file"), tablefmt="fancy_grid"))


@task.command("add-using-xname")
@click.argument("name")
@click.argument("list-txt", type=click.Path())
@click.argument("solutions")
@pass_course
def add_using_xname(course, name, list_txt, solutions):
    """Use students' faculty login to add the solutions."""
    fig = FiGiTool(subject=course.subject, name=name)

    output_table = []
    for student in course.students_generator_progressbar:
        fig.checkout_master()
        branch = fig.create_students_branch(uco=student.uco)
        branch.checkout()

        xname = fig.get_students_xname(list_txt=list_txt, student=student)
        if not xname:
            output_table.append((student.name, "Not found in the list."))

        students_file = Path(solutions) / f"{xname}.py"
        if not students_file.exists():
            output_table.append((student.name, f"File '{students_file}` not found."))
            continue

        fig.copy_and_add_solution(
            file_with_solution=students_file, new_name=f"{name}.py"
        )
        fig.git_commit(student, solution=None)
        output_table.append((student.name, str(students_file)))
    fig.checkout_master()
    click.echo(tabulate(output_table, headers=("uco", "file"), tablefmt="fancy_grid"))


@task.command("add-using-name")
@click.argument("name")
@click.argument(
    "solutions",
    type=click.Path(dir_okay=True, file_okay=True, exists=True, readable=True),
)
@pass_course
def add_using_name(course, name, solutions):
    """Use students' name to add the solutions."""
    fig = FiGiTool(subject=course.subject, name=name)

    output_table = []
    for student in course.students_generator_progressbar:
        fig.checkout_master()
        branch = fig.create_students_branch(uco=student.uco)
        branch.checkout()

        student_files = list(Path(solutions).glob(f"{student.uco}*"))
        if not student_files:
            output_table.append((student.name, "File not found."))
            continue
        if len(student_files) != 1:
            output_table.append(
                (student.name, "More files found -- cannot determine the right one.")
            )
            continue
        student_file = student_files[0]

        fig.copy_and_add_solution(
            file_with_solution=student_file, new_name=f"{name}.py"
        )
        fig.git_commit(student, solution=None)
        output_table.append((student.name, str(student_file)))
    fig.checkout_master()
    click.echo(tabulate(output_table, headers=("uco", "file"), tablefmt="fancy_grid"))


@click.command()
@click.argument("name")
@pass_course
def task_delete(course, name):
    """Delete the branches for the task."""
    fig = FiGiTool(subject=None, name=name)
    table = fig.for_each_student(course, fig.get_line_task_delete)
    click.echo(tabulate(table, headers=("name", "branch"), tablefmt="fancy_grid"))


@task.command()
@click.argument("name")
@click.argument("cmd", type=click.STRING)
@pass_course
def foreach(course, name, cmd):
    """Run a command for each solution-branch."""
    fig = FiGiTool(subject=course.subject, name=name)

    for student in course.students:
        fig.checkout_master()
        click.echo(f"{'#' * 5} {student.name} {'#' * 5}")
        branch = fig.create_students_branch(uco=student.uco)
        branch.checkout()
        subprocess.call(cmd.split(" "))

    fig.checkout_master()


@project.command("push-master")
@pass_course
def push_master(course):
    """Push a master branch to all students' remotes."""
    fig = FiGiTool(subject=course.subject)

    fig.checkout_master()
    for student in course.students_generator_progressbar:
        fig.git_push(student)
    fig.checkout_master()


@task.command()
@click.argument("name")
@pass_course
def push(course, name):
    """Push the solutions to the students' projects."""
    fig = FiGiTool(subject=course.subject, name=name)

    for student in course.students_generator_progressbar:
        fig.checkout_master()
        branch = fig.create_students_branch(uco=student.uco)
        branch.checkout()

        if fig.repo.active_branch.commit == fig.repo.heads.master.commit:
            click.echo("No changes. No push.")
            continue

        fig.git_push(student=student)

    fig.checkout_master()


@task.command("create-mr")
@click.option(
    "--description", type=click.STRING, help="Description of the merge-request."
)
@click.argument("name")
@click.argument("list-txt", type=click.Path())
@pass_course
def create_mr(course, description, name, list_txt):
    """Create a merge-request with the solution for each student."""
    fig = FiGiTool(subject=course.subject, name=name)

    mrs_list = []
    for student in course.students_generator_progressbar:
        fig.checkout_master()
        fig.create_and_checkout_new_branch(student.uco)

        if fig.repo.active_branch.commit == fig.repo.heads.master.commit:
            click.echo("No changes. No merge request.")
            continue

        students_file, last_solution = fig.get_students_solution(
            list_txt=list_txt, student=student, name=name
        )
        if not students_file:
            mrs_list.append((student.name, "Not found in the list."))

        if not description:
            teacher_mail_file = students_file.parent / "teacher_email"
            description = teacher_mail_file.read_text()

        mr = fig.create_merge_request(
            uco=student.uco, student=student.name, description=description
        )
        mrs_list.append((mr.title, mr.url))

    fig.checkout_master()
    click.echo(tabulate(mrs_list, tablefmt="fancy_grid"))


@task.command()
@click.argument("name")
@click.argument("user")
@click.argument("login")
@click.argument("list-txt", type=click.Path())
@pass_course
def assign(course, name, user, login, list_txt):
    """Assign the {user} with {login} according to the list.txt file."""
    fig = FiGiTool(subject=course.subject, name=name)

    user_id = fig.service.gitlab_instance.users.list(username=login)[0].id

    students = []
    with open(list_txt) as list_file:
        for line in list_file.readlines():
            if user in line:
                line_split = line.split(" ")
                students.append(
                    Student(
                        name=f"{line_split[1][1:]} {line_split[2][:-1]}",
                        uco=line_split[3][:-2],
                    )
                )

    with click.progressbar(
        students, item_show_func=lambda student: str(student.name if student else "-")
    ) as students_list:
        for student_obj in students_list:
            mr = fig.get_pr(student=student_obj)
            project = fig.get_gitlab_project(student=student_obj)
            gitlab_mr = project.gitlab_repo.mergerequests.get(mr.id)
            gitlab_mr.assignee_id = user_id
            gitlab_mr.save()


@task.command("add-description-from-odpovednik")
@click.argument("name")
@click.argument("csv-file", type=click.File())
@pass_course
def add_description_from_odpovednik(course, name, csv_file):
    """Use the exported odpovednik to set task merge-request descriptions."""
    fig = FiGiTool(subject=course.subject, name=name)

    mrs_list = []
    for student in course.students_generator_progressbar:
        mr = fig.get_pr(student=student)
        project = fig.get_gitlab_project(student=student)
        mr_gitlab = project.gitlab_repo.mergerequests.get(mr.id)

        lines = csv.reader(csv_file, delimiter=";", quotechar='"')
        for uco, name, _, _, _, _, _, contents in lines:
            if uco == student.uco or name == student.name:
                formatted_content = (
                    contents.replace("\n|", "\n")
                    .replace("###", "#####")
                    .replace("=====", "###")
                    .replace("***", "*")
                    .replace(":\n    ", ":\n\n    ")
                )
                mr_gitlab.description = formatted_content
                mr_gitlab.save()
                mrs_list.append((student.name, mr.url, formatted_content))
                break
        else:
            mrs_list.append((student.name, mr.url, "not found"))

        csv_file.seek(0)

    click.echo(tabulate(mrs_list, tablefmt="fancy_grid"))


@task.command("list")
@click.option(
    "-a", "--assignee", type=click.STRING, help="Filter by the assignee name."
)
@click.option("--correction", is_flag=True, help="Show only corrections.")
@click.option("-s", "--show-assignee", is_flag=True, help="Show assignee")
@click.option("-d", "--diffs", is_flag=True, help="Show diffs tab")
@click.option("-l", "--link", "show_link", is_flag=True, help="Show links")
@click.option("-o", "--open", "open_link", is_flag=True, help="Open links in firefox")
@click.option("-m", "--mark", is_flag=True, help="Show the mark.")
@click.option("--is-msg", is_flag=True, help="Show the content for 'Poznamkovy blok'.")
@click.option("--plain", is_flag=True, help="Show in the plain mode.")
@click.argument("name")
@pass_course
def task_list(
    course,
    correction,
    assignee,
    show_assignee,
    diffs,
    show_link,
    open_link,
    mark,
    is_msg,
    plain,
    name,
):
    """List the students' merge-requests and other useful info about solutions."""
    fig = FiGiTool(subject=course.subject, name=name)

    mrs_list = fig.for_each_student(
        course,
        fig.get_line_mrs,
        correction=correction,
        diffs=diffs,
        show_link=show_link or is_msg,
        assignee=assignee,
        show_assignee=show_assignee,
        open_link=open_link,
        mark=mark,
        is_msg=is_msg,
    )

    if not is_msg:
        click.echo(tabulate(mrs_list, tablefmt="fancy_grid" if not plain else "simple"))
        return

    for name, link, result in mrs_list:
        print(
            f"{name}\n"
            f"{20 * '#'}\n"
            f"# Známka *{result[10:]}\n"
            f"\n"
            f"Komentáře k řešení:\n"
            f"{link}\n"
            f"(soubor flake8.txt obsahuje kontrolu PEP8 pomocí nástroje flake8)\n"
        )


@task.command("edit")
@click.option(
    "--description", type=click.STRING, help="Description of the merge-request."
)
@click.argument("name")
@pass_course
def edit(course, description, name):
    """Edit the students' merge-requests."""
    fig = FiGiTool(subject=course.subject, name=name)

    mrs_list = []
    for student in course.students_generator_progressbar:
        mr = fig.get_pr(student=student)
        project = fig.get_gitlab_project(student=student)
        mr_gitlab = project.gitlab_repo.mergerequests.get(mr.id)
        if description:
            mr_gitlab.description = description
            mrs_list.append((student.name, mr.url, description))
        mr_gitlab.save()

    click.echo(tabulate(mrs_list, tablefmt="fancy_grid"))


@task.command()
@click.argument("name")
@pass_course
def checkout(course, name):
    """
    Checkout the branch matching the filtered user.

    (Exactly one match required.)
    """
    fig = FiGiTool(subject=course.subject, name=name)
    if len(course.students) > 1:
        table = [(s.name, s.uco) for s in course.students]
        click.echo(
            tabulate(
                table, headers=("name", "project", "web_url"), tablefmt="fancy_grid"
            )
        )
        click.echo("Multiple occurrences. Switching to master.")
        fig.checkout_master()
    elif len(course.students) == 1:
        fig.create_and_checkout_new_branch(uco=course.students[0].uco)
    else:
        click.echo("No match")


if __name__ == "__main__":
    figitool()
