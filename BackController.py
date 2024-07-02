from sanic import Sanic
import sanic.response as sr
import uuid
import json
import urllib.request
import urllib.parse

app = Sanic("MyApp")
server_address = "127.0.0.1:8188"
client_id = str(uuid.uuid4())


@app.route('/')
async def test(request):
    return sr.json({"info": "visit /image to get picture"})


@app.route('/image')
async def image(request):

    prompt = json.load(open('test.json', encoding='utf-8'))
    data = json.dumps(prompt).encode('utf-8')
    req = urllib.request.Request("http://{}/prompt".format(server_address), data=data)
    prompt_id = json.loads(urllib.request.urlopen(req).read())['prompt_id']
    return sr.json({"id": prompt_id})


@app.route('/history/<prompt_id>')
async def history(request, prompt_id):
    with urllib.request.urlopen("http://{}/history/{}".format(server_address, prompt_id)) as response:
        return json.loads(response.read())


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8899)
