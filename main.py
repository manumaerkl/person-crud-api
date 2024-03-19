from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from database import SessionLocal, engine
import models

# Creates all tables in the database
models.Base.metadata.create_all(bind=engine)

# Pydantic model for a person
class Person(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    age: int

    @validator('age')
    def validate_age(cls, v):
        if v < 1:
            raise ValueError('Age must be a positive integer')
        return v

# Pydantic model for updating a person
class UpdatePerson(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None

    @validator('age')
    def validate_age(cls, v):
        if v is not None and v < 1:
            raise ValueError('Age must be a positive integer')
        return v


app = FastAPI()

# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "Welcome to CRUD API for Managing Person Records!",
        "docs": "You can find the API documentation and test the endpoints at http://localhost:8000/docs",
        "info": "This API allows you to perform CRUD operations on person records. Each person has a first name, last name, email, and age.",
        "endpoints": {
            "POST /people/": "Adds a new person to the database.",
            "GET /people/{person_id}": "Retrieves the details of a person based on the provided person_id.",
            "PUT /people/{person_id}": "Updates the specified fields of a person record.",
            "DELETE /people/{person_id}": "Deletes the person record corresponding to the person_id."
        }
    }

# Endpoint for creating a person
@app.post("/people/")
def create_person(person: Person):
    db = SessionLocal()
    db_person = db.query(models.Person).filter(models.Person.email == person.email).first()
    if db_person is not None:
        raise HTTPException(status_code=400, detail="Email address already used by another person")
    db_person = models.Person(first_name=person.first_name, last_name=person.last_name, email=person.email, age=person.age)
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    db.close()
    return db_person

# Entpoint for retrieving a person
@app.get("/people/{person_id}")
def read_person(person_id: int):
    db = SessionLocal()
    db_person = db.query(models.Person).filter(models.Person.id == person_id).first()
    db.close()
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person

# Endpoint for updating a person
@app.put("/people/{person_id}")
def update_person(person_id: int, person: UpdatePerson):
    db = SessionLocal()
    if person.email is not None:
        db_person = db.query(models.Person).filter(models.Person.email == person.email).first()
        if db_person is not None:
            raise HTTPException(status_code=400, detail="Email address already used by another person")
    db_person = db.query(models.Person).filter(models.Person.id == person_id).first()
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    for var, value in vars(person).items():
        setattr(db_person, var, value) if value else None
    db.commit()
    db.refresh(db_person)
    db.close()
    return db_person

# Endpoint for deleting a person
@app.delete("/people/{person_id}")
def delete_person(person_id: int):
    db = SessionLocal()
    db_person = db.query(models.Person).filter(models.Person.id == person_id).first()
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    db.delete(db_person)
    db.commit()
    db.close()
    return {"detail": "Person deleted"}
