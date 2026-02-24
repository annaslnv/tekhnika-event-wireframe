#!/bin/bash
# Запуск локального сервера для просмотра сайта
# Открой в браузере: http://localhost:8080

cd "$(dirname "$0")"
echo "Сервер запущен. Открой в браузере: http://localhost:8080"
echo "Остановка: Ctrl+C"
python3 -m http.server 8080
