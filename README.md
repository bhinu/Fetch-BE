# Points Management API

This API allows for managing a user's points across different payers. The API supports the following operations:

- **Add Points**: Add points for a specific payer with a timestamp.
- **Spend Points**: Spend points across payers based on specific rules.
- **Check Balances**: Fetch the current balance for all payers.

The implementation is done in Python using the Flask framework.

---

## Table of Contents

1. [Requirements](#requirements)
2. [Setup Instructions](#setup-instructions)
3. [API Endpoints](#api-endpoints)
    - [Home](#home)
    - [Add Points](#add-points)
    - [Spend Points](#spend-points)
    - [Get Balance](#get-balance)
4. [Testing the API](#testing-the-api)

---

## Requirements

To run this project, you need the following installed on your system:

1. **Python 3.8 or above**: [Download Python](https://www.python.org/downloads/).
2. **Pip**: Installed automatically with Python 3.x.
3. **Flask Framework**: A Python web framework.

---

## Setup Instructions

1. Clone the repository or download the code files.
2. Open a terminal and navigate to the project directory.
3. Create a virtual environment (optional but recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # For macOS/Linux
    venv\Scripts\activate     # For Windows
    ```
4. Install the required Python packages:
    ```bash
    pip install flask
    ```
5. Run the Flask server:
    ```bash
    python app.py
    ```
6. The server will start at `http://127.0.0.1:8000`.

---

## API Endpoints

### Home

- **URL**: `/`
- **Method**: GET
- **Description**: Displays a welcome message and available endpoints.
- **Response**:
    ```json
    {
        "message": "Welcome to the Points API. Available endpoints:",
        "endpoints": {
            "/add": "POST - Add points",
            "/spend": "POST - Spend points",
            "/balance": "GET - Get current balances"
        }
    }
    ```

---

### Add Points

- **URL**: `/add`
- **Method**: POST
- **Description**: Add points for a specific payer with a timestamp.
- **Request Body**:
    ```json
    {
        "payer": "DANNON",
        "points": 1000,
        "timestamp": "2022-11-02T14:00:00Z"
    }
    ```
- **Response**:
    ```json
    {
        "message": "Transaction added successfully."
    }
    ```

---

### Spend Points

- **URL**: `/spend`
- **Method**: POST
- **Description**: Spend points based on rules (oldest first, no payer balance goes negative).
- **Request Body**:
    ```json
    {
        "points": 5000
    }
    ```
- **Response**:
    ```json
    [
        { "payer": "DANNON", "points": -100 },
        { "payer": "UNILEVER", "points": -200 },
        { "payer": "MILLER COORS", "points": -4700 }
    ]
    ```

---

### Get Balance

- **URL**: `/balance`
- **Method**: GET
- **Description**: Fetch the current point balances for all payers.
- **Response**:
    ```json
    {
        "DANNON": 1000,
        "UNILEVER": 0,
        "MILLER COORS": 5300
    }
    ```

---

## Testing the API

To test the API, follow these steps:

1. Start the Flask server:
    ```bash
    python app.py
    ```
2. Use a tool like [Postman](https://www.postman.com/) or `curl` to send requests to the endpoints.
3. **Example Test Flow**:
    - Add Transactions:
        ```json
        { "payer": "DANNON", "points": 300, "timestamp": "2022-10-31T10:00:00Z" }
        { "payer": "UNILEVER", "points": 200, "timestamp": "2022-10-31T11:00:00Z" }
        { "payer": "DANNON", "points": -200, "timestamp": "2022-10-31T15:00:00Z" }
        { "payer": "MILLER COORS", "points": 10000, "timestamp": "2022-11-01T14:00:00Z" }
        { "payer": "DANNON", "points": 1000, "timestamp": "2022-11-02T14:00:00Z" }
        ```
    - Spend Points:
        ```json
        { "points": 5000 }
        ```
    - Check Balances:
        ```json
        {
            "DANNON": 800,
            "MILLER COORS": 5500,
            "UNILEVER": 0
        }
        ```
---
