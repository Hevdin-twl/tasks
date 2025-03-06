from kubernetes import client, config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        
        logger.info(service_list)
        
        # Выводим значения массива dns_names
        logger.info("Сформированы следующие DNS имена: %s", dns_names)
    
        # Возвращаем JSON-ответ с кодом 200
        return jsonify(service_list), 200
    except Exception as e:
        logger.error("Ошибка при получении сервисов: %s", str(e))
        return jsonify({'error': str(e)}), 500 
 
if __name__ == "__main__":
    main()