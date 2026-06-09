Инструкция по запуску приложения

0. Войти под root или добавить пользователя в группу Docker
1. Склонировать репозиторий на ОС Debian или Ubuntu с установленным Docker и Docker Compose git clone https://github.com/aleksandrkpz/kr_trpo
2. Перейти в папку kr_trpo
3. Выполнить команду docker compose up -d
4. Дождаться завершения запуска контейнеров
5. Выполнить миграции:
docker compose exec -T main python manage.py migrate
docker compose exec -T input python manage.py migrate
docker compose exec -T stat python manage.py migrate

6. Откройте браузер:

   а) Если запускаете на локальной машине:
     http://localhost

   б) Если запускаете на виртуальной машине VirtualBox + NAT:
     Настройте проброс портов (Порт гостя 80, порт хоста 8080) и откройте:
     http://localhost:8080

   в) Если запускаете на удалённом сервере или VirtualBox + Сетвой мост:
     Узнайте IP командой: ip a
     Откройте: http://<IP-адрес>
