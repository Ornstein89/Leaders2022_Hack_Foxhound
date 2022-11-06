[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![GitHub contributors](https://img.shields.io/github/contributors/Ornstein89/VTB_API_hack2022)

# Leaders2022_Hack_Foxhound
Решение команды Foxhound на хакатоне "Лидеры цифровой трансформации 2022"

# Инструкция по запуску
Демо решение расположено по адресу [158.160.36.137](http://158.160.36.137)


Для запуска локально, см. [Развертывание через docker-compose](#развертывание-через-docker-compose)

# Развертывание через docker-compose
1. Установить [docker](https://docs.docker.com/engine/install/ubuntu/)
2. В папке compose создать файл .env и [заполнить](#описание-переменных-окружения) его в соответствии с примерами
3. Запустить команду docker compose up -d с правами суперпользователя
```bash
sudo docker compose up -d
```
5. Настроить внешний nginx, который будет пересылать все запросы на порт приложения

# Описание переменных окружения

## HTTP_PORT
Файлы: .env

Тип: целое число

Назначение: порт на котором будет крутиться приложение

## BROKER_PASS
Файлы: .env

Тип: строка

Назначение: пароль для rabbitmq

## BROKER_USER
Файлы: .env

Тип: строка

Назначение: имя пользователя для rabbitmq (можно указать user)

# Команды docker-compose 
Все команды необходимо выполнять в папке compose
- Остановить все контейнеры
```bash
sudo docker-compose stop
```
- Перезапустить контейнер
```bash
sudo docker-compose restart {container_name}
```
- Запуск ipython
```bash
sudo docker-compose exec backend ipython
```

