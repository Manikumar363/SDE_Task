# Employee Management API (FastAPI + MongoDB)

A RESTful API for employee management using FastAPI and MongoDB (Atlas or local). Supports CRUD, advanced queries, pagination, schema validation, and JWT authentication.

## Features

- Create, read, update, delete employees
- List employees by department (with pagination)
- Search employees by skill
- Get average salary by department
- MongoDB JSON schema validation
- Unique index on `employee_id`
- JWT authentication for protected routes

## Requirements

- Python 3.8+
- MongoDB (Atlas or local)

## Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd sde_task
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure environment variables:**

   - Edit `.env` file:
     ```env
     MONGO_URI=<your-mongodb-uri>
     DB_NAME=assessment_db
     ```
   - For MongoDB Atlas, use the connection string from your cluster.
   - For local MongoDB, use `mongodb://localhost:27017`.

4. **Run the app:**
   ```bash
   uvicorn main:app --reload
   ```
   The API will be available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Authentication

- Obtain a JWT token via `/token` endpoint:
  - username: `admin`
  - password: `admin123`
- Use the token as a Bearer token for protected endpoints (POST, PUT, DELETE /employees).

## Example Employee JSON

```json
{
  "employee_id": "E001",
  "name": "John Doe",
  "department": "Engineering",
  "salary": 75000,
  "joining_date": "2023-01-15",
  "skills": ["Python", "MongoDB", "APIs"]
}
```

## Endpoints

- `POST /employees` (protected)
- `GET /employees/{employee_id}`
- `PUT /employees/{employee_id}` (protected)
- `DELETE /employees/{employee_id}` (protected)
- `GET /employees?department=...&skip=0&limit=10`
- `GET /employees/avg-salary`
- `GET /employees/search?skill=...`

## Notes

- Ensure your MongoDB server is running and accessible.
- For Atlas, whitelist your IP in the cluster's Network Access settings.
- All data validation is enforced via Pydantic and MongoDB JSON Schema.

---

Feel free to fork, modify, and use for your own projects!
