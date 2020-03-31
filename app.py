from subprocess import PIPE, run
from flask import Flask, request
from flask_restful import Resource, Api
app = Flask(__name__)
api = Api(app)


class build(Resource):
    def post(self,file):
        resp = run(f'docker-compose -f {file} build', stdout=PIPE, stderr=PIPE, universal_newlines=True)
        print(resp)
        return {"build": f'{"ok" if not resp.returncode else resp.stderr}'}

class up(Resource):
    def post(self,file,detach):
        detach = True if detach =="true" else False
        resp = run(f'docker-compose -f {file} up {"-d" if detach else ""}', stdout=PIPE, stderr=PIPE, universal_newlines=True)
        return {"up": f'{"ok" if not resp.returncode else resp.stderr}'}


api.add_resource(build, '/build/<string:file>')
api.add_resource(up, '/up/<string:file>/detach/<string:detach>')

if __name__ == '__main__':
    app.run()
