.PHONY: up down build
REG=smcsde
NAME=cicd
VERSION=latest
DOCKERHUB_TOKEN=$(PWD)/.dockerhub-token
JENKINS_TOKEN=$(PWD)/.jenkins-token


build:
	VERSION=$(VERSION) docker-compose build --pull

up:
	VERSION=$(VERSION) docker-compose up -d

down:
	VERSION=$(VERSION) docker-compose down

upload:
	docker tag $(REG)/$(NAME):server $(REG)/$(NAME):server-$(VERSION)
	docker tag $(REG)/$(NAME):client $(REG)/$(NAME):client-$(VERSION)
	@if [ -f $(DOCKERHUB_TOKEN) ]; then \
		cat $(DOCKERHUB_TOKEN) | docker login -u $(REG) --password-stdin; \
	else \
		docker login; \
	fi
	docker push $(REG)/$(NAME):server-$(VERSION)
	docker push $(REG)/$(NAME):client-$(VERSION)
	
jenkins:
	# run jenkins
	@echo "Getting jenkings ready..."
	cd ~/Zeugs/Tools/Build/Jenkins && docker-compose up -d
	@sleep 10
	@echo "Starting build..."
	@if [ -f $(JENKINS_TOKEN) ]; then \
		TOKEN=$$(cat $(JENKINS_TOKEN)); \
		curl --user "admin:$$TOKEN" --request 'POST' "http://localhost:8080/job/cicd/build?token=$(NAME)"; \
	else \
		echo "Error: No jenkins token!"; \
		exit 1; \
	fi
		
