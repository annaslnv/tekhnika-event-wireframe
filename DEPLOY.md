# Выкладка сайта на сервер

Чтобы по ссылке (http://88.216.70.147) было видно **то же самое, что на localhost:8080**, нужны оба шага: загрузка файлов и настройка веб-сервера (Nginx). Подключение по SSH — см. **ИНСТРУКЦИЯ_ПОДКЛЮЧЕНИЕ.md** в корне проекта.

**Полный деплой с первого раза:** (1) создать каталог на сервере, (2) rsync — загрузить файлы, (3) скопировать и включить `nginx-tekhnika-event.conf`, перезагрузить nginx. Дальнейшие обновления — только rsync (шаг 2 уже выполнен).

## 1. Загрузка файлов на сервер

Из папки **над** `tekhnika-event-wireframe` (например, из `курсор`) выполните:

```bash
rsync -avz --delete -e "ssh -i ~/.ssh/id_rsa_server_88" \
  tekhnika-event-wireframe/ \
  root@88.216.70.147:/var/www/tekhnika-event/
```

- `--delete` — удаляет на сервере файлы, которых уже нет локально (сайт на сервере будет точной копией).
- Если в `~/.ssh/config` задан хост `server88`, можно короче:

```bash
rsync -avz --delete tekhnika-event-wireframe/ server88:/var/www/tekhnika-event/
```

Первый раз на сервере создайте каталог:

```bash
ssh -i ~/.ssh/id_rsa_server_88 root@88.216.70.147 "mkdir -p /var/www/tekhnika-event"
```

## 2. Настройка Nginx на 88.216.70.147

В проекте есть готовый конфиг **nginx-tekhnika-event.conf**. Чтобы сайт открывался по IP (как на localhost):

**Один раз на сервере** (или после смены сервера):

```bash
# Скопировать конфиг на сервер (из папки над tekhnika-event-wireframe):
scp -i ~/.ssh/id_rsa_server_88 tekhnika-event-wireframe/nginx-tekhnika-event.conf root@88.216.70.147:/etc/nginx/sites-available/tekhnika-event

# Подключиться и включить сайт:
ssh -i ~/.ssh/id_rsa_server_88 root@88.216.70.147
ln -sf /etc/nginx/sites-available/tekhnika-event /etc/nginx/sites-enabled/tekhnika-event
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx
exit
```

После этого сайт доступен по адресу **http://88.216.70.147** (то же содержимое, что на http://localhost:8080).

## 3. Обновление (чтобы на сервере всегда была последняя версия)

После любых правок в макете просто снова выполните команду `rsync` из шага 1 — на сервере окажется актуальная версия, доступная по вашей ссылке.
