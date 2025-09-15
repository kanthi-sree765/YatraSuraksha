from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import base64


app = FastAPI()

# Database connection (use your actual DB config)
conn = psycopg2.connect(
    host="localhost",
    database="yatrasuraksha_db",
    user="postgres",
    password="postgres"
)

class QRData(BaseModel):
    tourist_id: str
    digital_id_hash: str

@app.post("/api/tourists/verify")
def verify_tourist(data: QRData):
    cursor = conn.cursor()
    query = "SELECT name, aadhaar_number, trip_itinerary, emergency_contacts FROM tourist_profile WHERE tourist_id=%s AND digital_id_hash=%s"
    cursor.execute(query, (data.tourist_id, data.digital_id_hash))
    result = cursor.fetchone()
    
    if not result:
        raise HTTPException(status_code=404, detail="Tourist not found or invalid hash")

    name, aadhaar, itinerary, emergency_contacts = result
    return {
        "tourist_id": data.tourist_id,
        "name": name,
        "aadhaar_number": aadhaar,
        "trip_itinerary": itinerary,
        "emergency_contacts": emergency_contacts
    }

from fastapi.responses import Response

@app.get("/api/tourists/{tourist_id}/qrcode/image")
def get_qrcode_image(tourist_id: str):
    cursor = conn.cursor()
    query = "SELECT qr_code FROM tourist_profile WHERE tourist_id = %s"
    cursor.execute(query, (tourist_id,))
    result = cursor.fetchone()

    if not result:
        raise HTTPException(status_code=404, detail="Tourist not found")

    qr_base64 = result[0]
    img_bytes = base64.b64decode(qr_base64)
    return Response(content=img_bytes, media_type="image/png")

