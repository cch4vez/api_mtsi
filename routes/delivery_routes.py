from flask import Blueprint, request, jsonify
from db.connection import engine
from sqlalchemy import text
from utils.decorators import token_required

delivery_bp = Blueprint('delivery', __name__)

@delivery_bp.route('/deliveryInstruction', methods=['POST'])
@token_required
def delivery_instruction(current_user):
    data = request.get_json()
    vins = data.get('vins', [])

    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO delivery_instruction_header (tlp_number, origin_code, pedimento_number, pedimento_date, created_by)
            VALUES (:tlp, :origin, :pedimento, :date, :user)
        """), {
            "tlp": data['tlpNumber'],
            "origin": data['originCode'],
            "pedimento": data['pedimentoNumber'],
            "date": data['pedimentoDate'],
            "user": current_user
        })

        confirmation_id = conn.execute(text("SELECT LAST_INSERT_ID()")).scalar()

        for vin in vins:
            conn.execute(text("""
                INSERT INTO delivery_instruction_details
                (confirmation_id, vin, make, family, carline, year_model, destination_code, color, weight, delivery_instructions)
                VALUES (:cid, :vin, :make, :family, :carline, :year, :dest, :color, :weight, :instr)
            """), {
                "cid": confirmation_id,
                "vin": vin['vin'],
                "make": vin['make'],
                "family": vin['family'],
                "carline": vin['carline'],
                "year": vin['yearModel'],
                "dest": vin['destinationCode'],
                "color": vin['color'],
                "weight": vin['weight'],
                "instr": vin.get('deliveryInstrucions', '')
            })

    return jsonify({
        "confirmationNumber": str(confirmation_id),
        "message": "Instrucción de Viaje Recibida.",
        "processed": True
    })
