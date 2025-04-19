# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем Node.js
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt package*.json ./

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt
RUN npm install

# Копируем исходный код
COPY . .

# Собираем фронтенд
RUN npm run build

# Открываем порт
EXPOSE 5000

# Запускаем приложение
CMD ["python", "app.py"] 