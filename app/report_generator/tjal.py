from app.scrapper.utils import (
    first_level_url,
    second_level_url,
    has_second_level,
    report,
)
from app.const import AL_BASE_URL, AL_FIRST_LEVEL_URL, AL_SECOND_LEVEL_URL

from app.dao import dao_report


def tjal_report(process_number, report_id):
    data = {"_id": report_id, "process_number": process_number}
    url = first_level_url(AL_FIRST_LEVEL_URL, process_number)
    first_data = report(url, "AL")

    data["primeiro_grau"] = first_data
    second_level, process_code = has_second_level(AL_BASE_URL, process_number)
    if second_level:
        url = second_level_url(AL_SECOND_LEVEL_URL, process_code)
        second_data = report(url, "al")
        data["segundo_grau"] = second_data

    dao_report.update_report(report_id, data)
