# QA Microservices E2E Framework

End-to-end automation framework that validates a complete **API → UI → PostgreSQL** data flow instead of testing each layer in isolation.

The repository includes a small FastAPI application and a test suite built with Pytest and Playwright. Test data is created through the API, verified in the browser, checked directly in PostgreSQL and removed automatically after execution.

## What the project demonstrates

- API, UI, database and end-to-end testing;
- test-data preparation through Playwright `APIRequestContext`;
- Page Object Model for maintainable browser tests;
- direct PostgreSQL validation;
- fixtures, parametrization and isolated cleanup;
- traces, screenshots and videos for failed scenarios;
- Allure reporting;
- Docker-based local environment;
- automated execution with GitHub Actions.

## Tested flow

```text
Test setup
    |
    v
Create order through API
    |
    v
Validate record in PostgreSQL
    |
    v
Process order through API / UI
    |
    v
Verify final status in UI and database
    |
    v
Automatic cleanup
```

## Project structure

```text
project-root/
├── app/                    # Demo service: FastAPI + HTML
├── core/                   # API clients, DB helpers and configuration
├── pages/                  # Page Object Model
├── tests/
│   ├── api/                # API tests
│   └── ui/                 # UI and E2E tests
├── artifacts/              # Traces, screenshots and videos
├── .github/workflows/      # CI pipeline
├── docker-compose.yml
├── Dockerfile
├── pytest.ini
└── requirements.txt
```

## Covered scenarios

- service health check;
- order creation through REST API;
- database-state verification in PostgreSQL;
- order processing through API and UI;
- order-status rendering in the browser;
- negative login scenario with invalid credentials.

## Tech stack

- Python
- Pytest
- Playwright
- FastAPI
- PostgreSQL
- Docker / Docker Compose
- Allure
- GitHub Actions

## Local setup

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\activate
```

Linux / macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
playwright install
```

Create `.env` from `.env.example` when local overrides are needed.

Start the demo application and database:

```bash
docker compose up --build
```

Run API and UI tests:

```bash
pytest -m "api or ui"
```

## Engineering focus

The framework is designed around verifiable state transitions across service boundaries. A successful HTTP response alone is not treated as sufficient evidence: tests confirm that the expected data reaches PostgreSQL and is displayed correctly in the UI.

## Author

**Dimash Janibekov**  
Python Backend / QA Automation Engineer

- GitHub: [DizzyZ7](https://github.com/DizzyZ7)
- Telegram: [@dizzy_dev](https://t.me/dizzy_dev)
- Portfolio: [DizZy Systems Atlas](https://dizzyz7.github.io/DizZy-Systems-Atlas/)