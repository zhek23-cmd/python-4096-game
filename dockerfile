# Используем официальный образ Python 3.10
FROM python:3.10-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл зависимостей (если есть)
COPY requirements.txt .

# Устанавливаем зависимости (если requirements.txt не пустой)
RUN pip install --no-cache-dir -r requirements.txt 2>/dev/null || echo "Нет зависимостей для установки"

# Копируем все файлы проекта
COPY . .

# Устанавливаем переменные окружения для корректной работы консоли
ENV PYTHONUNBUFFERED=1
ENV TERM=xterm-256color

# Делаем скрипт исполняемым
RUN chmod +x /app/main.py

# Запускаем игру
CMD ["python", "main.py"]