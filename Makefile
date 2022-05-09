# defines name of image dynamically
timestamp:=$(shell date +%Y%m%d_%H%M%S)
image_name:=patterned:$(timestamp)


make local_run:
	docker build -t $(image_name) -f ./Dockerfile . ;\
	docker run --interactive --tty $(image_name) ;\
	clear


make run:

	python3 -m src.main


make test:

	python3 -m testing.unittest_main

make docker_cleanup:
	docker system prune -a