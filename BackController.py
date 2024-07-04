import uuid

from sanic import Sanic
from sanic.response import json
import json as js
import ComfyUIApi

app = Sanic("MyApp")

apiService = ComfyUIApi.ApiService()

clients = []


@app.websocket("/connect")
async def connect(request, ws):
    client_id = str(uuid.uuid4())
    apiService.link(client_id, ws)
    while True:
        data = await ws.recv()
        data = js.loads(data)
        print("Received:", data)
        await apiService.generate(data, client_id)


@app.route('/styles')
async def styles(request):
    return json({'data': apiService.styles})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8899)
