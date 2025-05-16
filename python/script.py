from flask import Flask, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from kubernetes import client, config
import logging
import urllib.request
import random
import os
import time

# Инициализация Flask
app = Flask(__name__)

# Инициализация логгера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация конфигурации кубера через его API
config.load_incluster_config()
v1 = client.CoreV1Api()

# Инициализация планировщика
scheduler = BackgroundScheduler()

def setup_environment():
    """ Настройка и возвращение времени ожидания перед запуском. """
    startup_delay = os.environ.get('STARTUP_DELAY_SECONDS', 0)
    try:
        delay_seconds = max(0, int(startup_delay))
    except ValueError:
        logger.warning(f"Некорректное значение переменной окружения: {startup_delay}. Используется значение по умолчанию: 0.")
        delay_seconds = 0
    logger.info(f"Значение ожидания перед запуском: {delay_seconds} секунд.")
    return delay_seconds

def delay(seconds):
    """ Ожидание указанного количества секунд с логированием. """
    logger.info(f"Ожидание перед запуском {seconds} секунд...")
    time.sleep(seconds)
    logger.info("Ожидание завершено.")

@app.route('/sleep', methods=['GET'])
def sleep_route():
    """ Эндпоинт для ожидания заданного времени. """
    host_url = request.host_url
    sleep_value = request.args.get('seconds')
    seconds_wait = validate_sleep_value(sleep_value)

    if seconds_wait is None:
        return "Параметр 'sleep' должен быть целым числом больше 0.", 400

    logger.info(f"{host_url} Aslept {seconds_wait} seconds")
    time.sleep(seconds_wait)
    
    return f"Ждали {seconds_wait} секунд."

def validate_sleep_value(sleep_value):
    """ Проверяет и валидирует значение, переданное в качестве параметра ожидания. """
    if not sleep_value:
        return random.randint(1, 5)
    try:
        seconds_wait = int(sleep_value)
        if seconds_wait < 1:
            raise ValueError("Значение должно быть больше 0.")
        return seconds_wait
    except ValueError:
        return None

@app.route('/self-test', methods=['GET'])
def self_test():
    """ Эндпоинт для проверки доступности сервиса. """
    return jsonify({"message": "Self-test successful"}), 200

@app.route('/kuber', methods=['GET'])
def get_services():
    """ Эндпоинт для получения информации от Kubernetes API о сервисах. """
    return jsonify(fetch_services_from_k8s())

def fetch_services_from_k8s():
    """ Функция для получения сервисов из Kubernetes. """
    label_selector = "service_type=flask-test-worker"
    logger.info("Получение сервисов с лейблом: %s", label_selector)
    
    try:
        services = v1.list_service_for_all_namespaces(label_selector=label_selector)
        service_list = []

        for service in services.items:
            service_info = extract_service_info(service)
            service_list.append(service_info)
            log_service_response(service_info)

        return {'services': service_list}
    
    except Exception as e:
        logger.error("Произошла ошибка при получении сервисов: %s", e)
        return {'error': 'Ошибка при получении сервисов'}, 500

def extract_service_info(service):
    """ Извлекает информацию о сервисе. """
    return {
        'name': service.metadata.name,
        'namespace': service.metadata.namespace,
        'ports': [{'port': port.port, 'protocol': port.protocol} for port in service.spec.ports]
    }

def log_service_response(service_info):
    """ Получает ответ от сервиса и логирует его. """
    dns_name = f"http://{service_info['name']}.default.svc.cluster.local:8080/sleep"
    try:
        with urllib.request.urlopen(dns_name) as url_response:
            response_data = url_response.read().decode('utf-8')
            logger.info("Cluster Dns name: %s. Response: %s", dns_name, response_data)
    except Exception as e:
        logger.error("Ошибка при обращении к %s: %s", dns_name, e)

def start_scheduler():
    """ Запускает планировщик для периодического выполнения функции получения сервисов. """
    scheduler.add_job(func=fetch_services_from_k8s, trigger='interval', seconds=5)
    scheduler.start()

def main():
    """ Главная функция запуска приложения. """
    delay_seconds = setup_environment()
    delay(delay_seconds)
    start_scheduler()
    app.run(host='0.0.0.0', port=8080, debug=False)

if __name__ == '__main__':
    main()
