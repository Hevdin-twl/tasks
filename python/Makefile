# Определяем переменные
IMAGE_NAME=hevdin/flask-test
K8S_DEPLOYMENT=flask-test1
K8S_NAMESPACE=default
ARCHARM=arm64
TAGARM=$(ARCHARM)
ARCHAMD=amd64
TAGAMD=$(ARCHAMD)

# Основной target по умолчанию
.DEFAULT_GOAL := all

# Makefile targets
all: build push deploy buildarm buildamd

build:
	@echo "Сборка Docker образа для образа поумолчанию..."
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

.PHONY: all build push deploy rollback buildarm buildamd
