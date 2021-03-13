from flask import Flask, request
from flask import jsonify
from arango import ArangoClient
import json
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS
confjson = {}
with open("/home/arjun/api.json", "rb") as f:
    confjson = json.loads(f.read())


client = ArangoClient()
db = client.db(confjson['dbname'], username=confjson['username'], password=confjson['password'])
graph = db.graph(confjson['graphname'])


app = Flask(__name__)
CORS(app)
api = Api(app)

resp = {
    "resp": None,
    "status": "error"
}


def strip_junk(answer):
    answer = {k: v for k, v in answer.items() if k not in ['_id', '_rev']}
    return answer


# Collections CRUD
class Collections(Resource):
    def get(self, collection_name=None):
        if collection_name is not None:
            count = graph.vertex_collection(collection_name).count()
            return jsonify({
                "resp": [{
                    "count": count,
                    "collection_name": collection_name
                }],
                "status": "success"
            })
        else:
            return jsonify({
                "resp": [{
                    "count": graph.vertex_collection(x).count(),
                    "collection_name": x
                } for x in graph.vertex_collections()],
                "status": "success"
            })
    def post(self, collection_name=None):
        if collection_name is not None:
            try:
                graph.create_vertex_collection(collection_name)
                return jsonify({
                    
                })


api.add_resource(Collections, '/collections/<collection_name>', '/collections', '/collections/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010)
