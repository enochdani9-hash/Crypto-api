from fastapi import FastAPI
from pydantic import BaseModel

# Initialize the API
app = FastAPI(title="Agritech Soil API")

# Define the exact data structure the API expects to receive
class SoilTest(BaseModel):
    crop_type: str
    current_n: float
    current_p: float
    current_k: float

# Your core agronomy engine
def calculate_npk_deficit(crop_type, current_n, current_p, current_k):
    crop_requirements = {
        "tomato": {"n": 150, "p": 65, "k": 200},
        "cabbage": {"n": 200, "p": 75, "k": 200},
        "pepper": {"n": 130, "p": 60, "k": 160}
    }
    
    crop = crop_type.lower()
    if crop not in crop_requirements:
        return {"error": f"Crop '{crop_type}' is not supported yet."}
        
    targets = crop_requirements[crop]
    n_needed = max(0, targets["n"] - current_n)
    p_needed = max(0, targets["p"] - current_p)
    k_needed = max(0, targets["k"] - current_k)
    
    return {
        "crop": crop,
        "current_soil_levels": {"N": current_n, "P": current_p, "K": current_k},
        "recommendation_kg_per_ha": {
            "Nitrogen_N": n_needed,
            "Phosphorus_P": p_needed,
            "Potassium_K": k_needed
        },
        "status": "Optimal" if (n_needed == 0 and p_needed == 0 and k_needed == 0) else "Action Required"
    }

# The actual Web Endpoint
@app.post("/api/v1/fertilizer-calc")
def fertilizer_recommendation(data: SoilTest):
    return calculate_npk_deficit(
        data.crop_type, 
        data.current_n, 
        data.current_p, 
        data.current_k
    )

@app.get("/")
def read_root():
    return {"message": "Welcome to the Agritech Soil API. The server is live."}