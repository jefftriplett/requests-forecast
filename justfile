@_default:
    just --list

@bootstrap:
    pip install -U pip pip-tools pre-commit
    pip install --upgrade -r requirements.in

@pip-compile:
    pip-compile --resolver=backtracking requirements.in

@pip-compile-update:
    pip-compile --resolver=backtracking --upgrade

# Run pre-commit
@pre-commit *ARGS:
    pre-commit run {{ ARGS }}

@pre-commit-all-files:
    just pre-commit --all-files
