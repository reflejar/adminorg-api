import { Service } from '../../services/general';

let apiEndpoint = 'operative/estados/cuenta';

const get = (params) => async (dispatch) => {
  const path = `${apiEndpoint}/${params.destinatario}/?fecha=${params.fecha}`;

  const response = await Service.get(path);

  if (response && response.data) {
    dispatch({
      type: 'GET_STATUS_CUENTAS',
      payload: response.data
    });
  }
};

export const cuentasActions = {
  get
};
