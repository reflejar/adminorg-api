import { Service } from '../../services/general';

const apiEndpoint = 'operative/plataformas/';

const get_all = () => async (dispatch) => {
  const response = await Service.get(apiEndpoint);

  if (response && response.data && response.data.results) {
    dispatch({ type: 'GET_PLATAFORMA', payload: response.data.results });
  }
};

export const plataformaActions = {
  get_all
};
