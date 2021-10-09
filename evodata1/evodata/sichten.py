import datetime
from flask import (
    current_app,
    request,
    abort,
)
from influxdb import InfluxDBClient

from evodata import app, basic_auth


@app.route("/")
@basic_auth.required
def evodata():
    args = request.args
    influxdb_client = InfluxDBClient(
        current_app.config["INFLUXDB_HOST"],
        current_app.config["INFLUXDB_PORT"],
        current_app.config["INFLUXDB_USER"],
        current_app.config["INFLUXDB_PASSWORD"],
        current_app.config["INFLUXDB_DATABASE"],
    )

    retention_policy = None
    influxdb_data = []
    measurement = "evodata_event"
    fields = {"status": 1}
    try:
        geraeteliste = [v for k, v in args.items() if "Ger" in k]
        tags = {"System": geraeteliste[0], "tag": args["Chip-Nr"]}
        checksum = args["checksum"]
    except Exception:
        returnstatus = "status=not_ok\r\n"
        return returnstatus, 418
    timestamp = datetime.datetime.utcnow().isoformat()

    data_point = {
        "measurement": measurement,
        "tags": tags,
        "time": timestamp,
        "fields": fields,
    }
    influxdb_data.append(data_point)
    # print("Data: ", influxdb_data, flush=True)
    influxdb_client.write_points(
        influxdb_data, retention_policy=retention_policy
    )
    returnstatus = "status=ok&checksum=" + checksum + "\r\n"
    return returnstatus, 200


@app.route("/debug")
@basic_auth.required
def debug():
    influxdb_client = InfluxDBClient(
        current_app.config["INFLUXDB_HOST"],
        current_app.config["INFLUXDB_PORT"],
        current_app.config["INFLUXDB_USER"],
        current_app.config["INFLUXDB_PASSWORD"],
        current_app.config["INFLUXDB_DATABASE"],
    )
    querystring = 'SELECT * FROM "evodata"."autogen"."evodata_event" WHERE '
    whereclause = (
        "time >= '2021-09-23T18:30:00Z' AND time <= '2021-12-23T18:50:00Z'"
    )
    results = influxdb_client.query(querystring + whereclause)

    return results.raw, 200
