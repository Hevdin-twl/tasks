# Выкачиваем из dockerhub образ с python
FROM python:3.11.0
# Устанавливаем рабочую директорию для конфигурации среды
WORKDIR /backend
# Скачиваем/обновляем необходимые библиотеки для проекта 
COPY requirements.txt /backend
RUN pip3 install --upgrade pip -r requirements.txt
# копируем содержимое папки, где находится Dockerfile, в рабочую директорию контейнера
COPY . /backend
# Устанавливаем порт, который будет использоваться для сервера
EXPOSE 8080
# Запускаем приложение
CMD ["python3", "-u", "script.py"]
