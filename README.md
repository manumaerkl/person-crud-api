# CRUD API for Managing Person Records

## Introduction

This project is a RESTful API developed with FastAPI and Python. It manages person records stored in a PostgreSQL database. Each person record includes the following fields: ID, First Name, Last Name, Email, and Age. The API provides four main CRUD (Create, Read, Update, Delete) operations.

## Getting Started

### Prerequisites

- Python 3.11.8
- PostgreSQL or any other database that is compatible with SQLAlchemy

### Installation

1. Clone the repository:
    ```bash
    git clone <repository-url>
    ```
2. Navigate into the project directory:
    ```bash
    cd <project-directory>
    ```
3. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
4. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
5. Update the database URL in `database.py` with your actual database information.

## Usage

Start the FastAPI server:

```bash
uvicorn main:app --reload
```
Now your API should be running and accessible at `http://localhost:8000`.

## API Endpoints

The API provides the following endpoints:

- `POST /people/`: Adds a new person to the database. The body of the request should include the First Name, Last Name, Email, and Age.
- `GET /people/{person_id}`: Retrieves the details of a person based on the provided `person_id`.
- `PUT /people/{person_id}`: Updates the specified fields of a person record. The body of the request should include any combination of First Name, Last Name, Email, and Age.
- `DELETE /people/{person_id}`: Deletes the person record corresponding to the `person_id`.

For more information about these endpoints, you can check the API documentation that is automatically generated and available at `http://localhost:8000/docs` when the server is running.