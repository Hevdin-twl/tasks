from flask import Flask, request
import time
import random

# Функция для ожидания одной минуты
def wait_one_minute():
    print("Ожидание 1 минуты перед запуском...")
    time.sleep(60)  # Ожидание 60 секунд
    print("Продолжение работы приложения.")
wait_one_minute()

# Создание экземпляра приложения Flask
app = Flask(__name__)

# Определение случайного значения переменной в диапазоне от 1 до 5
def rand_sec(): 
   return random.randint(1, 5)

# Определение маршрута для корневого URL
#@app.route('/')
#def hello_world():
#    return 'Hello World'
# Получение GET параметра sleep
@app.route('/sleep/<seconds>')
def sleep(seconds):
   return time.sleep(seconds)
   print("HOSTNAME Aslept: {seconds} seconds")
# если параметр sleep пустой то устанавливает случайное значение в диапазоне 1-5
if sleep(seconds) is None:
   wait_time = rand_sec()
   time.sleep(wait_time)
   print("HOSTNAME Aslept: {wait_time} seconds")


# Запуск сервера
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
