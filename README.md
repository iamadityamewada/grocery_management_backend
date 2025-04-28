# GroceryWise FastAPI Backend

This directory contains the FastAPI backend for the GroceryWise application.

## Setup

1.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment Variables:**
    - Copy the `.env.example` file to `.env`:
      ```bash
      cp .env.example .env
      ```
    - **Generate a `SECRET_KEY`:** Run `openssl rand -hex 32` in your terminal and paste the output into the `.env` file for the `SECRET_KEY` variable. This is crucial for security.
    - Review other variables in `.env` (like `DATABASE_URL` if you want to use a different database name or location).

4.  **Database Migrations:**
    - Initialize the database using Alembic:
      ```bash
      alembic upgrade head
      ```
    - This command reads the models defined in `app/models/models.py` and creates the corresponding tables in the SQLite database specified by `DATABASE_URL` in your `.env` file (default: `sql_app.db`).
    - If you make changes to your SQLAlchemy models in the future, you'll need to generate a new migration:
      ```bash
      alembic revision --autogenerate -m "Describe your changes here"
      ```
    - Then apply the migration:
      ```bash
      alembic upgrade head
      ```

## Running the Backend

1.  **Start the FastAPI server:**
    ```bash
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```
    - `--reload`: Automatically restarts the server when code changes are detected (useful for development).
    - `--host 0.0.0.0`: Makes the server accessible from your local network (and the Next.js frontend running in its container or locally).
    - `--port 8000`: The port the server will listen on.

2.  **Access the API Docs:**
    Once the server is running, open your web browser and navigate to:
    - **Swagger UI:** [http://localhost:8000/api/v1/docs](http://localhost:8000/api/v1/docs)
    - **ReDoc:** [http://localhost:8000/api/v1/redoc](http://localhost:8000/api/v1/redoc)
    These interfaces allow you to interactively explore and test the API endpoints.

## Project Structure

-   `alembic/`: Contains database migration scripts and configuration.
-   `app/`: Main application code.
    -   `api/`: API endpoint definitions.
        -   `deps.py`: Dependency injection functions (e.g., getting current user).
        -   `v1/`: Version 1 of the API.
            -   `endpoints/`: Specific resource endpoints (auth, users, groceries).
            -   `api.py`: Aggregates all v1 routers.
    -   `core/`: Core components like configuration and database setup.
    -   `crud/`: CRUD (Create, Read, Update, Delete) database operations.
    -   `models/`: SQLAlchemy database models.
    -   `schemas/`: Pydantic data validation schemas.
    -   `main.py`: FastAPI application entry point.
-   `.env`: Environment variables (ignored by git).
-   `.env.example`: Example environment variables.
-   `alembic.ini`: Alembic configuration.
-   `requirements.txt`: Python dependencies.
-   `sql_app.db`: SQLite database file (created after running migrations, ignored by git).
-   `README.md`: This file.

## Next Steps for Frontend Integration

1.  **Update Frontend API URL:** Ensure the `NEXT_PUBLIC_API_URL` in the frontend's `.env` file (or environment variables) points to the correct backend address (e.g., `http://localhost:8000`).
2.  **Implement Frontend API Calls:** Replace the mock API calls in `src/lib/api.ts` with actual `fetch` calls to the FastAPI endpoints defined here.
3.  **Handle Authentication Flow:** Ensure the frontend correctly stores the JWT token received upon login and sends it in the `Authorization: Bearer <token>` header for protected requests. Manage token expiration and refresh logic if needed.
4.  **Error Handling:** Implement robust error handling in the frontend to display meaningful messages based on API responses (e.g., "Invalid credentials", "Item not found").
