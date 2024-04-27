IMAGE_NAME = etl_mb
DOCKERFILE = Dockerfile

build:
	docker rmi $(IMAGE_NAME)
	docker build -t $(IMAGE_NAME) -f $(DOCKERFILE) .




