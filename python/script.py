from flask import Flask, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from kubernetes import client, config
import logging
import urllib.request
import random
import os
import time

# инициализация Flask
app = Flask(__name__)

# инициализация логгера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# инициализация конфигурации кубера через его api
config.load_incluster_config()
v1 = client.CoreV1Api()

# инициализация планировщика
scheduler = BackgroundScheduler()

# функция ожидания принимает параметр GET sleep?sleep=[значение]
@app.route('/sleep', methods=['GET'])
def sleep_route():
    host_url = request.host_url
    sleep_value = request.args.get('seconds')
    if not sleep_value:
        seconds_wait = random.randint(1, 5)
    else:
        try:
            seconds_wait = int(sleep_value)
            if seconds_wait < 1:
                raise ValueError("Значение должно быть больше 0.")
        except ValueError:
            return "Параметр 'sleep' должен быть целым числом больше 0.", 400
    logger.info(f"{host_url} Aslept {seconds_wait} seconds")
    time.sleep(seconds_wait)
    return f"Ждали {seconds_wait} секунд."

# функция проверки доступности вызывается GET параметром /self-test
@app.route('/self-test', methods=['GET'])
def self_test():
    return jsonify({"message": "Self-test successful"}), 200

# функция ожидания перед запуском
def wait(seconds):
    logger.info(f"Ожидание перед запуском {seconds} секунд...")
    time.sleep(seconds)
    logger.info("Ожидание завершено.")

# создание endpoint для вывода информации от Kubernetes API
@app.route('/kuber', methods=['GET'])
def get_service():
    label_selector = "service_type=flask-test-worker"
    logger.info("Получение сервисов с лейблом: %s", label_selector)
    
    try:
        services = v1.list_service_for_all_namespaces(label_selector=label_selector)
        logger.info("Количество сервисов, найденных: %d", len(services.items))
        
        service_list = []
        responses = []
        
        for service in services.items:
            service_info = {
                'name': service.metadata.name,
                'namespace': service.metadata.namespace,
                'ports': [{'port': port.port, 'protocol': port.protocol} for port in service.spec.ports]
            }
            service_list.append(service_info)

            dns_name = f"http://{service.metadata.name}.default.svc.cluster.local:8080/sleep"
            try:
                with urllib.request.urlopen(dns_name) as url_response:
                    response_data = url_response.read().decode('utf-8')
                    responses.append(response_data)
                    logger.info("Cluster Dns name: %s. Response: %s", dns_name, response_data)
            except Exception as e:
                logger.error("Ошибка при обращении к %s: %s", dns_name, e)
                responses.append(f"Error accessing {dns_name}: {e}")
        
        return jsonify({'services': service_list, 'responses': responses})
    
    except Exception as e:
        logger.error("Произошла ошибка при получении сервисов: %s", e)
        return jsonify({'error': 'Ошибка при получении сервисов'}), 500

# функция планировщика запуска функции get_services с интервалом в 5 секунд
def start_scheduler():
    scheduler.add_job(func=get_service, trigger='interval', seconds=5)
    scheduler.start()

# функция считывания переменной окружения времени ожидания перед запуском
def main():
    startup_delay = os.environ.get('STARTUP_DELAY_SECONDS')
    logger.info(f"Значение ожидания: {startup_delay}")

    if startup_delay is not None:
        try:
            delay_seconds = int(startup_delay)
            if delay_seconds < 0:
                raise ValueError("Значение задержки не может быть отрицательным.")
        except ValueError as e:
            logger.info(f"Ошибка: {e}. Используем значение по умолчанию: 0.")
            delay_seconds = 0
    else:
        logger.info("Переменная окружения STARTUP_DELAY_SECONDS не найдена. Используем значение по умолчанию: 0.")
        delay_seconds = 0

    wait(delay_seconds)
    start_scheduler()  # Запускаем планировщик
    app.run(host='0.0.0.0', port=8080, debug=False)

# Вызов функции main
if __name__ == '__main__':
    main()