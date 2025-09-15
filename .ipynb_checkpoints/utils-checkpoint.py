import hashlib
import qrcode
import base64
from io import BytesIO
import psycopg2
import uuid
import json
from config import contract, w3

def compute_digital_id_hash(aadhaar_number: str, trip_itinerary: dict) -> str:
    combined = aadhaar_number + str(trip_itinerary)
    return hashlib.sha256(combined.encode()).hexdigest()

def send_hash_to_blockchain(digital_id_hash: str, tourist_wallet_address: str) -> str:
    tx_hash = contract.functions.registerTourist(digital_id_hash).transact({'from': tourist_wallet_address})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt.contractAddress

def generate_qr_code(tourist_id: str, digital_id_hash: str) -> str:
    data = f"{tourist_id}|{digital_id_hash}"
    qr = qrcode.make(data)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

def store_in_db(name, aadhaar_number, trip_itinerary, emergency_contacts, digital_id_hash, qr_base64):
    conn = psycopg2.connect(
        database="yatrasuraksha_db",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    tourist_id = str(uuid.uuid4())
    query = """
    INSERT INTO tourist_profile 
    (tourist_id, name, aadhaar_number, trip_itinerary, emergency_contacts, digital_id_hash, qr_code)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (
        tourist_id,
        name,
        aadhaar_number,
        json.dumps(trip_itinerary),
        json.dumps(emergency_contacts),
        digital_id_hash,
        qr_base64
    ))
    conn.commit()
    cursor.close()
    conn.close()

    return tourist_id
