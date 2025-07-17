# 🧠 SmartTaskAnalytics

**SmartTaskAnalytics** — это микросервисное веб-приложение для умного управления задачами с расширенной системой тегов, аутентификацией и возможностью дальнейшего расширения аналитическими инструментами.  

Проект разработан в архитектуре **микросервисов**, каждый из которых выполняет чётко определённую функцию — от управления пользователями до сбора статистики по задачам. Используются современные технологии: **FastAPI**, **PostgreSQL**, **JWT**, **Docker** и др.

---

## 🚀 Возможности

- 🔐 Безопасная регистрация и аутентификация пользователей (JWT)
- 📋 CRUD-интерфейс для управления задачами
- 🏷️ Система тегов и приоритетов
- ⏰ Поддержка дедлайнов и статусов выполнения
- 📊 Гибкое масштабирование с использованием микросервисной архитектуры
- 🧠 (В разработке) Аналитика по выполненным задачам, приоритетам, дедлайнам

---

## 🧰 Используемые технологии

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.116.1.0-0e7c61?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red?logo=python)
![Alembic](https://img.shields.io/badge/Alembic-Migrations-446e9b)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ed?logo=docker)
![Pytest](https://img.shields.io/badge/Pytest-Testing-blue?logo=pytest)
![AsyncIO](https://img.shields.io/badge/Async-Awaitable-green)

---

## 📦 Сервисы проекта

| Сервис | Назначение | Порт |
|--------|------------|------|
| [`auth-service`](./auth_service) | Аутентификация и управление пользователями | `8000` |
| [`task-service`](./task_service) | Управление задачами и тегами | `8888` |
| [`analytics-service`](./analytics_service) | Статистика и аналитика по задачам *(в разработке)* | `8002` |

---

## 📂 Структура проекта
```
SmartTaskAnalytics/
├── auth_service/
│ └── src/
├── task_service/
│ └── src/
└─analytics_service/
  └── src/ (в разработке)
```

-----

## 🏁 Быстрый старт
### 1. Клонирование
```bash git clone https://github.com/your-username/SmartTaskAnalytics.git cd SmartTaskAnalytics```

### 2. Установка и запуск auth-service
```
cd /auth_service
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```
### 3. Установка и запуск task-service
```
cd ../task_service
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

### 4. Настрой переменные окружения
Не забудь указать свои перененные для баз данных и т.п. в файлах .env.


