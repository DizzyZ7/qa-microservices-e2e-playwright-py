# E2E тестирование микросервисов (API → UI → DB) на Playwright + Pytest

Этот репозиторий показывает современный подход QA Automation (2026):
- Подготовка тестовых данных через API (Playwright APIRequestContext)
- Проверка отображения в UI (Playwright браузер)
- Валидация состояния в БД (SQLAlchemy/psycopg2)
- Изоляция тестов через cleanup фикстуры
- Allure отчеты + публикация в GitHub Pages
- Trace Viewer артефакты при падениях
- Docker: запуск одной командой

## Быстрый старт (Docker)
```bash
docker-compose up --build --exit-code-from tests

1. Локальный запуск (без Docker)

Подними Postgres и приложение: 
docker-compose up --build db app

2. Установи зависимости:

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install --with-deps


3. Запусти тесты:

pytest

Allure

После прогона:
allure serve allure-results

Trace Viewer
При падении теста trace сохраняется в artifacts/traces/*.zip.
Открыть:

npx playwright show-trace artifacts/traces/<file>.zip
