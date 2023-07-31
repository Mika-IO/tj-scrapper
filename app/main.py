from fastapi import FastAPI

app = FastAPI()


@app.post("/report")
def create_report():
    return {"report": []}


@app.get("/report/{report_id}")
def get_report(report_id):
    return {"report": report_id}
