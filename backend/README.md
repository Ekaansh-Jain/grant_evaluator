# Grant Evaluator FastAPI Backend

This is the backend API for the Grant Evaluator application. It provides REST endpoints for uploading grant proposals, running AI-powered evaluations, and managing evaluation results using MongoDB Atlas.

## Features

- **File Upload**: Accept PDF and DOCX grant proposals
- **AI Evaluation Pipeline**: Full evaluation using LLM agents (summarizer, scorer, critique, budget, decision)
- **MongoDB Atlas Storage**: Store evaluations and settings
- **CORS Enabled**: Works with React frontend

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Edit `.env` with your MongoDB Atlas connection string:

```env
MONGODB_URL=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority
DATABASE_NAME=grant-evaluator
```

### 3. MongoDB Atlas Setup

1. Create a free account at [MongoDB Atlas](https://cloud.mongodb.com/)
2. Create a new cluster (free tier is sufficient)
3. Create a database user with read/write permissions
4. Get your connection string from "Connect" → "Connect your application"
5. Whitelist your IP address or use `0.0.0.0/0` for development

### 4. Run the Server

```bash
# Development mode with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or use Python directly
python main.py
```

API will be available at: `http://localhost:8000`

Interactive docs: `http://localhost:8000/docs`

## API Endpoints

### Health Check
- `GET /` - Check if API is running

### Evaluations
- `POST /api/evaluations` - Upload and evaluate a grant proposal
- `GET /api/evaluations` - Get all evaluations (sorted by date)
- `GET /api/evaluations/{id}` - Get specific evaluation by ID

### Settings
- `GET /api/settings` - Get application settings
- `PUT /api/settings` - Update application settings

## Project Structure

```
backend/
├── main.py                    # FastAPI application and routes
├── models.py                  # Pydantic models for validation
├── database.py                # MongoDB connection and collections
├── evaluation_pipeline.py     # Grant evaluation orchestration
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## Dependencies

- **FastAPI**: Modern web framework
- **Motor**: Async MongoDB driver
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation
- **Python-dotenv**: Environment management

## Development

### Running Tests

```bash
pytest
```

### Code Quality

```bash
# Format code
black .

# Lint
flake8 .
```

## Deployment

For production deployment:

1. Set proper CORS origins in `main.py`
2. Use production-grade MongoDB Atlas cluster
3. Enable SSL/TLS
4. Use environment variables for secrets
5. Deploy with Gunicorn/Uvicorn workers

Example production command:
```bash
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```
