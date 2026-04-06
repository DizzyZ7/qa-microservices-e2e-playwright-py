# 🧪 E2E Automation Framework (API → UI → DB)
**Playwright + Pytest | Microservices Testing | 2026-ready**

Этот репозиторий демонстрирует современный подход к автоматизации тестирования микросервисов:
не просто UI-клики, а **сквозная проверка всей цепочки данных** — от API до базы данных.

Проект ориентирован на практики, которые ожидаются от **QA Automation Engineer уровня Middle+/Senior**.

---

## 🚀 Ключевые возможности

- ✅ **End-to-End сценарии (API → UI → DB)**
- ⚡ Подготовка тестовых данных через **Playwright APIRequestContext**
- 🧱 **Page Object Model (POM)** для UI-тестов
- 🗄 Проверка состояния данных напрямую в **PostgreSQL**
- 🧹 Изоляция тестов и автоматический **cleanup**
- 📊 **Allure Reports** с публикацией в GitHub Pages
- 🕵️ **Playwright Trace Viewer** при падениях тестов
- 🐳 **Docker & docker-compose** — запуск одной командой
- 🤖 **CI/CD (GitHub Actions)**

---

## 🧩 Архитектура проекта

```text
project-root/
├── app/                    # Демонстрационный микросервис (FastAPI + HTML)
├── core/                   # API клиенты, DB helpers, настройки
├── pages/                  # Page Object Model
├── tests/
│   ├── api/                # API тесты
│   └── ui/                 # UI + E2E тесты
├── artifacts/              # traces / screenshots / videos
├── .github/workflows/      # CI/CD pipeline
├── docker-compose.yml
├── Dockerfile              # Docker-образ для тестов
├── pytest.ini
└── requirements.txt
```

## ⚙️ Локальный запуск

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
playwright install
```

Если нужны локальные переопределения окружения, создай `.env` на основе `.env.example`.

Для запуска приложения и БД через Docker:

```bash
docker compose up --build
```

Для запуска тестов локально:

```bash
pytest -m "api or ui"
```

## ✅ Что покрыто тестами

- healthcheck сервиса
- создание заказа через API с проверкой состояния в PostgreSQL
- обработка заказа через API и UI
- отображение статуса заказа в UI
- ошибка логина при невалидных данных
