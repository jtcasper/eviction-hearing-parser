from io import StringIO
import csv

from flask import Flask, request, make_response, render_template
import persist

app = Flask(__name__)


@app.route("/")
def root():
    return app.send_static_file("index.html")


@app.route("/work_csv", methods=["POST"])
def work_csv():
    request_csv_file = request.files["file"]
    csv_bytes = request_csv_file.read()
    case_ids = [case_id.decode("utf-8") for case_id in csv_bytes.splitlines()]
    persist.insert_case_work_logs([(case_id,) for case_id in case_ids])
    work_rows = persist.get_case_work_logs(case_ids)
    return (render_template("work_csv.html", work_rows=work_rows), 202)


@app.route("/make_csv", methods=["POST"])
def make_csv():
    request_csv_file = request.files["file"]

    return_file = StringIO()
    headers_written = False

    csv_bytes = request_csv_file.read()

    for case_id in [case_id.decode("utf-8") for case_id in csv_bytes.splitlines()]:
        case = persist.get_case(case_id)
        if case is not None:
            if not headers_written:
                writer = csv.DictWriter(
                    return_file,
                    sorted(list((set(case.keys())) - {"hearings"})),
                    extrasaction="ignore",
                )
                writer.writeheader()
                headers_written = True
            writer.writerow(
                {**case,}
            )
    return (return_file.getvalue(), {"Content-Type": "text/csv; charset=utf-8"})


if __name__ == "__main__":
    app.run(debug=True)
