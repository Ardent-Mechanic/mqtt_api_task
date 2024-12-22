#  **Mqtt Api**

Welcome to the **Mqtt Api** repository! This project leverages modern technologies to deliver robust, scalable, and efficient solutions. Below, you'll find all the essential details to get started and contribute effectively.

---

## 🌟 **Technologies Used**

| Technology   | Purpose                                      |
|--------------|----------------------------------------------|
| **Pipenv**   | Virtual environment and dependency management |
| **FastAPI**  | High-performance web framework for APIs      |
| **Alembic**  | Database migrations tool                     |
| **PostgreSQL** | Powerful relational database system          |
| **Logging**  | Application-wide logging and debugging        |
| **FastMQTT** | MQTT integration for real-time communication |

---

## 🛠️ **Setup Instructions**

### Prerequisites

Ensure you have the following installed:
- Python 3.12
- Pipenv
- PostgreSQL

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/project-name.git
   cd project-name
   ```

2. Create and activate a virtual environment using Pipenv:
   ```bash
   pipenv install --dev
   pipenv shell
   ```

3. Set up your `.env` file:
   ```env
   APP_CONFIG__DB__URL=postgresql+asyncpg://<user>:<password>@<host>:<port>/<database>
   APP_CONFIG__DB__ECHO=<0/1>

   APP_CONFIG__MQTT__HOST=host
   APP_CONFIG__MQTT__PORT=port
   APP_CONFIG__MQTT__TOPIC=topic
   ```
   
4. Before applying migrations, make sure the database exists. You can create the database manually using the following command:
   ```bash
   psql -U <user> -h <host> -p <port> -c "CREATE DATABASE <database>;"
   ```

5. Apply database migrations:
   ```bash
   alembic upgrade head
   ```

6. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

---

## 🔑 **Key Features**

- 🚀 **FastAPI-powered API** for blazing-fast performance.
- 🔄 **Alembic** for seamless database migrations.
- 💾 **PostgreSQL** for reliable data persistence.
- ⚡ **FastMQTT** for real-time messaging and IoT integrations.
- 📋 **Logging** to keep track of application health and performance.

---

## 🗂️ **Project Structure**

```
project-name/
├── api/                # Обработчики маршрутов и API логика
│   └── api_v1/         # Версионированные эндпоинты API (v1)
├── core/               # Основная бизнес-логика и настройки приложения
├── crud/               # CRUD-операции для работы с базой данных
├── db/                 # Настройки базы данных и модели
├── logs/               # Логи приложения
├── migrations/         # Скрипты миграций для Alembic
├── model/              # Определения моделей базы данных
├── schemas/            # Pydantic-схемы для валидации данных
├── utils/              # Утилиты и mqtt клиент
├── tests/              # Тесты для приложения
├── .example.env        # Пример файла окружения с настройками
├── alembic.ini         # Конфигурация Alembic для миграций
├── logging.conf        # Конфигурация логирования приложения
├── Pipfile             # Управление зависимостями через Pipenv
├── Pipfile.lock        # Зафиксированные версии зависимостей
└── main.py             # Основной файл
```