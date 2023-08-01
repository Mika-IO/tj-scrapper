from pymongo import MongoClient
from app.const import MONGO_CONNECTION_STRING, MONGO_DB_NAME

client = MongoClient(MONGO_CONNECTION_STRING)
db = client[MONGO_DB_NAME]


def insert_report(report):
    try:
        collection = db["reports"]
        result = collection.insert_one(report)
        print(f"Report inserted ID: {result.inserted_id}")
    except Exception as e:
        print(f"Error to insert report: {e}")


def update_report(report_id: str, update_data: dict):
    try:
        collection = db["reports"]
        query = {"_id": report_id}
        update = {"$set": update_data}
        result = collection.update_one(query, update)
        if result.modified_count > 0:
            print(f"Report with id {report_id} updated successfully.")
        else:
            print(f"No report found with id {report_id}.")
    except Exception as e:
        print(f"Error updating report: {e}")


def get_report(report_id):
    try:
        collection = db["reports"]
        report = collection.find_one({"_id": report_id})

        if report:
            report.pop("_id")
            return report
        else:
            return None
    except Exception as e:
        print(f"Error to get report: {e}")


def get_report_by_process_number(process_number):
    try:
        collection = db["reports"]
        report = collection.find_one({"process_number": process_number})

        if report:
            report = dict(report)
            report["id"] = report.pop("_id")
            return report
        else:
            return None
    except Exception as e:
        print(f"Error to get report by process_number: {e}")
        raise ValueError("Error fetching report from database") from e
