import sqlite3


def get_case(case_id: str):
    conn = sqlite3.connect("cases.db")
    conn.execute("pragma journal_mode=wal")

    conn.row_factory = sqlite3.Row
    curs = conn.cursor()
    curs.execute("SELECT * FROM V_CASE WHERE ID = ?", (case_id,))
    case = curs.fetchone()
    curs.close()
    if case is None:
        return None
    return dict(case)


def rest_case(case):
    """
    Takes a dictionary representation of a case and maps it in to a sqlite DB
    """
    conn = sqlite3.connect("cases.db", isolation_level=None)
    conn.execute("pragma journal_mode=wal")

    curs = conn.cursor()
    curs.execute(
        """
    INSERT OR REPLACE INTO CASE_DETAIL
    (ID, STATUS, REGISTER_URL, PRECINCT, STYLE, PLAINTIFF, DEFENDANTS, PLAINTIFF_ZIP, DEFENDANT_ZIP)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            case["case_number"],
            case["status"],
            case["register_url"],
            case["precinct_number"],
            case["style"],
            case["plaintiff"],
            case["defendants"],
            case["plaintiff_zip"],
            case["defendant_zip"],
        ),
    )
    curs.execute(
        """
    INSERT OR REPLACE INTO DISPOSITION
    (CASE_DETAIL_ID, TYPE, DATE, AMOUNT, AWARDED_TO, AWARDED_AGAINST)
    VALUES (?, ?, ?, ?, ?, ?)
    """,
        (
            case["case_number"],
            case["disposition_type"],
            case["disposition_date"],
            str(case["disposition_amount"]),
            case["disposition_awarded_to"],
            case["disposition_awarded_against"],
        ),
    )
    # TODO scrape all event types in a similar way (writs should be consolidated in)
    # Types should mirror the values from the HTML table headers, HR/ER/SE/etc.
    for hearing_number, hearing in enumerate(case["hearings"]):
        curs.execute(
            """
            INSERT OR REPLACE INTO EVENT
            (CASE_DETAIL_ID, EVENT_NUMBER, DATE, TIME, OFFICER, RESULT, TYPE)
            VALUES (?, ?, ?, ?, ?, ?, 'HR')
            """,
            (
                case["case_number"],
                hearing_number,
                hearing["hearing_date"],
                hearing["hearing_time"],
                hearing["hearing_officer"],
                hearing["appeared"],
            ),
        )
    curs.close()


def get_case_work_logs(case_ids):
    """
    Looks up CASE_WORK_LOGs by case_id and yields them.
    """

    if type(case_ids) is not list:
        # Handle a single case_id being requested
        case_ids = [case_ids]

    questions = ",".join(["?" for i in range(len(case_ids))])

    conn = sqlite3.connect("cases.db")
    conn.execute("pragma journal_mode=wal")
    conn.row_factory = sqlite3.Row

    curs = conn.cursor()
    curs.execute(f"SELECT * FROM CASE_WORK_LOG WHERE ID IN ({questions})", case_ids)
    for work_log in curs:
        yield dict(work_log)


def insert_case_work_logs(case_ids):
    """
    Inserts or marks CASE_WORK_LOGs so that they will be picked up and scraped.
    """
    if type(case_ids) is not list:
        # Handle a single case_id being requested
        case_ids = [case_ids]

    conn = sqlite3.connect("cases.db", isolation_level=None)
    conn.execute("pragma journal_mode=wal")
    curs = conn.cursor()
    curs.executemany(
        "INSERT INTO CASE_WORK_LOG (ID, NEEDS_WORK) VALUES (?, 1) ON CONFLICT (ID) DO UPDATE SET NEEDS_WORK=1",
        case_ids,
    )


def update_case_work_logs(case_ids):
    """
    Marks CASE_WORK_LOGs as worked.
    """
    if type(case_ids) is not list:
        # Handle a single case_id being requested
        case_ids = [case_ids]

    conn = sqlite3.connect("cases.db", isolation_level=None)
    conn.execute("pragma journal_mode=wal")
    curs = conn.cursor()
    curs.executemany("UPDATE CASE_WORK_LOG SET NEEDS_WORK = 0 WHERE ID = ?", case_ids)
