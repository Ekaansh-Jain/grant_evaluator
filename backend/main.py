"""
FastAPI Backend for Grant Evaluator
Supports file upload, grant evaluation pipeline, and MongoDB Atlas storage
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from typing import List, Optional
import os
import sys
import tempfile
from datetime import datetime
from bson import ObjectId

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import EvaluationResponse, SettingsModel, EvaluationCreate
from database import get_database
import database
from evaluation_pipeline import run_full_evaluation
from src.agents.pdf_generator import generate_evaluation_report_pdf

app = FastAPI(
    title="Grant Evaluator API",
    description="AI-powered grant proposal evaluation system",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup"""
    from database import connect_to_mongo
    try:
        await connect_to_mongo()
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"❌ CRITICAL ERROR: MongoDB connection failed!")
        print(f"{'='*60}")
        print(f"Error: {e}")
        print(f"\n💡 Solution: Check QUICKFIX_MONGODB.md for instructions")
        print(f"{'='*60}\n")


@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown"""
    from database import close_mongo_connection
    await close_mongo_connection()


@app.get("/")
async def root():
    """Health check endpoint"""
    from database import client, database
    
    mongo_status = "disconnected"
    if client is not None:
        try:
            await client.admin.command('ping')
            mongo_status = "connected"
        except:
            mongo_status = "error"
    
    return {
        "status": "healthy" if mongo_status == "connected" else "degraded",
        "service": "Grant Evaluator API",
        "version": "1.0.0",
        "mongodb": mongo_status,
        "database": database.name if database is not None else None
    }


@app.post("/api/evaluations", response_model=EvaluationResponse)
async def create_evaluation(
    file: UploadFile = File(...),
    db=Depends(get_database)
):
    """
    Upload and evaluate a grant proposal (PDF or DOCX)
    Returns comprehensive evaluation with scores, critique, and budget analysis
    """
    
    # Validate file type
    allowed_extensions = ['.pdf', '.docx']
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
        )
    
    # Get settings for max_budget
    settings = await database.settings_collection.find_one()
    max_budget = settings.get('max_budget', 50000) if settings else 50000
    
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        tmp_file_path = tmp_file.name
    
    try:
        # Run evaluation pipeline
        evaluation_result = run_full_evaluation(
            file_path=tmp_file_path,
            max_budget=max_budget
        )
        
        # Prepare document for MongoDB
        evaluation_doc = {
            "file_name": file.filename,
            "file_size": len(content),
            "decision": evaluation_result["decision"],
            "overall_score": evaluation_result["overall_score"],
            "scores": evaluation_result["scores"],
            "critique_domains": evaluation_result["critique_domains"],
            "section_scores": evaluation_result["section_scores"],
            "full_critique": evaluation_result["full_critique"],
            "budget_analysis": evaluation_result["budget_analysis"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # Insert into MongoDB
        result = await database.evaluations_collection.insert_one(evaluation_doc)
        evaluation_doc["id"] = str(result.inserted_id)
        evaluation_doc["_id"] = str(result.inserted_id)
        
        # Convert datetime to ISO string for JSON response
        evaluation_doc["created_at"] = evaluation_doc["created_at"].isoformat()
        evaluation_doc["updated_at"] = evaluation_doc["updated_at"].isoformat()
        
        return evaluation_doc
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")
    finally:
        # Clean up temp file
        if os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)


@app.get("/api/evaluations", response_model=List[EvaluationResponse])
async def get_evaluations(db=Depends(get_database)):
    """Get all evaluations, sorted by creation date (newest first)"""
    
    cursor = database.evaluations_collection.find().sort("created_at", -1)
    evaluations = []
    
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        doc["created_at"] = doc["created_at"].isoformat()
        doc["updated_at"] = doc["updated_at"].isoformat()
        evaluations.append(doc)
    
    return evaluations


@app.get("/api/evaluations/{evaluation_id}", response_model=EvaluationResponse)
async def get_evaluation_by_id(evaluation_id: str, db=Depends(get_database)):
    """Get a specific evaluation by ID"""
    
    try:
        obj_id = ObjectId(evaluation_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid evaluation ID format")
    
    doc = await database.evaluations_collection.find_one({"_id": obj_id})
    
    if not doc:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    
    doc["id"] = str(doc["_id"])
    doc["created_at"] = doc["created_at"].isoformat()
    doc["updated_at"] = doc["updated_at"].isoformat()
    
    return doc


@app.get("/api/evaluations/{evaluation_id}/download")
async def download_evaluation_pdf(evaluation_id: str, db=Depends(get_database)):
    """Download evaluation as PDF report"""
    
    try:
        obj_id = ObjectId(evaluation_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid evaluation ID format")
    
    doc = await database.evaluations_collection.find_one({"_id": obj_id})
    
    if not doc:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    
    # Prepare data for PDF generation
    doc["id"] = str(doc["_id"])
    doc["created_at"] = doc["created_at"].isoformat()
    doc["updated_at"] = doc["updated_at"].isoformat()
    
    try:
        # Generate PDF
        pdf_buffer = generate_evaluation_report_pdf(doc)
        
        # Create filename
        filename = f"grant_evaluation_{doc.get('file_name', 'report').replace('.pdf', '').replace('.docx', '')}_{evaluation_id[:8]}.pdf"
        
        # Return PDF as streaming response
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Access-Control-Expose-Headers": "Content-Disposition"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")


@app.get("/api/settings", response_model=SettingsModel)
async def get_settings(db=Depends(get_database)):
    """Get application settings"""
    
    settings = await database.settings_collection.find_one()
    
    if not settings:
        # Return default settings if none exist
        return {
            "max_budget": 50000,
            "chunk_size": 1000,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
    
    settings["id"] = str(settings["_id"])
    settings["created_at"] = settings.get("created_at", datetime.utcnow()).isoformat()
    settings["updated_at"] = settings.get("updated_at", datetime.utcnow()).isoformat()
    
    return settings


@app.put("/api/settings", response_model=SettingsModel)
async def update_settings(settings: SettingsModel, db=Depends(get_database)):
    """Update application settings"""
    
    existing = await database.settings_collection.find_one()
    
    settings_dict = {
        "max_budget": settings.max_budget,
        "chunk_size": settings.chunk_size,
        "updated_at": datetime.utcnow()
    }
    
    if existing:
        # Update existing settings
        await database.settings_collection.update_one(
            {"_id": existing["_id"]},
            {"$set": settings_dict}
        )
        settings_dict["id"] = str(existing["_id"])
        settings_dict["created_at"] = existing.get("created_at", datetime.utcnow())
    else:
        # Create new settings
        settings_dict["created_at"] = datetime.utcnow()
        result = await database.settings_collection.insert_one(settings_dict)
        settings_dict["id"] = str(result.inserted_id)
    
    settings_dict["created_at"] = settings_dict["created_at"].isoformat()
    settings_dict["updated_at"] = settings_dict["updated_at"].isoformat()
    
    return settings_dict


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
