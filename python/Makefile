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

# Основной target по умолчанию
.DEFAULT_GOAL := all

# Makefile targets
all: build build_last push deploy buildarm buildamd release
#сборка билда с тегом последней версии из github
build:
	@echo "Сборка Docker image с текущей версией из Github..."
	docker build -t $(IMAGE_NAME):$(APP_VERSION) .

build_last: 
	@echo "Сборка Docker Image последней версии..."
	docker build -t $(IMAGE_NAME):latest .
	

# Задача для сборки образа с архитектурой ARM64
buildarm:
	@echo "Сборка Docker образа для архитектуры $(ARCHARM)..."
	docker buildx build --platform linux/$(ARCHARM) -t $(IMAGE_NAME):$(TAGARM) --push .

# Задача для сборки образа с архитектурой AMD64
buildamd:
	@echo "Сборка Docker образа для архитектуры $(ARCAMD)..."
	docker buildx build --platform linux/$(ARCHAMD) -t $(IMAGE_NAME):$(TAGAMD) --push .

push:
	docker push $(IMAGE_NAME):latest

deploy:
	kubectl set image deployment/$(K8S_DEPLOYMENT) $(K8S_DEPLOYMENT)=$(IMAGE_NAME):latest -n $(K8S_NAMESPACE)

rollback:
	kubectl rollout undo deployment/$(K8S_DEPLOYMENT) -n $(K8S_NAMESPACE)

# Задача для helm upgrade релиза с текущим git-hub hash комита значение K8S_DEPLOYMENT в нашем случае совпадает с названием релиза хельм
release:
	helm upgrade $(K8S_DEPLOYMENT) $(HELM_DIR) --set=image.tag=$(APP_VERSION)

.PHONY: all build build_last push deploy rollback buildarm buildamd release
