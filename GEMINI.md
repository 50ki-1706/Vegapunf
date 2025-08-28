# GEMINI.md

## Project Overview

This is a full-stack web application with a Python [FastAPI](https://fastapi.tiangolo.com/) backend and a [React](https://react.dev/) frontend. The frontend is built with [Vite](https://vitejs.dev/) and uses [axios](https://axios-http.com/) for making HTTP requests to the backend.

The project is structured into two main directories:
- `backend`: Contains the FastAPI application.
- `frontend`: Contains the React application.

## Building and Running

### Backend

1.  **Navigate to the backend directory:**
    ```bash
    cd backend/
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the development server:**
    ```bash
    uvicorn main:app --reload
    ```
    The backend will be running at `http://127.0.0.1:8000`.

### Frontend

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend/
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```
3.  **Run the development server:**
    ```bash
    npm run dev
    ```
    The frontend will be running at `http://localhost:5173`.

## Development Conventions

### Frontend

- The frontend code is linted with [ESLint](https://eslint.org/). You can run the linter with `npm run lint`.
