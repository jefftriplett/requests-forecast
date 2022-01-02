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
    run("python setup.py sdist")
    run("python setup.py bdist_wheel")


@task
def pypi_test(c):
    run("python setup.py sdist -r test")
    run("python setup.py bdist_wheel -r test")


@task
def pypi_upload(c):
    run("python setup.py sdist upload")
    run("python setup.py bdist_wheel upload")


@task
def pypi_test_upload(c):
    run("python setup.py sdist upload -r test")
    run("python setup.py bdist_wheel upload -r test")


@task
def test(c):
    run("py.test")
