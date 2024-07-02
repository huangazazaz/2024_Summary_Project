# 导入所需库
import websocket  # NOTE: 需要安装websocket-client (https://github.com/websocket-client/websocket-client)
import uuid
import json
import urllib.request
import urllib.parse


class ApiService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.styles = [
                {
                    'id': 0,
                    'styleLabel': 'person',
                    'styleName': 'V3-1GIRL-人像LoRA-MIST-AiARTiST_1GIRL.safetensors'
                },
                {
                    'id': 1,
                    'styleLabel': 'post',
                    'styleName': 'V3-艺术海报构图设计LoRA-CADS-AiARTiST_测试版.safetensors'
                }
            ]
            self.server_address = "127.0.0.1:8188"
            self.links = {}
            self.back_links = {}

    def link(self, client_id, ws):
        back_ws = websocket.WebSocket()
        back_ws.connect("ws://{}/ws?clientId={}".format(self.server_address, client_id))
        self.links[client_id] = ws
        self.back_links[client_id] = back_ws

    async def generate(self, pos_text, neg_text, style, client_id):
        prompt = json.load(open('prompt.json', encoding='utf-8'))
        prompt["PosCLIP"]["inputs"]["text"] = pos_text
        prompt["NegCLIP"]["inputs"]["text"] = neg_text
        for s in self.styles:
            if s['id'] == style:
                prompt["Lora"]["inputs"]["lora_name"] = s['styleName']
                break
        await self.get_images(prompt, client_id)

    def queue_prompt(self, prompt, client_id):
        print('queue')
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

    # 定义通过WebSocket接收消息并下载图像的函数
    async def get_images(self, prompt, client_id):
        prompt_id = self.queue_prompt(prompt, client_id)['prompt_id']
        print(prompt_id)
        output_images = {}
        while True:
            out = self.back_links[client_id].recv()
            if isinstance(out, str):
                message = json.loads(out)
                if message['type'] == 'executing':
                    data = message['data']
                    if data['node'] is None and data['prompt_id'] == prompt_id:
                        await self.links[client_id].send(json.dumps({'type': 'state', 'data': "done"}))
                        break  # 执行完成
                await self.links[client_id].send(json.dumps({'type': 'state', 'data': message['type']}))
            else:
                continue  # 预览是二进制数据

        history = self.get_history(prompt_id)[prompt_id]
        for node_id in history['outputs']:
            node_output = history['outputs'][node_id]
            if 'images' in node_output:
                images_output = []
                for image in node_output['images']:
                    image_data = self.get_image(image['filename'], image['subfolder'], image['type'])
                    images_output.append(image_data)
                output_images[node_id] = images_output
        for node_id in output_images:
            for image_data in output_images[node_id]:
                from PIL import Image
                import io
                await self.links[client_id].send(image_data)
                image = Image.open(io.BytesIO(image_data))
                image.show()
        return output_images

    # 显示输出图像（这部分已注释掉）
    # Commented out code to display the output images:
    #
    # for node_id in images:
    #     for image_data in images[node_id]:
    #         from PIL import Image
    #         import io
    #
    #         image = Image.open(io.BytesIO(image_data))
    #         image.show()
