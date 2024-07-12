import uuid

from sanic import Sanic
from Service import GenerationService
from Mapper import UserMapper
from sanic.response import json
import json as js
from DTO.UserDTO import User

app = Sanic("MyApp")

generationService = GenerationService.GenerationService()
userMapper = UserMapper.UserMapper()

clients = []


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
    return json({'data': generationService.styles()})


@app.route('/add')
async def add(request):
    new_user = User(username='johndoe', password='securepassword', email='john.doe@example.com',
                    avatar='path/to/avatar.jpg')

    return json({'data': userMapper.add(new_user)})


@app.route('/get')
async def get(request):
    username = request.args.get('username')  # 获取查询参数username
    print(username)
    return json({'data': userMapper.get(username).to_dict()})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8765, debug=True)
