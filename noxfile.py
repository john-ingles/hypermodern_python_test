import os
import tempfile

import nox

nox.options.sessions = "lint", "safety", "mypy", "tests"


locations = "src", "tests", "noxfile.py"


package = "hypermodern_python_test"


@nox.session(python="3.9")
def tests(session):
    args = session.posargs or ["--cov", "-m", "not e2e"]
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(
        session, "coverage[toml]", "pytest", "pytest-cov", "pytest-mock"
    )
    session.run("pytest", *args)


@nox.session(python="3.9")
def lint(session):
    args = session.posargs or locations
    install_with_constraints(
        session,
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
    install_with_constraints(session, "black")
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
    install_with_constraints(session, "safety")
    session.run("safety", "check", f"--file={requirements.name}", "--full-report")
    requirements.close()
    os.remove(requirements.name)


@nox.session(python="3.9")
def mypy(session):
    args = session.posargs or locations
    install_with_constraints(session, "mypy")
    session.run("mypy", *args)


@nox.session(python="3.9")
def typeguard(session):
    args = session.posargs or ["-m", "not e2e"]
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(session, "pytest", "pytest-mock", "typeguard")
    session.run("pytest", f"--typeguard-packages={package}", *args)


def install_with_constraints(session, *args, **kwargs):
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
    session.install(f"--constraint={requirements.name}", *args, **kwargs)
    requirements.close()
    os.remove(requirements.name)
