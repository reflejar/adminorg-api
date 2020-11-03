import axios from 'axios';
import config from '../config/config';


let headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Token ' + localStorage.getItem('token'),
}

const get = (apiEndpoint) => {
    return axios.get(config.baseUrl+apiEndpoint, { headers })
    .then((response) => {return response})
}

const remove = (apiEndpoint) => {
    return axios.delete(config.baseUrl+apiEndpoint, { headers })
    .then((response) => {return response})
    .catch((err) => { return err.response });
}

const post = (apiEndpoint, payload) => {
    return axios.post(config.baseUrl + apiEndpoint, payload, { headers })
    .then((response) => { return response })
    .catch((err) => { return err.response });
}

const postMultiData = (apiEndpoint, payload) => {
    headers['Content-Type'] = 'multipart/form-data';
    return axios.post(config.baseUrl + apiEndpoint, payload, { headers })
    .then((response) => { return response })
    .catch((err) => { return err.response });
}

const put = (apiEndpoint, payload) => {
    return axios.put(config.baseUrl + apiEndpoint, payload, { headers })
    .then((response) => { return response })
    .catch((err) => { return err.response });
}

export const Service = {
    get,
    remove,
    post,
    put,
    postMultiData,
}
