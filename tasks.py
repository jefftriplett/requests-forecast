from invoke import run, task


@task
def clean(c):
    run("cd docs && make clean")


@task
def docs(c):
    run("cd docs && make html")


@task
def foreman(c):
    run("foreman start -f Procfile.dev")


@task
def git_push(c):
    run("git push origin --all")
    run("git push bitbucket --all")
    run("git push gitlab --all")


@task
def pypi(c):
    run("python -m build")


@task
def pypi_upload(c):
    run("python -m twine upload dist/*")


@task
def test(c):
    run("pytest")
