from flask import Flask, request, jsonify
from kubernetes import client, config
import logging
import urllib.request
import random
import os
import time
import logging

# инициализация Flask
app = Flask(__name__)

#инициализация логггера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#инициализация конфигурации кубера через его api
config.load_incluster_config()
v1 = client.CoreV1Api()

# функция ожидания прнимает параметр GET sleep?sleep=[значение]
@app.route('/sleep', methods=['GET'])
def sleep_route():
    # Получаем GET параметр 'sleep'
    host_url = request.host_url
    sleep_value = request.args.get('seconds')

    # Если параметр пустой, назначаем случайное значение от 1 до 5
    if not sleep_value:
        seconds_wait = random.randint(1, 5)
    else:
        # Пробуем преобразовать параметр в число
        try:
            seconds_wait = int(sleep_value)
            if seconds_wait < 1:
                raise ValueError("Значение должно быть больше 0.")
        except ValueError:
            return "Параметр 'sleep' должен быть целым числом больше 0.", 400
# Ожидаем заданное количество секунд
    logger.info(f"{host_url} Aslept {seconds_wait} seconds")
    time.sleep(seconds_wait)
    return f"Ждали {seconds_wait} секунд."

#функция проверки доступности вызывается гет параметром /self-test
@app.route('/self-test', methods=['GET'])
def self_test():
    # Возвращаем статус 200 OK без проверки параметра
    return jsonify({"message": "Self-test successful"}), 200

# функция wait ожидание перед запуском
def wait(seconds):
    """Функция ожидания"""
    logger.info(f"Ожидание перед запуском {seconds} секунд...")
    time.sleep(seconds)
    logger.info("Ожидание завершено.")

# создаем endpoint для вывода информации от  kubernetes api
from flask import jsonify

@app.route('/kuber', methods=['GET'])
def get_service():
    label_selector = "service_type=flask-test-worker"
    logger.info("Получение сервисов с лейблом: %s", label_selector)
    services = v1.list_service_for_all_namespaces(label_selector=label_selector)
    logger.info("Количество сервисов, найденных: %d", len(services.items))
    
    try:
        service_list = []
        dns_names = []
        
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
            dns_name = f"http://{service.metadata.name}.default.svc.cluster.local:8080/sleep"
            dns_names.append(dns_name)
        
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
    
    return jsonify({'services': service_list, 'responses': response})
    
# функция считывания переменной окружения времени ожидания перед запуском, задается в окружении среды export STARTUP_DELAY_SECONDS=[seconds]
def main():
    # Считываем переменную окружения STARTUP_DELAY_SECONDS
    startup_delay = os.environ.get('STARTUP_DELAY_SECONDS')

    # Логируем значение ожидания
    logger.info(f"Значение ожидания: {startup_delay}")

    # Приводим значение переменной к целому числу, если оно определено, иначе используем 0
    if startup_delay is not None:
        try:
            delay_seconds = int(startup_delay)
            # Проверяем, что значение больше или равно 0
            if delay_seconds < 0:
                raise ValueError("Значение задержки не может быть отрицательным.")
        except ValueError as e:
            logger.info(f"Ошибка: {e}. Используем значение по умолчанию: 0.")
            delay_seconds = 0
    else:
        # Если переменная не задана, устанавливаем значение по умолчанию
        logger.info("Переменная окружения STARTUP_DELAY_SECONDS не найдена. Используем значение по умолчанию: 0.")
        delay_seconds = 0

    # Запускаем функцию ожидания
    wait(delay_seconds)
    app.run(host='0.0.0.0', port=8080, debug=False)
# Вызов функции main
if __name__ == '__main__':
    main()
