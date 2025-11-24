.PHONY: up down build
REG=smcsde
NAME=cicd
TAG=1
VERSION=latest
DOCKERHUB_TOKEN=$(PWD)/.dockerhub-token
JENKINS_TOKEN=$(PWD)/.jenkins-token


build:
	docker-compose build --pull

up:
	docker-compose up -d

down:
	docker-compose down

# see available images: docker images
# use command to tag and upload latest build: make VERSION=v2 upload
upload:
	docker tag $(REG)/$(NAME):$(TAG)_server $(REG)/$(NAME):$(TAG)_server-$(VERSION)
	docker tag $(REG)/$(NAME):$(TAG)_client $(REG)/$(NAME):$(TAG)_client-$(VERSION)
	@if [ ! -f $(DOCKERHUB_TOKEN) ]; then \
		cat $(DOCKERHUB_TOKEN) | docker login -u $(REG) --password-stdin; \
	else \
		docker login; \
	fi
	docker push $(REG)/$(NAME):$(TAG)_server-$(VERSION)
	docker push $(REG)/$(NAME):$(TAG)_client-$(VERSION)
	
jenkins:
	# run jenkins
	@echo "Getting jenkings ready..."
	cd ~/Zeugs/Tools/Build/Jenkins && docker-compose up -d
	@sleep 5
	@echo "Starting build..."
	@if [ -f $(JENKINS_TOKEN) ]; then \
		TOKEN=$$(cat $(JENKINS_TOKEN)); \
		curl --user "admin:$$TOKEN" --request 'POST' "http://localhost:8080/job/cicd/build?token=$(NAME)"; \
	else \
		echo "Error: No jenkins token!"; \
		exit 1; \
	fi
		
