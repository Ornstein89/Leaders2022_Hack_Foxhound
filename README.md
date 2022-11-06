[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![GitHub contributors](https://img.shields.io/github/contributors/Ornstein89/VTB_API_hack2022)

# Leaders2022_Hack_Foxhound
Решение команды Foxhound на хакатоне "Лидеры цифровой трансформации 2022"


Управление |  Просмотр и разметка | Генерация
--- | --- | ---
![image](https://user-images.githubusercontent.com/26321368/200194372-6b0f8b56-dc9e-4c5f-a1c3-19ed21fcd327.png) | ![image](https://user-images.githubusercontent.com/26321368/200194825-3740e0ec-3ace-4e76-ad42-e575b9f8e7bf.png) | ![image](https://user-images.githubusercontent.com/26321368/200194776-b6e852b7-0950-411c-923d-e1deacd0dd4b.png)


# Инструкция по запуску

Демо решение расположено по адресу [158.160.36.137](http://158.160.36.137)
Документация OpenAPI по адресу [158.160.36.137/docs](http://158.160.36.137/docs)
Для запуска локально, см. [Развертывание через docker-compose](#развертывание-через-docker-compose)

# Развертывание через docker-compose
1. Установить [docker](https://docs.docker.com/engine/install/ubuntu/)
2. В папке compose создать файл .env и [заполнить](#описание-переменных-окружения) его в соответствии с примерами
3. Запустить команду docker compose up -d с правами суперпользователя
```bash
sudo docker compose up -d
```
5. Настроить внешний nginx, который будет пересылать все запросы на порт приложения

# Структура репозитория

1. `/ML_Denis` - исходный код и демонстрационный jupyter notebook генератора №2 (U-Net, CGAN)
2. `/backend` - исходный код сервера
3. `/compose` - файлы docker compose для автоматического развёртывания в контейнерах
4. `/frontend` - исходный код фронтенда на Vue и JS
5. `/generator_simple` - исходный код и демонстрационный jupyter notebook генератора №1 (алгоритмический случайный гладкий контур с размытием случайным Гауссовым полем)
6. `/models` - исходный код и демонстрационный jupyter notebook генератора №3
7. `/previewer` - исходный код модуля для генерации предпросмотра DICOM в формате PNG при загрузке

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

