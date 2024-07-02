import request from "@/utils/request.js";
import {mapToParamsString} from "@/utils/ParameterFormat.js";
export const generateService = (data) => {
    console.log(data)
    return request.post('/generate', data)
}
export const getStylesService = () => {
    return request.get('/styles')
}
