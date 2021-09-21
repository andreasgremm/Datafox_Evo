import encodings
from flask import (
    current_app,
    request,
    abort,
)
from evodata import app


@app.route("/")
@app.route("/index")
@app.route("/admin/evodata")
def index():
    args = request.args
    geraeteliste = [v for k, v in args.items() if "Ger" in k]
    if len(geraeteliste) > 0:
        geraet = geraeteliste[0]
        print(geraet)

    if request.remote_addr != current_app.config["EVODATA_IP"]:
        abort(403)  # Forbidden

    checksum = args["checksum"]
    returnstatus = "status=ok&checksum=" + checksum + "\r\n"

    return returnstatus, 200
