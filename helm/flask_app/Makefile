# Переменные
HELM_RELEASE_NAME := flask-test1
VALUES_FILE := ./values.yaml
IMAGENAME := hevdin/flask-test

# Динамическое получение последнего Git commit hash
IMAGETAG := $(shell git rev-parse --short HEAD)

# Флаги для Helm
HELM_FLAGS := --set image.tag=$(IMAGETAG)
              
# Цель для установки/обновления Helm-чарта
helm-deploy:
	helm upgrade --install $(HELM_RELEASE_NAME) \
	-f $(VALUES_FILE) $(HELM_FLAGS)

# Генерация values.yaml с использованием Git commit hash
helm-generate-values:
	truncate -s 0 $(VALUES_FILE)
	echo "image:  $(IMAGENAME)" >> $(VALUES_FILE)
	echo "tag: $(IMAGETAG)" >> $(VALUES_FILE)

# Полный процесс: генерация values.yaml + деплой
helm-full-deploy: helm-generate-values helm-deploy
