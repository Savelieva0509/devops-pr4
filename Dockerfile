# Базовий образ: легкий Linux з Python 3.12
FROM python:3.12-slim

# Python не створює зайві .pyc-файли й одразу показує логи
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Робоча папка всередині контейнера
WORKDIR /app

# Спочатку тільки список бібліотек: так Docker швидше перезбирає образ
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Тепер увесь код сайту
COPY . .

# Сайт працює на порту 8000
EXPOSE 8000

# Що робити при запуску контейнера
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:8000"]