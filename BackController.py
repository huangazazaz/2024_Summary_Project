import uuid

from sanic import Sanic
from Service import GenerationService
from sanic.response import json
import json as js
from Service.UserService import UserService

app = Sanic("MyApp")

generationService = GenerationService.GenerationService()
userService = UserService()

clients = []


# generation ===========================================

@app.websocket("/connect")
async def connect(request, ws):
    client_id = str(uuid.uuid4())
    generationService.link(client_id, ws)
    while True:
        data = await ws.recv()
        data = js.loads(data)
        print("Received:", data)
        await generationService.generate(data, client_id)


@app.route('/styles')
async def styles(request):
    return json({'data': generationService.styles})


@app.route('/history/<username>')
async def history(request, username):
    return json({'data': generationService.generation_history(username)})


# =============================================

# user ===========================================


@app.route('/register', methods=["POST"])
async def register(request):
    return await userService.register(request)


@app.route('/login', methods=["POST"])
async def login(request):
    return await userService.login(request)


# =============================================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8765, debug=True)
