# Определяем переменные
IMAGE_NAME=hevdin/flask-test
K8S_DEPLOYMENT=flask-test1
K8S_NAMESPACE=default
ARCHARM=arm64
TAGARM=$(ARCHARM)
ARCHAMD=amd64
TAGAMD=$(ARCHAMD)
APP_VERSION := $(shell git rev-parse --short HEAD)
HELM_DIR=../helm/flask_app/
DOCKER_BUILDER ?= mybuilder

# Основной target по умолчанию
.DEFAULT_GOAL := all

# Все цели Makefile
.PHONY: all build build_last push deploy rollback buildarm buildamd release

# Makefile targets
all: build push deploy release

ensure-builder:
	@if docker buildx ls | grep -q $(DOCKER_BUILDER); then \
		echo "Builder $(DOCKER_BUILDER) уже существует, используем его"; \
	else \
		echo "Builder $(DOCKER_BUILDER) не найден, создаем его"; \
		docker buildx create --use --name $(DOCKER_BUILDER) --driver docker-container; \
	fi


#сборка билда с тегом последней версии из github
build: ensure-builder
	@echo "Сборка Docker image с версией $(APP_VERSION)"
	docker buildx build --platform linux/$(ARCHARM),linux/$(ARCHAMD) -t $(IMAGE_NAME):$(APP_VERSION) -t $(IMAGE_NAME):latest --push .

deploy:
	@echo "Деплоим image $(APP_VERSION) в кубер $(K8S_NAMESPACE)/$(K8S_DEPLOYMENT) через апдейт Deployment-а"
	kubectl set image deployment/$(K8S_DEPLOYMENT) $(K8S_DEPLOYMENT)=$(IMAGE_NAME):latest -n $(K8S_NAMESPACE)

rollback:
	@echo "Откатываем $(K8S_NAMESPACE)/$(K8S_DEPLOYMENT)"
	kubectl rollout undo deployment/$(K8S_DEPLOYMENT) -n $(K8S_NAMESPACE)

# Задача для helm upgrade релиза с текущим git-hub hash комита значение K8S_DEPLOYMENT в нашем случае совпадает с названием релиза хельм
release:
	@echo "Деплоим image $(APP_VERSION) в кубер $(K8S_DEPLOYMENT) через Helm Chart $(HELM_DIR)"
	helm upgrade $(K8S_DEPLOYMENT) $(HELM_DIR) --set=image.tag=$(APP_VERSION)

