from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from anthropic import Anthropic
import os
import json
import httpx
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="Travel Planner AI API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class TravelPreferences(BaseModel):
    city: str
    interests: List[str]  # e.g., ["sejarah", "kuliner", "alam"]
    duration: int  # dalam hari
    budget: str  # "rendah", "menengah", "tinggi"
    start_location: Optional[str] = None

class Destination(BaseModel):
    name: str
    description: str
    category: str
    lat: float
    lon: float
    estimated_duration: str
    tips: str

class TravelPlan(BaseModel):
    destinations: List[Destination]
    route_summary: str
    total_distance: str
    estimated_time: str
    budget_consideration: str
    start_location: str

# Nominatim geocoding
async def geocode_location(location: str) -> tuple:
    """Konversi nama lokasi ke koordinat lat/lon"""
    async with httpx.AsyncClient() as client:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": location,
            "format": "json",
            "limit": 1
        }
        headers = {"User-Agent": "TravelPlannerAI/1.0"}
        
        response = await client.get(url, params=params, headers=headers)
        data = response.json()
        
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])
        return None, None

# Generate travel plan dengan Claude
async def generate_travel_plan(preferences: TravelPreferences) -> dict:
    """Generate rencana perjalanan menggunakan Claude API"""
    
    client = Anthropic(
        api_key=os.environ.get("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com/anthropic"
    )
    
    prompt = f"""Kamu adalah travel planner expert untuk Indonesia. 
Buatkan rencana perjalanan wisata dengan detail berikut:

Kota: {preferences.city}
Minat: {', '.join(preferences.interests)}
Durasi: {preferences.duration} hari
Budget: {preferences.budget}

Berikan rekomendasi 5-8 destinasi wisata yang sesuai. Untuk setiap destinasi, berikan:
1. Nama lokasi yang spesifik dan akurat
2. Deskripsi singkat (2-3 kalimat)
3. Kategori (kuliner/sejarah/alam/belanja/religi/hiburan)
4. Estimasi waktu kunjungan
5. Tips praktis

Urutkan destinasi dalam rute yang logis dan efisien dengan pertimbangan jarak dan waktu tempuh ke setiap lokasi serta budget.

PENTING: Berikan response dalam format JSON yang valid dengan struktur:
{{
  "destinations": [
    {{
      "name": "Nama Lengkap Lokasi",
      "description": "Deskripsi detail",
      "category": "kategori",
      "estimated_duration": "durasi",
      "tips": "tips praktis"
    }}
  ],
  "route_summary": "Ringkasan rute perjalanan",
  "estimated_time": "Total estimasi waktu",
  "total_distance": "Total jarak tempuh dalam km dari semua destinasi",
  "budget_consideration": "Penjelasan singkat tentang bagaimana budget dipertimbangkan",
  "start_location": "Lokasi awal perjalanan"
}}

Hanya return JSON, tanpa penjelasan tambahan."""

    message = client.messages.create(
        model="deepseek-chat",
        max_tokens=5000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    response_text = message.content[0].text
    
    # Parse JSON response
    try:
        # Coba extract JSON dari response
        start = response_text.find('{')
        end = response_text.rfind('}') + 1
        json_str = response_text[start:end]
        plan_data = json.loads(json_str)
        return plan_data
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse AI response")

@app.post("/api/plan", response_model=TravelPlan)
async def create_travel_plan(preferences: TravelPreferences):
    """Endpoint utama untuk generate travel plan"""
    
    try:
        # Generate plan dari AI
        plan_data = await generate_travel_plan(preferences)
        
        # Geocode setiap destinasi
        destinations = []
        for dest in plan_data["destinations"]:
            location_query = f"{dest['name']}, {preferences.city}"
            lat, lon = await geocode_location(location_query)
            
            # Fallback ke koordinat kota jika gagal
            if lat is None:
                lat, lon = await geocode_location(preferences.city)
                # Tambahkan offset kecil untuk variasi
                import random
                lat += random.uniform(-0.01, 0.01)
                lon += random.uniform(-0.01, 0.01)
            
            destinations.append(Destination(
                name=dest["name"],
                description=dest["description"],
                category=dest["category"],
                lat=lat,
                lon=lon,
                estimated_duration=dest["estimated_duration"],
                tips=dest["tips"]
            ))
        
        return TravelPlan(
            destinations=destinations,

            route_summary=plan_data.get("route_summary", "Rute optimal telah dibuat"),
            budget_consideration=plan_data.get("budget_consideration", "Pertimbangan budget tidak tersedia"),
            total_distance=plan_data.get("total_distance", "Akan dihitung otomatis"),
            estimated_time=plan_data.get("estimated_time", f"{preferences.duration} hari"),
            start_location=plan_data.get("start_location", preferences.start_location or preferences.city)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/geocode")
async def geocode(location: str):
    """Helper endpoint untuk geocoding"""
    lat, lon = await geocode_location(location)
    if lat is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return {"lat": lat, "lon": lon}

@app.get("/")
async def root():
    return {
        "message": "Travel Planner AI API",
        "endpoints": {
            "/api/plan": "POST - Generate travel plan",
            "/api/geocode": "GET - Geocode location"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
