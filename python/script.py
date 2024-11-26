from flask import Flask, request, jsonify
import random
import time

app = Flask(__name__)

#функция ожидания прнимает параметр GET sleep?sleep=[значение]
@app.route('/sleep', methods=['GET'])

def sleep_route():
    # Получаем GET параметр 'sleep'
    host_url = request.host_url
    sleep_value = request.args.get('sleep')

    # Если параметр пустой, назначаем случайное значение от 1 до 5
    if not sleep_value:
        seconds = random.randint(1, 5)
    else:
        # Пробуем преобразовать параметр в число
        try:
            seconds = int(sleep_value)
            if seconds < 1:
                raise ValueError("Значение должно быть больше 0.")
        except ValueError:
            return "Параметр 'sleep' должен быть целым числом больше 0.", 400
# Ожидаем заданное количество секунд
    print(f"{host_url} Aslept {seconds} seconds")
    time.sleep(seconds)
    return f"Ждали {seconds} секунд."

# функция тестирования прнимает параметр GET self-test?self-test=true
@app.route('/self-test', methods=['GET'])
def self_test():
    # Получение GET параметра
    param = request.args.get('self-test')

    # Проверка наличия параметра
    if param is not None:
        # Возвращаем статус 200 OK
        return jsonify({"message": "Self-test successful"}), 200
    else:
        # Возвращаем ошибку 400 Bad Request, если параметр отсутствует
        return jsonify({"error": "Missing self-test parameter"}), 400



#if __name__ == '__main__':
#    app.run(debug=True)
# Запуск сервера
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

