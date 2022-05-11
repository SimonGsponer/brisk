# defines name of image dynamically
timestamp:=$(shell date +%Y%m%d_%H%M%S)
image_name:=patterned:$(timestamp)

make dev_setup:
	pip3 install -r requirements.txt ;\
	pip3 install -r requirements-dev.txt

make local_run:
	docker build -t $(image_name) -f ./Dockerfile . ;\
	docker run --interactive --tty $(image_name) ;\
	clear

make run:
	python3 -m src.main

make qa: format doccheck typecheck lint unittest

make format:
	python3 -m yapf --in-place --recursive --style pep8 --parallel ./src/ ./testing/

make typecheck:
	python3 -m mypy --config-file=./devops/mypy.ini --strict ./src/ ./testing/

make doccheck:
	python3 -m pydocstyle --convention=google --count ./src/ ./testing/

make lint:
	python3 -m pylint ./src/ ./testing/

make test:
	python3 -m testing.unittest_main

make docker_cleanup:
	docker system prune -a