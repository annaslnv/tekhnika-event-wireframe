# Выкладка сайта на сервер

Чтобы актуальная версия сайта была доступна по ссылке, загрузите содержимое этой папки на сервер. Подключение по SSH — см. **ИНСТРУКЦИЯ_ПОДКЛЮЧЕНИЕ.md** в корне проекта.

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

## 2. Настройка веб-сервера на 88.216.70.147

Чтобы сайт открывался по домену или по IP:

- **Nginx** — в конфиге сайта укажите `root /var/www/tekhnika-event;` и при необходимости `index index.html; try_files $uri $uri/ /index.html;` для удобной работы с путями вроде `/meropriyatiya/`.
- **Apache** — укажите `DocumentRoot /var/www/tekhnika-event` и включите `AllowOverride All` для `.htaccess`, если будете использовать перезапись URL.

После изменения конфига перезапустите веб-сервер (например, `systemctl reload nginx`).

## 3. Обновление (чтобы на сервере всегда была последняя версия)

После любых правок в макете просто снова выполните команду `rsync` из шага 1 — на сервере окажется актуальная версия, доступная по вашей ссылке.
