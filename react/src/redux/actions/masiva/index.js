import { Service } from '../../services/general';

const apiEndpoint = 'operative/documentos/cliente/11/masivo/';

const post = (data) => async (dispatch) => {
  const response = await Service.post(apiEndpoint, data);

  if (response && response.data) {
    dispatch({ type: 'SEND_FACTURACION_MASIVA', payload: response.data });
  }
};


export const masivaActions = {
  post
};
