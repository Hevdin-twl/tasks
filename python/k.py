from kubernetes import client, config
from flask import Flask, request, jsonify
import logging
import urllib.request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import logging
import urllib.request

def main():
    # Определение лейбла сервиса
    label_selector = "app_type=flask-test"
    logger.info("Получение сервисов с лейблом: %s", label_selector)
    services = v1.list_service_for_all_namespaces(label_selector=label_selector)
    logger.info("Количество сервисов, найденных: %d", len(services.items))
    
    try:
        service_list = []
        dns_names = []  # Создаем массив для хранения DNS имен
        
        for service in services.items:
            service_info = {
                'name': service.metadata.name,
                'namespace': service.metadata.namespace,
                'ports': []
            }
            for port in service.spec.ports:
                service_info['ports'].append({
                    'port': port.port,
                    'protocol': port.protocol
                })
            service_list.append(service_info)
            
            # Формируем DNS имя и добавляем его в массив dns_names
            dns_name = f"{service.metadata.name}.default.svc.cluster.local:8080/sleep"
            dns_names.append(dns_name)  # Добавляем в массив
            
        # Создаем массив для хранения ответов от веб-сервера
        response = []
        
        for dns_name in dns_names:
            try:
                with urllib.request.urlopen(dns_name) as url_response:
                    response_data = url_response.read().decode('utf-8')
                    response.append(response_data)
                    logger.info("Cluster Dns name: %s. Response: %s", dns_name, response_data)
            except Exception as e:
                logger.error("Ошибка при обращении к %s: %s", dns_name, e)
                response.append(f"Error accessing {dns_name}: {e}")
            
    except Exception as e:
        logger.error("Произошла ошибка: %s", e)

    return service_list, response  # Возвращаем список сервисов и массив ответов
 
if __name__ == "__main__":
    main()