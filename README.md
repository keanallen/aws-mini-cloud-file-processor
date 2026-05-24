# Mini Cloud File Processor

A small FastAPI service with a file upload endpoint.

## Requirements

- Python 3.12+
- `pip`

## Setup

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure AWS credentials with a named profile:

```bash
aws configure --profile demo-file-processor
```

Use this profile for local AWS access instead of storing AWS keys in `.env`.

## Run the project

Start the FastAPI app with Uvicorn:

```bash
uvicorn main:app --reload
```

The API will be available at:

- App: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Available endpoints

### `GET /`
Returns a simple health-style response:

```json
{"Hello": "World"}
```

### `POST /api/v1/file/upload`
Uploads a file request and returns the uploaded file name.

Example response:

```json
{"filename": "example.txt"}
```

You can test this endpoint from the Swagger UI at `/docs`.

## Project structure

```text
main.py                  # FastAPI app entry point
requirements.txt         # Python dependencies
src/api/router.py        # Main API router
src/api/v1/file.py       # File upload endpoint
src/schemas/file_schema.py # Request schema
```
