export const mapToParamsString = (params) => {
    let rare = ''
    params.forEach(function (item, key) {
        if (key === params.keys().next().value) {
            rare += '?' + key + '=' + item;
        } else {
            rare += '&' + key + '=' + item
        }
    })
    return rare
}