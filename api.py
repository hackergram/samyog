from flask import Flask, request
from flask import jsonify
import xetrapal
import pandas
from xetrapal import gdastras
from arango import ArangoClient
import copy


a = xetrapal.karma.load_xpal_smriti("/opt/av-appdata/avxpal.json")
avxpal = xetrapal.Xetrapal(a)
config = xetrapal.karma.load_config_json(a.configfile)
pygsheetsconfig = xetrapal.karma.load_config_json(
    config['Pygsheets']['avdrive'])
gd = gdastras.gd_get_googledriver(pygsheetsconfig)
client = ArangoClient()
db = client.db("LinkedIn-AV", username="root", password="theansweris42")
graph = db.graph("linkedinav")
nodes = graph.vertex_collection("nodes")
edges = graph.edge_collection("edges")

app = Flask(__name__)
resp = {
    "resp": None,
    "status": "error"
}


def strip_junk(answer):
    answer = {k: v for k, v in answer.items() if k not in ['_id', '_rev']}
    return answer


@app.route('/hello/', methods=['GET', 'POST'])
def welcome():
    return jsonify({
        "story": "Hello World!",
        "status": "success"
    })


@app.route('/nodes/', methods=['GET', 'POST'])
def get_nodes():
    myresp = copy.deepcopy(resp)
    if request.method == "GET":
        if request.args.get("id") is not None:
            try:
                answer = strip_junk(dict(nodes.get(request.args.get("id"))))
                myresp['resp'] = [answer]
                myresp['status'] = "success"
            except Exception as e:
                myresp['resp'] = [str(e)]
                resp['status'] = "error"
        else:
            myresp['resp'] = [nodes.all().count()]
            myresp['status'] = "success"
    if request.method == "POST":
        try:
            nodes.update(request.json)
            p = strip_junk(nodes.get(request.json['_key']))
            myresp['resp'] = [p]
            myresp['status'] = "success"
        except Exception as e:
            myresp['resp'] = [str(e)]
            resp['status'] = "error"

    return jsonify(myresp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010)
