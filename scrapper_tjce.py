from poc.scrapper import first_level_url, second_level_url, has_second_level, report
from poc.const import CE_BASE_URL, CE_FIRST_LEVEL_URL, CE_SECOND_LEVEL_URL
import json
import time


def tjce_report(process_number):
    url = first_level_url(CE_FIRST_LEVEL_URL, process_number)
    first_data = report(url)

    print("=== PRIMEIRO GRAU ===")
    print(json.dumps(first_data, indent=4, ensure_ascii=False))

    second_level, process_code = has_second_level(CE_BASE_URL, process_number)
    if second_level:
        url = second_level_url(CE_SECOND_LEVEL_URL, process_code)
        second_data = report(url)

        print("=== SEGUNDO GRAU ===")
        print(json.dumps(second_data, indent=4, ensure_ascii=False))


process_number = "0070337-91.2008.8.06.0001"

start = time.time()
tjce_report(process_number)
end = time.time()

print("execution_time: {:.6f} segundos".format(end - start))
