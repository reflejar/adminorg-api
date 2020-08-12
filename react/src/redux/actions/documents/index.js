import { Service } from '../../services/general';

const apiEndpoint = 'operative/documentos/cliente';

const get = (id) => async (dispatch) => {
  const response = await Service.get(`${apiEndpoint}/${id}/`);

  if (response && response.data) {
    dispatch({
      type: 'GET_DOCUMENT',
      payload: response.data
    });

    return response.data;
  }
};

const send = (type, values) => async (dispatch) => {
  const response = await Service.post(`${apiEndpoint}/${type}`, values);

  if (response && response.data) {
    dispatch({
      type: 'SET_DOCUMENT',
      payload: response.data
    });

    return response.data;
  }
};


export const documentsActions = {
  get,
  send
};
