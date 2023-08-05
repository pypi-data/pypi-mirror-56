from addok import core

class GetByIdView:

    def on_get(self, req, resp, _id):
        result = core.Result.from_id(_id)
        print(result.format())
        resp.status = 200
        resp.body = json.dumps(result.format())
        resp.content_type = 'application/json; charset=utf-8'

def register_http_endpoint(api):
  api.add_route('/id/{_id}', GetByIdView())
