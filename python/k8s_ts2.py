from flask import Flask, jsonify
from kubernetes import client, config
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config.load_incluster_config()
v1 = client.CoreV1Api()

@app.route('/kuber', methods=['GET'])
def main():
    label_selector = "app_type=flask-test"
    try:
        logger.info("Получение сервисов с лейблом: %s", label_selector)
        services = v1.list_service_for_all_namespaces(label_selector=label_selector)
        logger.info("Количество сервисов, найденных: %d", len(services.items))

        service_list = []
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

        return jsonify(service_list), 200
    except Exception as e:
        logger.error("Ошибка при получении сервисов: %s", str(e))
        return jsonify({'error': str(e)}), 500
    
    if __name__ == "__main__":
    main()
