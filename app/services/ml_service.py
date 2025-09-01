import random
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List

class MLService:
    def __init__(self):
        self.prediction_model_accuracy = 0.85
        
    def predict_energy_usage(self, historical_data: List[Dict], hours_ahead: int = 6) -> List[Dict]:
        """Predict energy usage for the next few hours"""
        if not historical_data:
            return []
        
        predictions = []
        last_usage = historical_data[-1]["energy_usage"]
        last_occupancy = historical_data[-1]["occupancy"]
        
        for hour in range(1, hours_ahead + 1):
            future_time = datetime.utcnow() + timedelta(hours=hour)
            future_hour = future_time.hour
            
            # Predict occupancy patterns
            if 6 <= future_hour <= 10:  # Morning
                occupancy_factor = 1.2
            elif 12 <= future_hour <= 14:  # Lunch
                occupancy_factor = 0.8
            elif 17 <= future_hour <= 22:  # Evening
                occupancy_factor = 1.4
            elif 23 <= future_hour or future_hour <= 5:  # Night
                occupancy_factor = 0.3
            else:
                occupancy_factor = 1.0
            
            predicted_occupancy = last_occupancy * occupancy_factor
            predicted_occupancy = max(20, min(100, predicted_occupancy))
            
            # Predict energy usage based on occupancy and time patterns
            base_prediction = last_usage * (predicted_occupancy / last_occupancy)
            
            # Add time-of-day factor
            if 16 <= future_hour <= 20:  # Peak hours
                base_prediction *= 1.15
            elif 1 <= future_hour <= 6:   # Off-peak
                base_prediction *= 0.85
                
            # Add some realistic variance
            variance = random.uniform(-0.08, 0.08)
            predicted_usage = base_prediction * (1 + variance)
            
            predictions.append({
                "timestamp": future_time.isoformat(),
                "predicted_usage": round(predicted_usage, 1),
                "predicted_occupancy": round(predicted_occupancy, 1),
                "confidence": round(self.prediction_model_accuracy - (hour * 0.05), 2),
                "factors": {
                    "time_of_day": future_hour,
                    "occupancy_impact": round((predicted_occupancy - 75) * 0.02, 3),
                    "seasonal_factor": 1.0
                }
            })
            
            last_usage = predicted_usage
            last_occupancy = predicted_occupancy
        
        return predictions
    
    def detect_anomalies(self, current_metrics: Dict, historical_data: List[Dict]) -> List[Dict]:
        """Detect anomalies in energy usage patterns"""
        if len(historical_data) < 10:
            return []
        
        anomalies = []
        recent_data = historical_data[-24:]  # Last 24 hours
        
        # Calculate statistical baselines
        usage_values = [d["energy_usage"] for d in recent_data]
        mean_usage = np.mean(usage_values)
        std_usage = np.std(usage_values)
        
        # Z-score anomaly detection
        current_usage = current_metrics["energy_usage"]
        z_score = abs(current_usage - mean_usage) / std_usage if std_usage > 0 else 0
        
        if z_score > 2.5:  # Significant deviation
            anomalies.append({
                "type": "statistical_anomaly",
                "severity": "high" if z_score > 3 else "medium",
                "description": f"Energy usage {current_usage:.0f} kWh is {z_score:.1f} standard deviations from normal",
                "expected_range": f"{mean_usage - 2*std_usage:.0f} - {mean_usage + 2*std_usage:.0f} kWh",
                "z_score": round(z_score, 2),
                "recommendation": "Investigate equipment status and occupancy patterns"
            })
        
        # Pattern-based anomaly detection
        same_hour_data = [d for d in recent_data if 
                         datetime.fromisoformat(d["timestamp"].replace('Z', '+00:00')).hour == datetime.now().hour]
        
        if len(same_hour_data) >= 3:
            same_hour_mean = np.mean([d["energy_usage"] for d in same_hour_data])
            if abs(current_usage - same_hour_mean) > same_hour_mean * 0.3:
                anomalies.append({
                    "type": "temporal_anomaly",
                    "severity": "medium",
                    "description": f"Usage unusual for this time of day (hour {datetime.now().hour})",
                    "historical_average": round(same_hour_mean, 1),
                    "deviation": round(((current_usage - same_hour_mean) / same_hour_mean) * 100, 1),
                    "recommendation": "Check for schedule changes or equipment issues"
                })
        
        return anomalies
    
    def calculate_savings_potential(self, current_metrics: Dict, optimizations: List[Dict]) -> Dict:
        """Calculate potential savings from optimization recommendations"""
        total_energy_savings = sum(opt["expectedSavings"] for opt in optimizations)
        current_cost = current_metrics["energy_usage"] * current_metrics.get("energy_price", 0.20)
        
        potential_savings = {
            "daily_energy_reduction": round(total_energy_savings, 1),
            "daily_cost_savings": round(current_cost * (total_energy_savings / 100), 2),
            "monthly_projection": round(current_cost * (total_energy_savings / 100) * 30, 2),
            "annual_projection": round(current_cost * (total_energy_savings / 100) * 365, 2),
            "carbon_reduction": round(current_metrics["energy_usage"] * (total_energy_savings / 100) * 0.4, 1),  # kg CO2
            "payback_period": "immediate",
            "confidence": round(np.mean([opt["confidence"] for opt in optimizations]), 2)
        }
        
        return potential_savings