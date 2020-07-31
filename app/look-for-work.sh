#!/bin/bash
sqlite3 cases.db 'select id from case_work_log where needs_work = 1' \
    | split --filter='MOZ_HEADLESS=1 python scrape_worker.py' -
