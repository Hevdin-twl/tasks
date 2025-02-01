from kubernetes import client, config
import logging

from kubernetes import client, config

def main():
    # Загружаем конфигурацию, обычно она автоматически настраивается в рамках кластера
    config.load_incluster_config()

    # Создаем объект API для работы с серверами Kubernetes
    v1 = client.CoreV1Api()

    # Фильтруем сервисы по лейблу app_type: flask-test
    label_selector = "app_type=flask-test"

    try:
        # Получаем список всех сервисов с указанным лейблом
        services = v1.list_service_for_all_namespaces(label_selector=label_selector)

        # Обрабатываем и выводим информацию о сервисах и их портах
        for service in services.items:
            print(f"Service Name: {service.metadata.name}, Namespace: {service.metadata.namespace}")
            for port in service.spec.ports:
                print(f"  - Port: {port.port}, Protocol: {port.protocol}")

    except client.exceptions.ApiException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
