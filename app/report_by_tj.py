from app.scrapper.utils import (
    first_level_url,
    second_level_url,
    has_second_level,
    report,
)
import datetime
from app.const import CE_BASE_URL, AL_BASE_URL

from app.dao import dao_report


def tj_report(process_number, report_id, tj):
    date = datetime.datetime.now().isoformat()
    data = {
        "_id": report_id,
        "process_number": process_number,
        "status": "complete",
        "updated_at": str(date),
    }

    match tj:
        case "ce":
            BASE_URL = CE_BASE_URL
        case "al":
            BASE_URL = AL_BASE_URL

    FIRST_LEVEL_URL = f"https://{BASE_URL}cpopg/show.do"
    SECOND_LEVEL_URL = f"https://{BASE_URL}cposg5/show.do"

    url = first_level_url(FIRST_LEVEL_URL, process_number)
    first_data = report(url, tj)

    data["primeiro_grau"] = first_data
    second_level, process_code = has_second_level(BASE_URL, process_number)
    if second_level:
        url = second_level_url(SECOND_LEVEL_URL, process_code)
        second_data = report(url, tj)
        data["segundo_grau"] = second_data

    dao_report.update_report(report_id, data)
