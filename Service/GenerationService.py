# 导入所需库
import random
from datetime import datetime
from DTO.RecordDTO import Record
import websocket  # NOTE: 需要安装websocket-client (https://github.com/websocket-client/websocket-client)
import json
import urllib.request
import urllib.parse
from Mapper.RecordMapper import RecordMapper
from PIL import Image
import io
from Util.AliOSS import AliOSS


def load_lora_styles(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        styles = json.load(file)

    for index, style in enumerate(styles):
        style['id'] = index

    return styles


class GenerationService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.styles = load_lora_styles("D:/PycharmProjects/summaryProject/styles.json")
            self.server_address = "127.0.0.1:8188"
            self.links = {}
            self.back_links = {}
            self.oss = AliOSS()
            self.recordMapper = RecordMapper()

    def link(self, client_id, ws):
        back_ws = websocket.WebSocket()
        back_ws.connect("ws://{}/ws?clientId={}".format(self.server_address, client_id))
        self.links[client_id] = ws
        self.back_links[client_id] = back_ws

    async def generate(self, data, user_id):
        prompt = json.load(open('prompt.json', encoding='utf-8'))
        # prefix()

        #
        # 翻译
        # key 提取
        # text = "adsfafd"
        text = data['text']

        prompt["PosCLIP"]["inputs"]["text"] = text
        prompt["NegCLIP"]["inputs"]["text"] = "text"
        prompt["Lora"]["inputs"]["strength_model"] = data['strength_model']
        prompt["Lora"]["inputs"]["strength_clip"] = data['strength_clip']
        prompt["KSampler"]["inputs"]["steps"] = data['steps']
        prompt["KSampler"]["inputs"]["cfg"] = data['cfg']
        prompt["KSampler"]["inputs"]["denoise"] = data['denoise']
        prompt["Latent"]["inputs"]["width"] = data['width']
        prompt["Latent"]["inputs"]["height"] = data['height']
        prompt["Latent"]["inputs"]["batch_size"] = data['batch_size']
        for s in self.styles:
            if s['id'] == data['style']:
                prompt["Lora"]["inputs"]["lora_name"] = s['styleName']
                break

        prompt_id = self.queue_prompt(prompt, user_id)['prompt_id']
        print(prompt_id)
        output_images = {}
        while True:
            out = self.back_links[user_id].recv()
            if isinstance(out, str):
                message = json.loads(out)
                if message['type'] == 'executing':
                    state_data = message['data']
                    if state_data['node'] is None and state_data['prompt_id'] == prompt_id:
                        await self.links[user_id].send(json.dumps({'type': 'state', 'data': "done"}))
                        break  # 执行完成
                await self.links[user_id].send(json.dumps({'type': 'state', 'data': message}))
            else:
                continue  # 预览是二进制数据

        history = self.get_history(prompt_id)[prompt_id]
        for node_id in history['outputs']:
            node_output = history['outputs'][node_id]
            if 'images' in node_output:
                for image in node_output['images']:
                    image_data = self.get_image(image['filename'], image['subfolder'], image['type'])
                    url = self.oss.uploadFile(image_data, datetime.now().strftime("%Y%m%d%H%M%S") + image['filename'])
                    new_record = Record(user_id=user_id, text=text, url=url, style=data['style'],
                                        generation_time=datetime.now(), strength_clip=data['strength_clip'],
                                        strength_model=data['strength_model'], steps=data['steps'], cfg=data['cfg'],
                                        denoise=data['denoise'], width=data['width'], height=data['height'],
                                        batch_size=data['batch_size'], conversation_id=data['conversation_id'])
                    self.recordMapper.add(new_record)
                    await self.links[user_id].send(json.dumps({'type': 'image', 'data': url}))
                    # image = Image.open(io.BytesIO(image_data))
                    # image.show()

    def queue_prompt(self, prompt, client_id):
        print('queue')
        prompt["KSampler"]["inputs"]["seed"] = random.randint(100000000, 1000000000000)
        p = {"prompt": prompt, "client_id": client_id}
        data = json.dumps(p).encode('utf-8')
        req = urllib.request.Request("http://{}/prompt".format(self.server_address), data=data)
        return json.loads(urllib.request.urlopen(req).read())

    # 定义从服务器下载图像数据的函数
    def get_image(self, filename, subfolder, folder_type):
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        url_values = urllib.parse.urlencode(data)
        with urllib.request.urlopen("http://{}/view?{}".format(self.server_address, url_values)) as response:
            return response.read()

    # 定义获取历史记录的函数
    def get_history(self, prompt_id):
        with urllib.request.urlopen("http://{}/history/{}".format(self.server_address, prompt_id)) as response:
            return json.loads(response.read())

    # 显示输出图像（这部分已注释掉）
    # Commented out code to display the output images:
    #
    # for node_id in images:
    #     for image_data in images[node_id]:
    #
    #         image = Image.open(io.BytesIO(image_data))
    #         image.show()
    def generation_history(self, username):
        return self.recordMapper.get_history(username)
