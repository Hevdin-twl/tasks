# Определяем переменные
IMAGE_NAME=hevdin/myimages/flask-test1
K8S_DEPLOYMENT=flask-test1
K8S_NAMESPACE=default

# Основной target по умолчанию
.DEFAULT_GOAL := all

# Makefile targets
all: build push deploy

build:
	docker build -t $(IMAGE_NAME):latest .

push:
	docker push $(IMAGE_NAME):latest

deploy:
	kubectl set image deployment/$(K8S_DEPLOYMENT) $(K8S_DEPLOYMENT)=$(IMAGE_NAME):latest -n $(K8S_NAMESPACE)

rollback:
	kubectl rollout undo deployment/$(K8S_DEPLOYMENT) -n $(K8S_NAMESPACE)

.PHONY: all build push deploy rollback
