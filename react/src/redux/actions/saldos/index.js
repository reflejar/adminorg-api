import { Service } from '../../services/general';

const apiEndpoint = 'operative/estados/saldos';

const get = (params) => async (dispatch) => {
  const path = `${apiEndpoint}/${params.destinatario}/?fecha=${params.fecha}`;

  const response = await Service.get(path);

  
  if (response && response.data) {
    if (typeof params.destinatario === "number" && params.capture) {
      dispatch({
        type: 'GET_SALDOS',
        payload: response.data
      });
    } 
    return response.data;

  }
};

export const saldosActions = {
  get
};