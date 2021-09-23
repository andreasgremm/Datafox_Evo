import datetime
from flask import (
    current_app,
    request,
    abort,
)
from influxdb import InfluxDBClient

from evodata import app


@app.route("/")
@app.route("/admin/evodata")
def evodata():
    args = request.args
    geraeteliste = [v for k, v in args.items() if "Ger" in k]
    if len(geraeteliste) > 0:
        geraet = geraeteliste[0]

    if request.remote_addr != current_app.config["EVODATA_IP"]:
        abort(403)  # Forbidden

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
    tags = {"System": geraet, "tag": args["Chip-Nr"]}
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

    checksum = args["checksum"]
    returnstatus = "status=ok&checksum=" + checksum + "\r\n"

    return returnstatus, 200


@app.route("/debug")
def debug():
    if request.remote_addr != current_app.config["DEBUG_HOST"]:
        abort(403)  # Forbidden
    influxdb_client = InfluxDBClient(
        current_app.config["INFLUXDB_HOST"],
        current_app.config["INFLUXDB_PORT"],
        current_app.config["INFLUXDB_USER"],
        current_app.config["INFLUXDB_PASSWORD"],
        current_app.config["INFLUXDB_DATABASE"],
    )
    querystring = 'SELECT * FROM "evodata"."autogen"."evodata_event" WHERE '
    whereclause = (
        "time >= '2021-09-23T18:30:00Z' AND time <= '2021-09-23T18:50:00Z'"
    )
    results = influxdb_client.query(querystring + whereclause)

    return results.raw, 200
