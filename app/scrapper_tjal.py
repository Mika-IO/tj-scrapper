from scrapper.scrapper import (
    first_level_url,
    second_level_url,
    has_second_level,
    report,
)
from scrapper.const import AL_BASE_URL, AL_FIRST_LEVEL_URL, AL_SECOND_LEVEL_URL
import json
import time


def tjal_scrapper(process_number):
    url = first_level_url(AL_FIRST_LEVEL_URL, process_number)
    first_data = report(url)

    print("=== PRIMEIRO GRAU ===")
    print(json.dumps(first_data, indent=4, ensure_ascii=False))

    second_level, process_code = has_second_level(AL_BASE_URL, process_number)
    if second_level:
        url = second_level_url(AL_SECOND_LEVEL_URL, process_code)
        second_data = report(url)

        print("=== SEGUNDO GRAU ===")
        print(json.dumps(second_data, indent=4, ensure_ascii=False))


process_number = "0710802-55.2018.8.02.0001"

start = time.time()
tjal_scrapper(process_number)
end = time.time()

print("execution_time: {:.6f} segundos".format(end - start))
