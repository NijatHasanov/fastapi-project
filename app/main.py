from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
import json
from datetime import datetime

from app.services.data_service import DataService
from app.services.insights_service import AIInsightsService  
from app.services.ml_service import MLService
from app.routes import users, auth
from app.database import create_tables

app = FastAPI(
    title="Hotel Energy SaaS API",
    description="AI-Powered Energy Optimization Platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)

# Initialize services
data_service = DataService()
insights_service = AIInsightsService()
ml_service = MLService()

# In-memory storage (replace with database in production)
historical_data: List[Dict] = []

@app.on_event("startup")
async def startup_event():
    """Initialize system with database tables and sample data"""
    await create_tables()
    
    global historical_data
    # Generate initial historical data for better insights
    for i in range(24):  # Last 24 hours
        sample_data = data_service.generate_hotel_metrics()
        sample_data["timestamp"] = (datetime.utcnow().replace(hour=i)).isoformat()
        historical_data.append(sample_data)

@app.get("/")
def read_root():
    return {
        "message": "Hotel Energy SaaS API",
        "status": "operational", 
        "version": "1.0.0",
        "endpoints": ["/metrics", "/insights", "/recommendations", "/predictions", "/efficiency-score"]
    }

@app.get("/metrics")
def get_current_metrics():
    """Get real-time hotel energy metrics"""
    try:
        metrics = data_service.generate_hotel_metrics()
        
        # Store for historical analysis
        if len(historical_data) > 100:  # Keep last 100 readings
            historical_data.pop(0)
        historical_data.append(metrics)
        
        # Add computed fields
        metrics["status"] = "operational"
        metrics["last_updated"] = datetime.utcnow().isoformat()
        
        return metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating metrics: {str(e)}")

@app.get("/insights")
def get_ai_insights():
    """Get AI-generated insights and recommendations"""
    try:
        if not historical_data:
            return []
        
        current_metrics = historical_data[-1]
        insights = insights_service.generate_insights(current_metrics, historical_data)
        
        # Add metadata
        for insight in insights:
            insight["generated_at"] = datetime.utcnow().isoformat()
            insight["id"] = f"insight_{len(insights)}_{int(datetime.utcnow().timestamp())}"
        
        return insights
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating insights: {str(e)}")

@app.get("/recommendations") 
def get_optimization_recommendations():
    """Get specific optimization recommendations"""
    try:
        if not historical_data:
            return []
        
        current_metrics = historical_data[-1]
        recommendations = insights_service.generate_optimizations(current_metrics)
        
        # Add metadata and priority scoring
        for i, rec in enumerate(recommendations):
            rec["id"] = f"opt_{i}_{int(datetime.utcnow().timestamp())}"
            rec["status"] = "pending"
            rec["created_at"] = datetime.utcnow().isoformat()
            rec["priority_score"] = rec["expectedSavings"] * rec["confidence"]
        
        # Sort by priority score
        recommendations.sort(key=lambda x: x["priority_score"], reverse=True)
        
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")

@app.get("/predictions")
def get_energy_predictions():
    """Get ML-based energy usage predictions"""
    try:
        predictions = ml_service.predict_energy_usage(historical_data, hours_ahead=8)
        
        return {
            "predictions": predictions,
            "model_accuracy": ml_service.prediction_model_accuracy,
            "generated_at": datetime.utcnow().isoformat(),
            "baseline_usage": historical_data[-1]["energy_usage"] if historical_data else 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating predictions: {str(e)}")

@app.get("/efficiency-score")
def get_efficiency_score():
    """Get energy efficiency score and benchmarks"""
    try:
        score = data_service.calculate_efficiency_score(historical_data)
        
        return {
            "score": score,
            "grade": "Excellent" if score >= 85 else "Good" if score >= 70 else "Needs Improvement",
            "benchmarks": [
                {"name": "Hotel Average", "score": 72, "type": "industry"},
                {"name": "Industry Leader", "score": 88, "type": "best_practice"},
                {"name": "Your Target", "score": 85, "type": "goal"}
            ],
            "factors": {
                "usage_efficiency": round(score * 0.4, 1),
                "occupancy_optimization": round(score * 0.3, 1), 
                "system_performance": round(score * 0.3, 1)
            },
            "calculated_at": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating efficiency score: {str(e)}")

@app.get("/metrics/history")
def get_metrics_history():
    """Get historical metrics data for charts"""
    try:
        return {
            "readings": historical_data,
            "count": len(historical_data),
            "time_range": {
                "start": historical_data[0]["timestamp"] if historical_data else None,
                "end": historical_data[-1]["timestamp"] if historical_data else None
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving history: {str(e)}")

@app.get("/anomalies")
def get_anomaly_detection():
    """Get detected anomalies in energy patterns"""
    try:
        if not historical_data:
            return []
        
        current_metrics = historical_data[-1] 
        anomalies = ml_service.detect_anomalies(current_metrics, historical_data)
        
        return {
            "anomalies": anomalies,
            "detection_time": datetime.utcnow().isoformat(),
            "baseline_period": "24_hours"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error detecting anomalies: {str(e)}")

@app.get("/savings-potential")
def get_savings_potential():
    """Calculate potential savings from all optimizations"""
    try:
        if not historical_data:
            return {}
        
        current_metrics = historical_data[-1]
        optimizations = insights_service.generate_optimizations(current_metrics)
        savings = ml_service.calculate_savings_potential(current_metrics, optimizations)
        
        return savings
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating savings: {str(e)}")

@app.get("/health")
def health_check():
    """API health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "data_service": "operational",
            "insights_service": "operational", 
            "ml_service": "operational"
        },
        "data_points": len(historical_data)
    }
