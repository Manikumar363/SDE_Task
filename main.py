from fastapi import FastAPI, HTTPException, Query, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from database import employees_collection
from models import Employee, UpdateEmployee

app = FastAPI()

# JWT Auth setup
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# Dummy user for demonstration
fake_user = {
    "username": "admin",
    "hashed_password": pwd_context.hash("admin123")
}

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str):
    if username == fake_user["username"] and verify_password(password, fake_user["hashed_password"]):
        return {"username": username}
    return None

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    if username != fake_user["username"]:
        raise credentials_exception
    return {"username": username}

# Authentication part
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

# --------- CRUD ---------

@app.post("/employees")
def create_employee(employee: Employee, user: dict = Depends(get_current_user)):
    data = employee.dict()
    data["joining_date"] = employee.joining_date.isoformat()  # convert to string
    if employees_collection.find_one({"employee_id": employee.employee_id}):
        raise HTTPException(status_code=400, detail="Employee ID already exists")
    employees_collection.insert_one(data)
    return {"message": "Employee created successfully"}


# --------- Querying ---------

@app.get("/employees/avg-salary")
def average_salary():
    pipeline = [
        {"$group": {"_id": "$department", "avg_salary": {"$avg": "$salary"}}},
        {"$project": {"department": "$_id", "avg_salary": 1, "_id": 0}}
    ]
    return list(employees_collection.aggregate(pipeline))

@app.get("/employees/search")
def search_by_skill(skill: str):
    data = list(employees_collection.find({"skills": skill}, {"_id": 0}))
    return data

@app.get("/employees/{employee_id}")
def get_employee(employee_id: str):
    emp = employees_collection.find_one({"employee_id": employee_id}, {"_id": 0})
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp

@app.put("/employees/{employee_id}")
def update_employee(employee_id: str, updates: UpdateEmployee, user: dict = Depends(get_current_user)):
    upd = {k: v for k, v in updates.dict().items() if v is not None}
    if "joining_date" in upd:
        upd["joining_date"] = upd["joining_date"].isoformat()
    result = employees_collection.update_one({"employee_id": employee_id}, {"$set": upd})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee updated successfully"}

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: str, user: dict = Depends(get_current_user)):
    result = employees_collection.delete_one({"employee_id": employee_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted successfully"}

# --------- Querying ---------

@app.get("/employees")
def list_by_department(
    department: str = Query(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    cursor = employees_collection.find({"department": department}, {"_id": 0}).sort("joining_date", -1).skip(skip).limit(limit)
    data = list(cursor)
    return data

@app.get("/employees/avg-salary")
def average_salary():
    pipeline = [
        {"$group": {"_id": "$department", "avg_salary": {"$avg": "$salary"}}},
        {"$project": {"department": "$_id", "avg_salary": 1, "_id": 0}}
    ]
    return list(employees_collection.aggregate(pipeline))

@app.get("/employees/search")
def search_by_skill(skill: str):
    data = list(employees_collection.find({"skills": skill}, {"_id": 0}))
    return data
