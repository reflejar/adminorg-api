import { Service } from '../../services/general';

const apiEndpoint = 'operative/parametros/titulo/';

const search = (term) => ({
  type: 'SEARCH_TITULO',
  payload: term
});

const select = item => ({
  type: 'SELECT_CONTABILIDAD',
  payload: item
});

const get_all = () => async (dispatch) => {

  const response = await Service.get(apiEndpoint);
  if (response) {
    const titulos = response.data.results.map(g => ({...g, full_name: g.nombre})).sort((a, b) => {
      let comparison = 0;
      if (a.numero > b.numero) {
        comparison = 1;
      } else if (a.numero < b.numero) {
        comparison = -1;
      }
      return comparison;
    });

    dispatch({
      type: 'GET_TITULOS',
      payload: titulos
    });

  }
};

const get_item = (id) => async (dispatch) => {
  const response = await Service.get(apiEndpoint + id);
  if (response && response.data) {
    const titulo = {
      ...response.data,
      full_name: response.data.perfil.apellido + ', ' + response.data.perfil.nombre
    }

    dispatch({
      type: 'GET_TITULO',
      payload: titulo
    });

    dispatch(select(titulo));
  }

  return response.data;
  
};

const send = (values) => async (dispatch) => {

  let payload = {
    supertitulo: values.supertitulo,
    nombre: values.nombre,
    numero: values.numero,
    predeterminado: values.predeterminado,
  };

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
      type: 'POST_TITULO',
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

export const titulosActions = {
  get_all,
  get_item,
  send,
  search,
  select,
};
