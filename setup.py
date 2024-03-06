from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="team_task_manager",
    version="0.0.0",
    description="This is a simple task management system small businesses can use.",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    long_description=long_description,
    long_description_content_type="markdown",
    url="https://github.com/a-yh-chew/team-task-manager.git",
    author="a-yh-chew",
    author_email="a.yh.chew@gmail.com",
    license="Apache Software",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Win32 (MS Windows)",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3.12",
        "Topic :: System :: Systems Administration"
    ],
    install_requires=["setuptools>=69.1.1"],
    extras_require={
        "dev": ["pytest>=8.0.2", "twine>=5.0.0"],
    },
    python_requires=">=3.12",
)
