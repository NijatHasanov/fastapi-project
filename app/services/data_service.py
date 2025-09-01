import random
import time
from datetime import datetime, timedelta
from typing import Dict, List

class DataService:
    def __init__(self):
        self.base_energy_usage = 1200
        self.base_occupancy = 75
        
    def get_external_weather_data(self) -> Dict:
        """Simulate weather API data"""
        return {
            "temperature": random.uniform(18, 28),
            "humidity": random.uniform(40, 80),
            "weather_condition": random.choice(["sunny", "cloudy", "rainy"]),
            "wind_speed": random.uniform(5, 25)
        }
    
    def get_energy_grid_data(self) -> Dict:
        """Simulate energy grid API data"""
        return {
            "carbon_intensity": random.uniform(200, 450),  # gCO2/kWh
            "energy_price": random.uniform(0.12, 0.35),    # $/kWh
            "grid_demand": random.uniform(0.7, 1.0)        # utilization %
        }
    
    def generate_hotel_metrics(self) -> Dict:
        """Generate realistic hotel energy metrics"""
        weather = self.get_external_weather_data()
        grid = self.get_energy_grid_data()
        
        # Calculate dynamic factors
        hour = datetime.now().hour
        is_peak_hour = 16 <= hour <= 22
        is_business_day = datetime.now().weekday() < 5
        
        # Temperature impact on HVAC
        temp_deviation = abs(weather["temperature"] - 22)  # 22°C is optimal
        temp_factor = 1 + (temp_deviation * 0.03)
        
        # Occupancy simulation
        base_occupancy = self.base_occupancy
        if is_peak_hour:
            base_occupancy *= 1.2
        if is_business_day:
            base_occupancy *= 1.1
        
        occupancy = min(100, base_occupancy + random.uniform(-10, 15))
        
        # Energy usage calculation
        energy_usage = self.base_energy_usage * temp_factor * (occupancy / 100)
        energy_usage += random.uniform(-50, 100)  # Random variation
        
        # Savings calculation
        potential_savings = energy_usage * 0.15 * (grid["energy_price"] / 0.20)
        
        return {
            "energy_usage": round(energy_usage, 1),
            "occupancy": round(occupancy, 1),
            "temperature": round(weather["temperature"], 1),
            "humidity": round(weather["humidity"], 1),
            "carbon_intensity": round(grid["carbon_intensity"], 1),
            "energy_price": round(grid["energy_price"], 3),
            "potential_savings": round(potential_savings, 0),
            "integrations": 5,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def calculate_efficiency_score(self, historical_data: List[Dict]) -> int:
        """Calculate energy efficiency score based on historical data"""
        if not historical_data or len(historical_data) < 5:
            return 78  # Default score
        
        # Calculate average usage per occupancy
        avg_usage_per_occupancy = sum(
            d["energy_usage"] / max(d["occupancy"], 1) 
            for d in historical_data[-10:]
        ) / min(len(historical_data), 10)
        
        # Benchmark: 15 kWh per % occupancy is excellent
        benchmark = 15.0
        efficiency_ratio = benchmark / avg_usage_per_occupancy
        
        score = min(99, max(50, int(efficiency_ratio * 75)))
        return score