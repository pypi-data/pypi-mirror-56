# FIGITOOL

Python script for simplifying the teachers work:

### Workflow

1. Create a GitLab project for each student.
2. Share the project with the students.
3. For each task/homewark/exercise:
    - One branch for each user and the task.
    - Add the students' solutions. (Various ways possible.)
    - Commands like `flake8` can be run on each user-task branch.
    - Push the students' solutions.
    - Create the merge-request where the diff is the students solution.
    - Review the solution:
        - support for assignments, browser opening, filtering
        - special comments can be used to generate marks.
    - Update the solution if needed.
    - Generate an output sutable for the IS odpovednik that can be coppied to the IS.


### WIKI

User documentation can be found here:
https://gitlab.fi.muni.cz/xlachma1/figitool/wikis

### Installation

Currently, the only way how to install figitool is via `pip` (e.i. `pip3` since its python3 only):

```
pip3 install git+https://gitlab.fi.muni.cz/xlachma1/figitool.git
```

### The CLI

```
$ figitool --help
Usage: figitool [OPTIONS] COMMAND [ARGS]...

  Tool for helping teachers to automate the code-review workflow.

Options:
  -f, --filter TEXT         Filter -- name/uco substring
  -s, --start-with INTEGER
  --students-file FILENAME  csv with students (default 'seznam_export.csv')
  --subject TEXT            Name of the subject, defaults to the dir name. It
                            is used for various naming like project name.
  --help                    Show this message and exit.

Commands:
  check     Print the info about config and current environment.
  project   Manage the students' projects.
  students  Manage students of your course.
  task      Manage the task(s) for the students.
```

### Todo:

- [ ] better documentation and CLI messages
- [ ] error-prone code, better exception caching,...
- [ ] more generic
