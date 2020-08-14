#!/bin/bash
# seconds_in_a_week = 604800
sqlite3 cases.db "select id from case_work_log where updated_timestamp < strftime('%s', 'now') - 604800 LIMIT 100" \
    | MOZ_HEADLESS=1 /opt/eviction-hearing-parser/venv/bin/python /opt/eviction-hearing-parser/app/scrape_worker.py &
sqlite3 cases.db 'select id from case_work_log where needs_work = 1' \
    | split --lines=100 --filter='MOZ_HEADLESS=1 /opt/eviction-hearing-parser/venv/bin/python /opt/eviction-hearing-parser/app/scrape_worker.py' -
