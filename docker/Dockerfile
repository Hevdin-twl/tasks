# Используем мульти-аргументы для определения архитектуры
FROM ubuntu:latest

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
KUBECTL_URL="https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/${ARCH}/kubectl" && \
curl -LO ${KUBECTL_URL} && \
chmod +x kubectl && \
mv kubectl /usr/local/bin/ && \
rm kubectl_version
EOF

# Устанавливаем рабочую директорию
WORKDIR /workdir

# Устанавливаем точку входа
CMD ["bash"]
