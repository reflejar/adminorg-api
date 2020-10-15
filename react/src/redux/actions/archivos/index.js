import { Service } from '../../services/general';

const apiEndpoint = 'files/archivos/';

const search = (term) => ({
  type: 'SEARCH_ARCHIVO',
  payload: term
});

const select = item => ({
  type: 'SELECT_ANALITICA',
  payload: item
});

const get_all = () => async (dispatch) => {

  const response = await Service.get(apiEndpoint);
  if (response) {
    const archivos = response.data.results.map(g => ({...g, full_name: g.nombre}));

    dispatch({
      type: 'GET_ARCHIVOS',
      payload: archivos
    });

  }
};

const get_item = (id) => async (dispatch) => {
  const response = await Service.get(apiEndpoint + id);
  if (response && response.data) {
    const archivo = {
      ...response.data,
      full_name: response.data.perfil.apellido + ', ' + response.data.perfil.nombre
    }

    dispatch({
      type: 'GET_ARCHIVO',
      payload: archivo
    });

    dispatch(select(archivo));
  }

  return response.data;
  
};

const send = (values) => async (dispatch) => {

  let payload = {...values};

  let response;

  if (values.id) {
    response = await Service.put(apiEndpoint + values.id + '/', payload);
    await dispatch(get_all());
    return;
  } else {
    response = await Service.post(apiEndpoint, payload);
  }

  if (response) {
    await dispatch(get_all())
    await dispatch({
      type: 'POST_ARCHIVO',
      payload: response.data
    });
    response.result = 'success'
  } else {
    response = {
      result: 'error'
    }
  }


  return response
};

export const archivosActions = {
  get_all,
  get_item,
  send,
  search,
  select,
};
