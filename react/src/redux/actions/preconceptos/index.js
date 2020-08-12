import { Service } from '../../services/general';

const apiEndpoint = 'operative/preconceptos/';

const get_all = () => async (dispatch) => {
  try {
    const response = await Service.get(apiEndpoint);

    dispatch({ type: 'GET_PRECONCEPTOS_PENDING' });

    if (response && response.data) {
      dispatch({
        type: 'GET_PRECONCEPTOS_SUCCESSFULLY',
        payload: response.data
      });
    }
  } catch (error) {
    dispatch({ type: 'GET_PRECONCEPTOS_ERROR', payload: error });
  } finally {
    dispatch({ type: 'GET_PRECONCEPTOS_FINISHED' });
  }
};

const post = (data) => async (dispatch) => {
  const response = await Service.post(apiEndpoint, data);

  if (response && response.data) {
    dispatch({ type: 'SEND_PRECONCEPTOS', payload: response.data });
  }
};

const remove = (id) => async (dispatch) => {
  const response = await Service.remove(`${apiEndpoint}${id}/`);

  if (response && response.status >= 200 && response.status < 300) {
    dispatch({ type: 'DELETE_PRECONCEPTO', payload: id });
  }
};

export const preconceptosActions = {
  get_all,
  post,
  remove
};
