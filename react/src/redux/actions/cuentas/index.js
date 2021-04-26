import { Service } from '../../services/general';

let apiEndpoint = 'operative/estados/cuenta';

const get = (params) => async (dispatch) => {
  let path = `${apiEndpoint}/${params.destinatario}/?end_date=${params.fecha}`;
  if (params.titulo) {
    path = path + `&titulo=${params.titulo}`
  }

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
