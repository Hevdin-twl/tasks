# Выкачиваем из dockerhub образ с python
FROM python:3.11.0

#Обновление qemu
RUN apt update \ 
    apt install qemu-system

# Установка необходимых пакетов для работы с kubectl
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    && update-ca-certificates

# Получение версии kubectl и установка
RUN <<EOF 
curl -L https://dl.k8s.io/release/stable.txt -o kubectl_version && \
KUBECTL_VERSION=$(cat kubectl_version) && \
ARCH=$(uname -m) && \
if [ "$ARCH" = "aarch64" ]; then ARCH="arm64"; fi; \
KUBECTL_URL="https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/${ARCH}/kubectl" && \
curl -LO ${KUBECTL_URL} && \
chmod +x kubectl && \
mv kubectl /usr/local/bin/ && \
rm kubectl_version
EOF
    
# Устанавливаем рабочую директорию для конфигурации среды
WORKDIR /backend
# Скачиваем/обновляем необходимые библиотеки для проекта 
COPY requirements.txt /backend
RUN pip3 install --upgrade pip -r requirements.txt
# копируем содержимое папки, где находится Dockerfile, в рабочую директорию контейнера
COPY . /backend
# Устанавливаем порт, который будет использоваться для сервера
EXPOSE 8080
# Запускаем приложение
CMD ["python3", "-u", "script.py"]
