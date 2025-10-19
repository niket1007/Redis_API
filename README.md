# Redis API

A FastAPI-based REST API for performing CRUD operations on Redis with support for multiple data types including strings, lists, sets, hashes, and JSON.

## Features

- **Multiple Data Types Support**: STRING, LIST, SET, HASH, and JSON
- **CRUD Operations**: Create, Read, Update, and Delete operations for Redis keys
- **Key Expiration**: Set TTL (Time To Live) for keys
- **Path-based Queries**: Access specific fields in HASH and JSON data types
- **Comprehensive Error Handling**: Custom exception handlers with detailed logging
- **Integration Tests**: Full test suite using pytest
- **Type Safety**: Pydantic models for request/response validation

## Tech Stack

- **FastAPI**: Modern web framework for building APIs
- **Redis**: In-memory data structure store
- **Pydantic**: Data validation using Python type annotations
- **Python-Decouple**: Separate configuration from code
- **Pytest**: Testing framework

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Redis_API
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install fastapi redis python-decouple uvicorn pytest
```

4. Create a `.env` file in the root directory:
```env
redis_host=localhost
redis_port=6379
redis_username=your_username  # Optional
redis_password=your_password  # Optional
```

## Running the Application

Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

Access the interactive API documentation at `http://localhost:8000/docs`

## API Endpoints

### 1. Ping Redis Server
**GET** `/ping`

Check if Redis server is accessible.

**Response:**
```json
{
  "status": "success"
}
```

### 2. Get Data from Redis
**GET** `/redis/{key}?path={path}`

Retrieve data from Redis by key.

**Parameters:**
- `key` (path): Redis key
- `path` (query, optional): Field path for HASH or JSON data types

**Response:**
```json
{
  "key": "my_key",
  "value": "my_value"
}
```

### 3. Set Data in Redis
**POST** `/redis`

Create or update data in Redis.

**Request Body:**
```json
{
  "data_type": "STRING",
  "key": "my_key",
  "value": "my_value",
  "expiryT": 3600,
  "json_path": "$"
}
```

**Parameters:**
- `data_type`: STRING | LIST | SET | HASH | JSON
- `key`: Redis key name
- `value`: Data to store (type must match data_type)
- `expiryT` (optional): Expiration time in seconds
- `json_path` (optional): JSON path for JSON data type (default: "$")

**Response:**
```json
{
  "key": "my_key",
  "message": "Successfully added/updated to redis"
}
```

### 4. Delete Key from Redis
**DELETE** `/redis/{key}`

Delete a key from Redis.

**Parameters:**
- `key` (path): Redis key to delete

**Response:**
```json
{
  "key": "my_key",
  "message": "Delete operation successfully completed"
}
```

## Data Type Examples

### String
```json
{
  "data_type": "STRING",
  "key": "username",
  "value": "john_doe"
}
```

### List
```json
{
  "data_type": "LIST",
  "key": "shopping_list",
  "value": ["apples", "bananas", "oranges"]
}
```

### Set
```json
{
  "data_type": "SET",
  "key": "unique_visitors",
  "value": ["user1", "user2", "user3"]
}
```

### Hash
```json
{
  "data_type": "HASH",
  "key": "user:1000",
  "value": {
    "name": "John Doe",
    "email": "john@example.com"
  }
}
```

### JSON
```json
{
  "data_type": "JSON",
  "key": "user_profile",
  "value": {
    "name": "John Doe",
    "age": 30,
    "address": {
      "city": "New York",
      "country": "USA"
    }
  },
  "json_path": "$"
}
```

## Error Responses

### 404 Not Found
```json
{
  "message": "Invalid key"
}
```

### 500 Internal Server Error
```json
{
  "status": "error",
  "message": "Check server logs for debugging the issue"
}
```

## Running Tests

Execute the integration test suite:
```bash
pytest app/Test/test_integration.py -v
```

The tests cover:
- Connection testing (ping)
- CRUD operations for all data types
- Key expiration functionality
- Error handling scenarios
- Data type validation

## Project Structure

```
Redis_API/
├── app/
│   ├── Exception_Handlers/
│   │   ├── __init__.py
│   │   └── exception_handlers.py
│   ├── Log/
│   │   ├── __init__.py
│   │   └── logger.py
│   ├── Models/
│   │   ├── __init__.py
│   │   └── models.py
│   ├── Redis/
│   │   ├── __init__.py
│   │   └── redis.py
│   ├── Routers/
│   │   ├── __init__.py
│   │   └── routers.py
│   ├── Test/
│   │   ├── __init__.py
│   │   └── test_integration.py
│   └── main.py
├── logs/
│   └── app.log
├── .env
├── .gitignore
└── README.md
```

## Logging

The application uses a rotating file handler that creates daily log files in the `logs/` directory. Logs include:
- Info level: Endpoint entry and exit points
- Debug level: Function outputs and intermediate values
- Error level: Exceptions with stack traces
