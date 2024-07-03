<script setup>
import {ref} from "@vue/reactivity";
import {generateService, getStylesService} from "@/api/operate.js";

const styles = ref([])

const generateData = ref({
  pos_des: '',
  neg_des: '',
  style: 0,
  steps: 30,
  cfg: 4,
  strength_model: 0.7,
  strength_clip: 0.7,
  denoise: 1,
  width: 1024,
  height: 768,
  batch_size: 1
})

const getStyles = async () => {
  let result = await getStylesService()
  console.log(result.data)
  styles.value = result.data
  await connect()
}

getStyles()

const generate = async () => {
  // console.log(generateData.value)
  client.send(JSON.stringify(generateData.value))
  // let result = await generateService(generateData.value);
  // console.log(result)
}

let client
const imageUrl = ref('')
const state = ref('ready')
const connect = async () => {
  client = new WebSocket('ws://localhost:8899/connect');
  client.onmessage = (event) => {
    if (typeof event.data === "string") {
      let data = JSON.parse(event.data)
      console.log(data)
      state.value = data.data.type
      if (state.value === 'progress') state.value += ' ' + data.data.data.value + '/' + data.data.data.max
    } else {
      const blob = new Blob([event.data], {type: 'image/png'});
      // 创建 URL 对象
      imageUrl.value = URL.createObjectURL(blob);
    }
  };
  client.onopen = () => {
    console.log('WebSocket connected');
  };
  client.onerror = (error) => {
    console.error('WebSocket Error:', error);
  };
}

</script>

<script>
</script>

<template>
  <div style="width: 1500px;height: 1000px;margin-top: 100px">
    <div style="width: 100%;height: 100px;display: flex;flex-direction: row;justify-content: space-around">
      <div style="width: 600px;height: 100px">
        <el-text>positive description</el-text>
        <el-input v-model="generateData.pos_des" placeholder="input your description for image here"></el-input>
      </div>
      <div style="width: 600px;height: 100px">
        <el-text>negative description</el-text>
        <el-input v-model="generateData.neg_des" placeholder="input something you do not want to see here"></el-input>
      </div>
    </div>
    <div style="width: 100%;height: 100px;display: flex;flex-direction: row;justify-content: space-around">
      <div style="width: 200px;height: 20px">
        <el-text>steps</el-text>
        <el-input v-model="generateData.steps"></el-input>
      </div>
      <div style="width: 200px;height: 20px">
        <el-text>cfg</el-text>
        <el-input v-model="generateData.cfg"></el-input>
      </div>
      <div style="width: 200px;height: 20px">
        <el-text>strength_model</el-text>
        <el-input v-model="generateData.strength_model"></el-input>
      </div>
      <div style="width: 200px;height: 20px">
        <el-text>strength_clip</el-text>
        <el-input v-model="generateData.strength_clip"></el-input>
      </div>
    </div>
    <div style="width: 100%;height: 100px;display: flex;flex-direction: row;justify-content: space-around">
      <div style="width: 200px;height: 20px">
        <el-text>denoise</el-text>
        <el-input v-model="generateData.denoise"></el-input>
      </div>
      <div style="width: 200px;height: 20px">
        <el-text>batch_size</el-text>
        <el-input v-model="generateData.batch_size"></el-input>
      </div>
      <div style="width: 200px;height: 20px">
        <el-text>width</el-text>
        <el-input v-model="generateData.width"></el-input>
      </div>
      <div style="width: 200px;height: 20px">
        <el-text>height</el-text>
        <el-input v-model="generateData.height"></el-input>
      </div>
    </div>
    <div
        style="width: 1000px;height: 50px;margin: auto;display: flex;flex-direction: row;justify-content: space-around">
      <div style="width: 500px;height: 50px;">
        <el-text>style</el-text>
        <el-select placeholder="please choose style of image" v-model="generateData.style">
          <el-option
              v-for="s in styles"
              :key="s.id"
              :label="s.styleLabel"
              :value="s.id"
          >
          </el-option>
        </el-select>
      </div>
      <div style="width: 100px;float: right">
        <el-button style="width: 100%" @click='generate'>
          Generate
        </el-button>
      </div>
    </div>
    <div style="width: 600px;height: 50px;margin: 20px auto 0 auto;">
      <el-text>state</el-text>
      <el-text style="margin-left: 50px">{{ state }}</el-text>
    </div>
    <div style="width: 1648px;margin:auto">
      <img :src="imageUrl">
    </div>
  </div>
</template>

<style scoped>

</style>
