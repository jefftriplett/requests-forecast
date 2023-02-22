set dotenv-load := false

@_default:
    just --list

# Format the justfile
@fmt:
    just --fmt --unstable

# --------------------------------------------------
# scripts to rule them all recipes
# --------------------------------------------------

@bootstrap:
    pip install -U pip pip-tools pre-commit
    pip install --upgrade -r requirements.in

@lint:
    just pre-commit

@update:
    just pip-compile-update

# --------------------------------------------------
# our recipes
# --------------------------------------------------

# Update the version; Used before release to production
@bump *ARGS:
    bumpver update {{ ARGS }}

@bump-lint *ARGS:
    just bump --dry --no-fetch {{ ARGS }}

@pip-compile:
    pip-compile --resolver=backtracking requirements.in

@pip-compile-update:
    pip-compile --resolver=backtracking --upgrade

# Run pre-commit
@pre-commit *ARGS:
    pre-commit run {{ ARGS }}

@pre-commit-all-files:
    just pre-commit --all-files
