build:
	docker build --no-cache -t big-data-webui .

run:
	docker run --rm -it -p 8501:8501 -v $(shell pwd):/app -v /var/run/docker.sock:/var/run/docker.sock -v ../:/apps big-data-webui

.PHONY: run build

