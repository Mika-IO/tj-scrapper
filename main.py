from fastapi import FastAPI, BackgroundTasks, Request, HTTPException
import uuid
import datetime

from app.scrapper.utils import validate_process_number, is_valid_uuid
from app.report_by_tj import tj_report

from app.dao import dao_report

app = FastAPI()


@app.post("/report")
async def create_report(request: Request, background_tasks: BackgroundTasks):
    body = await request.json()

    if not body:
        raise HTTPException(status_code=400, detail="body is missing")

    process_number = body.get("process_number")

    if not process_number:
        raise HTTPException(status_code=400, detail="process_number is missing")

    if not validate_process_number(process_number):
        raise HTTPException(status_code=422, detail="invalid process_number")

    tj = body.get("tj")

    if not tj:
        raise HTTPException(status_code=400, detail="tj is missing")

    if not tj in ["ce", "al"]:
        raise HTTPException(status_code=400, detail="invalid tj")


    report = dao_report.get_report_by_process_number(process_number)
    if report:
        return {"process_number": process_number, "report_id": report["id"]}

    report_id = str(uuid.uuid4())
    date = datetime.datetime.now().isoformat()
    dao_report.insert_report(
        {
            "_id": report_id,
            "process_number": process_number,
            "status": "pending",
            "created_at": str(date),
            "updated_at": str(date),
        },
    )

    background_tasks.add_task(tj_report, process_number, report_id, tj)

    return {"process_number": process_number, "report_id": report_id}


@app.get("/report/{report_id}")
def get_report(report_id):
    if not is_valid_uuid(report_id):
        raise HTTPException(status_code=400, detail="invalid report")
    report = dao_report.get_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="report not found")
    return {"report": report}

