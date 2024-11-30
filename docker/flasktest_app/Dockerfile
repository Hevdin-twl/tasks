# Выкачиваем из dockerhub образ с python версии 3.9
FROM python:3.13.0
# Устанавливаем рабочую директорию для конфигурации среды
WORKDIR /backend
# Скачиваем/обновляем необходимые библиотеки для проекта 
COPY requirements.txt /backend
RUN pip3 install --upgrade pip -r requirements.txt
# копируем содержимое папки, где находится Dockerfile, в рабочую директорию контейнера
COPY . /backend
# Устанавливаем порт, который будет использоваться для сервера
EXPOSE 8080
# установка рабочий директориии приложения
WORKDIR /python
# копируем приложение
COPY . ../../python
# Запускаем приложение
CMD ["python3", "-u", "./script.py"]
