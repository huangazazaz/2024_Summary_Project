import uuid

from sanic import Sanic
from Service import GenerationService
from Service import OtherService
from sanic.response import json
import json as js
from Service.UserService import UserService

app = Sanic("MyApp")

generationService = GenerationService.GenerationService()
userService = UserService()
otherService = OtherService.OtherService()

clients = []


# generation ===========================================

@app.websocket("/connect")
async def connect(request, ws):
    user_id = request.json.get("user_id")
    generationService.link(user_id, ws)
    while True:
        data = await ws.recv()
        data = js.loads(data)
        print("Received:", data)
        await generationService.generate(data, user_id)


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


# other ===========================================


@app.route('/update_setting', methods=["POST"])
async def update_setting(request):
    data = request.json
    setting = data.get("setting", {})
    return await otherService.update_setting(setting)


@app.route('/get_setting/<username>')
async def get_setting(request, username):
    return otherService.get_setting(username)


# =============================================


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8765, debug=True)
