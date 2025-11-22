# AASKbot_3.0

## Сборка проекта

1. Создаем окружения
2. Устанавливаем пакеты (poetry install)

## Первый запуск

Все сервисы описаны в ```docker-compose.yml```

1. Необходимо поднять все контейнеры кроме ``app``
2. Применить миграции через
   ```alembic upgrade head```
3. Запуск проекта через ``python3 main.py``

## Работа на базе репозитория
Установить хуки:
```bash
pre-commit install
```
Выполнить проверку всех файлов:
```bash
pre-commit run --all-files
```

## Добавление новых таблиц в БД через миграции alembic
* Описать модели в /models
* ``alembic revision -m "migration message" --autogenerate``
* Проверить новую версию и применить её ``alembic upgrade head``

