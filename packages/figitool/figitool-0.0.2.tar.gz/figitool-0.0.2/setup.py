from setuptools import setup, find_packages

setup(
    name="figitool",
    version="0.0.2",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Click",
        "python-gitlab",
        "GitPython",
        "ogr",
        "PyYAML",
        "tabulate",
    ],
    entry_points="""
        [console_scripts]
        figitool=figitool.figitool:figitool
    """,
)
