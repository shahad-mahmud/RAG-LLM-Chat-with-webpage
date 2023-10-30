#! /usr/bin/bash

# Sample files
echo "Preparing sample files"
declare -a files=("requirements-dev.txt" "requirements-prod.txt" "main.py" "Dockerfile"
    "docker-compose.yaml" ".env-sample" ".pre-commit-config.yaml" ".gitignore" "Makefile")

for file_name in ${files[@]}; do
    if [[ ! -f $file_name ]]; then
        touch $file_name
    fi
done

# Prepare .env files
cat .env-sample >>.env
cat .env-sample >>.env-prod

# Install required packages
echo "Installing python packages"
pip install -r requirements-dev.txt

# flake-8 configs
if [[ ! -f .flake8 ]]; then
    echo "[flake8]" >.flake8
    echo "max-line-length = 88" >>.flake8
    echo "ignore = E203, W503" >>.flake8
fi

# install pre-commit hooks and run on all files
echo "Installing pre-commit hooks and running on all files"
pre-commit install
pre-commit autoupdate
pre-commit run --all-files

echo "Setup complete"
