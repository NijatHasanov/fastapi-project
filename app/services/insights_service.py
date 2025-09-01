import random
from typing import Dict, List
from datetime import datetime

class AIInsightsService:
    def __init__(self):
        self.insight_templates = {
            "energy_spike": {
                "type": "alert",
                "priority": "critical",
                "title": "Critical Energy Spike Detected",
                "icon": "🚨"
            },
            "hvac_optimization": {
                "type": "optimization",
                "priority": "high", 
                "title": "HVAC Optimization Opportunity",
                "icon": "🌡️"
            },
            "lighting_efficiency": {
                "type": "efficiency",
                "priority": "medium",
                "title": "Lighting Efficiency Improvement",
                "icon": "💡"
            },
            "demand_response": {
                "type": "savings",
                "priority": "medium",
                "title": "Peak Demand Management",
                "icon": "⚡"
            },
            "carbon_reduction": {
                "type": "sustainability",
                "priority": "low",
                "title": "Carbon Footprint Reduction",
                "icon": "🌱"
            }
        }
    
    def generate_insights(self, current_metrics: Dict, historical_data: List[Dict]) -> List[Dict]:
        """Generate AI-powered insights based on current and historical data"""
        insights = []
        
        # Energy Spike Detection
        if current_metrics["energy_usage"] > 1800:
            template = self.insight_templates["energy_spike"]
            insights.append({
                **template,
                "description": f"Energy usage at {current_metrics['energy_usage']:.0f} kWh is 40% above normal baseline.",
                "recommendation": "Immediately investigate HVAC Zone 3 and kitchen equipment for potential malfunctions.",
                "potentialSavings": "$75/hour",
                "confidence": 0.95,
                "severity": "critical"
            })
        
        # HVAC Optimization
        if (current_metrics["temperature"] < 20 and current_metrics["occupancy"] < 80) or \
           (current_metrics["temperature"] > 26 and current_metrics["energy_usage"] > 1500):
            template = self.insight_templates["hvac_optimization"]
            setpoint_change = 2 if current_metrics["temperature"] < 20 else -2
            insights.append({
                **template,
                "description": f"Weather conditions and occupancy levels suggest HVAC optimization opportunity.",
                "recommendation": f"Adjust thermostat setpoint by {setpoint_change}°C in common areas and vacant rooms.",
                "potentialSavings": "$120/day",
                "confidence": 0.88,
                "actionable": True,
                "setpoint_adjustment": setpoint_change
            })
        
        # Lighting Efficiency
        if current_metrics["occupancy"] < 70 and 6 <= datetime.now().hour <= 22:
            template = self.insight_templates["lighting_efficiency"]
            insights.append({
                **template,
                "description": f"Low occupancy ({current_metrics['occupancy']:.1f}%) detected during active hours.",
                "recommendation": "Implement motion sensors in common areas and reduce lighting to 70% in low-traffic zones.",
                "potentialSavings": "$45/day",
                "confidence": 0.82,
                "zones_affected": ["lobby", "hallways", "conference_rooms"]
            })
        
        # Peak Demand Management
        current_hour = datetime.now().hour
        if 16 <= current_hour <= 20 and current_metrics["energy_usage"] > 1600:
            template = self.insight_templates["demand_response"]
            insights.append({
                **template,
                "description": "High energy usage detected during peak demand hours.",
                "recommendation": "Initiate demand response protocol: pre-cool building and defer non-essential loads.",
                "potentialSavings": "$85",
                "confidence": 0.91,
                "load_reduction": "15%"
            })
        
        # Carbon Footprint
        if current_metrics["carbon_intensity"] > 350:
            template = self.insight_templates["carbon_reduction"]
            carbon_impact = (current_metrics["energy_usage"] * current_metrics["carbon_intensity"]) / 1000
            insights.append({
                **template,
                "description": f"High carbon intensity on grid ({current_metrics['carbon_intensity']:.0f} gCO2/kWh).",
                "recommendation": "Reduce energy consumption by 10% for next 2 hours to minimize environmental impact.",
                "potentialSavings": f"{carbon_impact * 0.1:.1f} kg CO2",
                "confidence": 0.86,
                "environmental_benefit": True
            })
        
        return insights
    
    def generate_optimizations(self, current_metrics: Dict) -> List[Dict]:
        """Generate specific optimization recommendations"""
        optimizations = []
        
        # HVAC Optimization
        optimal_temp = 22.0
        if current_metrics["occupancy"] < 60:
            optimal_temp += 1.5
        if current_metrics["temperature"] > 25:
            optimal_temp -= 1.0
            
        optimizations.append({
            "category": "hvac",
            "action": "adjust_setpoint",
            "current_value": current_metrics["temperature"],
            "targetValue": optimal_temp,
            "unit": "°C",
            "expectedSavings": 15,
            "confidence": 0.89,
            "reasoning": "Optimal balance based on occupancy patterns and weather conditions.",
            "implementation": "immediate"
        })
        
        # Lighting Optimization
        if current_metrics["occupancy"] < 85:
            light_level = max(60, 100 - (85 - current_metrics["occupancy"]))
            optimizations.append({
                "category": "lighting",
                "action": "adjust_brightness",
                "targetValue": light_level,
                "unit": "%",
                "expectedSavings": 8,
                "confidence": 0.84,
                "reasoning": f"Reduced foot traffic allows for {100-light_level}% lighting reduction.",
                "zones": ["common_areas", "hallways"]
            })
        
        # Equipment Scheduling
        if 23 <= datetime.now().hour or datetime.now().hour <= 5:
            optimizations.append({
                "category": "equipment",
                "action": "schedule_maintenance",
                "targetValue": 3,
                "unit": "systems",
                "expectedSavings": 5,
                "confidence": 0.92,
                "reasoning": "Off-peak hours ideal for equipment maintenance and optimization.",
                "affected_systems": ["elevators", "pumps", "ventilation"]
            })
        
        return optimizations