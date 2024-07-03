# Data Integration API

This project implements a data integration API using FastAPI. The API allows you to store and retrieve metric readings such as voltage and current. The data is stored in an SQLite database and can be queried by a date range to retrieve readings along with calculated average power readings.

## File Descriptions

### `database.py`

The `database.py` file is responsible for setting up the database connection using SQLAlchemy. It includes:

- **Database URL**: Specifies the SQLite database URL.
- **Engine Creation**: Creates a database engine.
- **Session Local**: Configures a session factory to interact with the database.
- **Base Class**: A base class for models to inherit from, provided by SQLAlchemy.

### `models.py`

The `models.py` file defines the database model for storing metric readings. It includes:

- **DataReading Model**: A SQLAlchemy model representing the `data_readings` table with columns for `id`, `timestamp`, `metric_name`, and `metric_value`.

### `main.py`

The `main.py` file contains the implementation of the FastAPI application logic. It includes:

- **Database Dependency**: A function to provide a database session for each request.
- **API Endpoints**:
  - `POST /data`: Parses and validates incoming plaintext data, then stores it in the database.
  - `GET /data`: Retrieves data within the specified date range, formats it as JSON, and calculates the average power reading for each day.
- **Application Entry Point**: Starts the Uvicorn server to run the FastAPI application.

