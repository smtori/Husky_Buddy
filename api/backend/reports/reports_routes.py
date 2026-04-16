from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error
import time
# Create a Blueprint for report routes
reports = Blueprint("reports", __name__)


# Get all reports
@reports.route("/reports", methods=["GET"])
def get_all_reports():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info('GET /report/reports')
        query = "SELECT * FROM flag_report"

        cursor.execute(query)
        reports_list = cursor.fetchall()

        current_app.logger.info(f'Retrieved {len(reports_list)} Reports')
        return jsonify(reports_list), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_reports: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Get detailed information about a specific report
@ngos.route("/reports/<int:report_id>", methods=["GET"])
def get_report(report_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM flag_report WHERE report_id = %s", (report_id,))
        report = cursor.fetchone()

        if not report:
            return jsonify({"error": "NGO not found"}), 404

        return jsonify(report), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# Create a new report
# Required fields: Name, Reason, 
@ngos.route("/reports", methods=["POST"])
def create_ngo():
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()

        required_fields = ["reporter_id", "reported_id", "reason", "status"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        query = """
            INSERT INTO flag_report (reporter_id, reported_id, reason, status, created_at)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            data["reporter_id"],
            data["reported_id"],
            data["reason"],
            data["status"],
            time.time,
        ))

        get_db().commit()
        return jsonify({"message": "Report created successfully", "report_id": cursor.lastrowid}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Update an existing reports information
@ngos.route("/reports/<int:report_id>", methods=["PUT"])
def update_ngo(report_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()

        cursor.execute("SELECT report_id FROM flag_report WHERE report_id = %s", (report_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Report not found"}), 404

        # Build update query dynamically based on provided fields
        allowed_fields = ["status"]
        update_fields = [f"{f} = %s" for f in allowed_fields if f in data]
        params = [data[f] for f in allowed_fields if f in data]

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        params.append(report_id)
        query = f"UPDATE flag_report SET {', '.join(update_fields)} WHERE report_id = %s"
        cursor.execute(query, params)
        get_db().commit()

        return jsonify({"message": "Report updated successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Get all projects associated with a specific NGO
# Example: /ngo/ngos/1/projects
@ngos.route("/ngos/<int:ngo_id>/projects", methods=["GET"])
def get_ngo_projects(ngo_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("SELECT NGO_ID FROM WorldNGOs WHERE NGO_ID = %s", (ngo_id,))
        if not cursor.fetchone():
            return jsonify({"error": "NGO not found"}), 404

        cursor.execute("SELECT * FROM Projects WHERE NGO_ID = %s", (ngo_id,))
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Get all donors associated with a specific NGO
# Example: /ngo/ngos/1/donors
@ngos.route("/ngos/<int:ngo_id>/donors", methods=["GET"])
def get_ngo_donors(ngo_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("SELECT NGO_ID FROM WorldNGOs WHERE NGO_ID = %s", (ngo_id,))
        if not cursor.fetchone():
            return jsonify({"error": "NGO not found"}), 404

        cursor.execute("SELECT * FROM Donors WHERE NGO_ID = %s", (ngo_id,))
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
