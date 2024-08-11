.ONESHELL:

image_base_name:=brisk_ii

timestamp:=$(shell date +%Y%m%d_%H%M%S)
image_name:=$(image_base_name)_:$(timestamp)
pyenv_name:=$(image_base_name)-3.10.12

make python_venv:
	pyenv virtualenv 3.10.12 $(pyenv_name) ; \
	source ~/.pyenv/versions/$(pyenv_name)/bin/activate ; \
	pip3 install --upgrade pip ; \
	pip3 install maturin

make compile:
	source ~/.pyenv/versions/$(pyenv_name)/bin/activate ; \
	maturin develop

make run:
	source ~/.pyenv/versions/$(pyenv_name)/bin/activate ; \
	python3 -m python.brisk.main

make build:
	source ~/.pyenv/versions/$(pyenv_name)/bin/activate ; \
	maturin build