import xetrapal
import pandas
from xetrapal import gdastras
from arango import ArangoClient

a = xetrapal.karma.load_xpal_smriti("/opt/av-appdata/avxpal.json")
avxpal = xetrapal.Xetrapal(a)
config = xetrapal.karma.load_config_json(a.configfile)
pygsheetsconfig = xetrapal.karma.load_config_json(
    config['Pygsheets']['avdrive'])
gd = gdastras.gd_get_googledriver(pygsheetsconfig)
client = ArangoClient(hosts="http://localhost:8529")
db = client.db("LinkedIn-AV", username="root", password="theansweris42")
graph = db.graph("linkedinav")
nodes = graph.vertex_collection("nodes")
edges = graph.edge_collection("edges")
