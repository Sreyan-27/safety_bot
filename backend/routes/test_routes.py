from flask import Blueprint, jsonify

test_bp = Blueprint("test_bp", __name__)

@test_bp.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "Backend Working"}), 200
