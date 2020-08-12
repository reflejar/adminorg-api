import axios from 'axios';
import config from '../config/config';

const get = (apiEndpoint) => {
    return axios.get(config.baseUrl+apiEndpoint)
    .then((response) => {return response})
    .catch((err) => {console.log(err)});
}

const post = (apiEndpoint, payload) => {
    return axios.post(config.baseUrl + apiEndpoint, payload)
    .then((response) => { return response })
    .catch((err) => { console.log(err) });
}

export const authService = {
    get,
    post,
}
