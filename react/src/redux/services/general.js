import axios from 'axios';
import config from '../config/config';


const initialHeaders = () => ({
    'Content-Type': 'application/json',
    'Authorization': 'Token ' + localStorage.getItem('token'),
})

const get = (apiEndpoint) => {
    let headers = initialHeaders();
    return axios.get(config.baseUrl+apiEndpoint, { headers })
    .then((response) => {return response})
}

const remove = (apiEndpoint) => {
    let headers = initialHeaders();
    return axios.delete(config.baseUrl+apiEndpoint, { headers })
    .then((response) => {return response})
    .catch((err) => { return err.response });
}

const post = (apiEndpoint, payload) => {
    let headers = initialHeaders();
    return axios.post(config.baseUrl + apiEndpoint, payload, { headers })
    .then((response) => { return response })
    .catch((err) => { return err.response });
}

const postMultiData = (apiEndpoint, payload) => {
    let headers = initialHeaders();
    headers['Content-Type'] = 'multipart/form-data';
    return axios.post(config.baseUrl + apiEndpoint, payload, { headers })
    .then((response) => { return response })
    .catch((err) => { return err.response });
}

const put = (apiEndpoint, payload) => {
    let headers = initialHeaders();
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
