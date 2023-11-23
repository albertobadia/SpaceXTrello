# Trello Task Manager API

## Overview

Welcome to the Trello Task Manager API, a Python application built with FastAPI that seamlessly integrates with Trello for efficient task management. This API empowers users to effortlessly create and manage tasks through a straightforward interface.

## Getting Started

Before running the application, ensure you have Docker and Docker Compose installed. Create a `.env` file with the required keys:

```env
SECRET_KEY=YourSecretKey
TRELLO_API_KEY=YourTrelloApiKey
```

**Generating the SECRET_KEY:**

For enhanced security, generate a robust `SECRET_KEY` using the following Python code:

```bash
python -c "import secrets; print(secrets.token_urlsafe())"
```

Replace `YourSecretKey` in the `.env` file with the generated key.

**Creating a Trello Power-Up and Obtaining TRELLO_API_KEY:**

1. Visit the [Trello Developer Portal](https://developer.atlassian.com/cloud/trello/).

2. Click "Get Started" and log in with your Trello account.

3. Create a new Power-Up, configure it to suit your project's needs, and find the `TRELLO_API_KEY` on the Power-Up settings page. Copy this key and replace `YourTrelloApiKey` in the `.env` file.

## Running with Docker

```bash
docker-compose up --build
```

## Quick Start

1. **User Registration and Authentication in the API:**

   - Register with the local API using the `POST /users/register/` endpoint with the `username` and `password` fields. Example:
     ```json
     {"username": "YourUser", "password": "YourPassword"}
     ```

   - Log in to the local API using the `POST /users/login/` endpoint with the same fields. This generates a JWT token for authentication. Example:
     ```json
     {"username": "YourUser", "password": "YourPassword"}
     ```

2. **Trello Registration and Authorization:**

   - Obtain the Trello authorization URL at `/trello/auth_url/`. Open this URL, acquire the authorization token, and associate it with your API user at `/trello/set_token/` using a POST request with the "token" field. Example:
     ```json
     {"token": "YourTrelloToken"}
     ```

3. **Task Creation:**

   - Create tasks using the `POST /tasks/` route with the request body, including the "type" field with its respective type and the corresponding parameters. Below are the required parameters for each type:

     - **ISSUE:**
       ```json
       {"type": "ISSUE", "title": "Title", "description": "Description"}
       ```

     - **BUG:**
       ```json
       {"type": "BUG", "description": "Description"}
       ```

     - **TASK:**
       ```json
       {"type": "TASK", "title": "Title", "category": "Category"}
       ```

## OpenAPI Documentation

Explore the OpenAPI documentation at `/docs/` for detailed information on available endpoints and how to interact with the API.
