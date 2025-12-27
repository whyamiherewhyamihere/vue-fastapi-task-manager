# Task Manager (Vue 3 + FastAPI)

Мини-приложение «Менеджер задач».

Репозиторий: https://github.com/whyamiherewhyamihere/vue-fastapi-task-manager

## Структура

- `frontend/` — Vue 3 (Vite) + Vue Router
- `backend/` — FastAPI + SQLite
- `docker-compose.yml` — запуск фронта и бэка

## Запуск через Docker

```bash
docker compose build
docker compose up
```

- Frontend: http://localhost:8080
- Backend: http://localhost:8000
- Проверка API: http://localhost:8000/api/health

Данные сохраняются в томе `tasks_data` (SQLite `tasks.db`).

## Запуск в режиме разработки (без Docker)

### Backend

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Vite-прокси настроен на `http://localhost:8000` для запросов `/api/*`.
