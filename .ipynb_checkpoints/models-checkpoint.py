from pydantic import BaseModel

class TouristInfo(BaseModel):
    name: str
    aadhaar_number: str
    trip_itinerary: dict
    emergency_contacts: dict
    tourist_wallet_address: str
