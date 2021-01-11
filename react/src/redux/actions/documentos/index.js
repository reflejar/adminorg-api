import set from 'lodash/set';
import qs from 'querystring';

import { Service } from '../../services/general';

let apiEndpoint = 'operative/documentos/';

const get = (type, id) => async (dispatch) => {
  if (!type) {
    return null;
  }  
  const response = await Service.get(`${apiEndpoint}${type}/${id}/`);

  if (response && response.data) {
    dispatch({
      type: 'GET_DOCUMENTO',
      payload: response.data
    });

    return response.data;
  }
};

const getList = (type, params) => async (dispatch) => {
  if (!type) {
    return null;
  }

  const query = qs.stringify({
    receipt__receipt_type__description: params.receipt_type,
    receipt__point_of_sales__number: params.point,
    receipt__receipt_number: params.numero,
    receipt__issued_date_from: params.startDate,
    receipt__issued_date_to: params.endDate,
  });

  const response = await Service.get(apiEndpoint + type + '/?' + query);

  if (response.data) {
    dispatch({
      type: 'GET_DOCUMENTOS',
      payload: response.data.results
    });

  }

  return response.data.results;
};

const send = (type, payload) => async (dispatch) => {
  set(payload, 'receipt.point_of_sales', Number(payload.receipt.point_of_sales));
  let endpoint = apiEndpoint + type + "/";
  if ("distribuciones" in payload) {
    endpoint = endpoint + "masivo/"
  }
  if (payload.id) {
    const response = await Service.put(endpoint + payload.id + "/", payload)
    if (response.status >= 400) throw response;  
  } else {
    const response = await Service.post(endpoint, payload);
    if (response.status >= 400) throw response;
  }

  

};

const remove = (type, payload) => async (dispatch) => {
  const endpoint = apiEndpoint + type + "/" + payload + "/";
  const response = await Service.remove(endpoint);
  if (response.status >= 400) throw response.data[0];
  
};

export const documentosActions = {
  get,
  getList,
  send,
  remove,
};
