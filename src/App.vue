<script setup>
import {ref} from "@vue/reactivity";
import {generateService, getStylesService} from "@/api/operate.js";

const styles = ref([])

const generateData = ref({
  pos_des: '',
  neg_des: '',
  style: ''
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
      state.value = data.data
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
        <el-input v-model="generateData.pos_des" placeholder="input your description for image here"></el-input>
      </div>
      <div style="width: 600px;height: 100px">
        <el-input v-model="generateData.neg_des" placeholder="input something you do not want to see here"></el-input>
      </div>
    </div>
    <div
        style="width: 1000px;height: 50px;margin: auto;display: flex;flex-direction: row;justify-content: space-around">
      <div style="width: 500px;height: 50px;">
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
      <div style="width: 100px;;float: right">
        <el-button style="width: 100%" @click='generate'>
          Generate
        </el-button>
      </div>
    </div>
    <div style="width: 600px;height: 50px;margin: auto">
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
