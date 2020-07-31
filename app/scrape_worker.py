import sys

import hearing
import persist


def work():
    for case_id in (line.rstrip() for line in sys.stdin):
        case = hearing.fetch_parsed_case(case_id)
        if case is not None:
            persist.rest_case(case)
            persist.update_case_work_logs((case_id,))


if __name__ == "__main__":
    work()
