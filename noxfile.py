import os
import tempfile

import nox

nox.options.sessions = "lint", "safety", "tests"


locations = "src", "tests", "noxfile.py"


@nox.session(python=["3.9"])
def tests(session):
    args = session.posargs or ["--cov", "-m", "not e2e"]
    session.run("poetry", "install", external=True)
    session.run("pytest", *args)


@nox.session(python=["3.9"])
def lint(session):
    args = session.posargs or locations
    session.install(
        "flake8",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-isort",
    )
    session.run("flake8", *args)


@nox.session(python="3.9")
def black(session):
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


@nox.session(python="3.9")
def safety(session):
    requirements = tempfile.NamedTemporaryFile(mode="w", delete=False)
    session.run(
        "poetry",
        "export",
        "--dev",
        "--format=requirements.txt",
        "--without-hashes",
        f"--output={requirements.name}",
        external=True,
    )
    session.install("safety")
    session.run("safety", "check", f"--file={requirements.name}", "--full-report")
    requirements.close()
    os.remove(requirements.name)
