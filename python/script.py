from flask import Flask, request, jsonify
from kubernetes import client, config
import random
import os
import time
import logging

# инициализация Flask
app = Flask(__name__)

# инициализация логгера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
@app.route('/kuber', methods=['GET'])
def get_services():
    # Загружаем конфигурацию, обычно она автоматически настраивается в рамках кластера
    config.load_incluster_config()

    # Создаем объект API для работы с серверами Kubernetes
    v1 = client.CoreV1Api()
    # Фильтруем сервисы по лейблу app_type: flask-test
    label_selector = "app_type=flask-test"
    
    try:
        # Получаем список всех сервисов с указанным лейблом
        services = v1.list_service_for_all_namespaces(label_selector=label_selector)
        
        # Подготавливаем данные к возврату
        #service_list = []
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
        # Возвращаем результаты в формате JSON
        return jsonify(service_list)
    
    except client.exceptions.ApiException as e:
        logger.error(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500   

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
