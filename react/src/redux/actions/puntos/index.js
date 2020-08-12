import { Service } from '../../services/general';

let apiEndpoint = 'operative/parametros/punto/';

const get_all = () => async (dispatch) => {
  const response = await Service.get(apiEndpoint);

  if (response) {
    dispatch({ type: 'GET_PUNTOS', payload: response.data});
  }
};


export const puntosActions = {
  get_all
};
