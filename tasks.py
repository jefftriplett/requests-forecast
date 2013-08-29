from invoke import run, task


@task
def clean():
    run('cd docs && make clean')


@task
def docs():
    run('cd docs && make html')


@task
def foreman():
    run('foreman start -f Procfile.dev')


@task
def pypi():
    run('python setup.py sdist')
    run('python setup.py bdist_wheel')


@task
def pypi_upload():
    run('python setup.py sdist upload')
    run('python setup.py bdist_wheel upload')


@task
def test():
    run('py.test '
        '--cov-report term-missing '
        '--cov tests/test_requests_forecast.py')
