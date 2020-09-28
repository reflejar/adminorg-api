import { Service } from '../../services/general';

let apiEndpoint = 'operative/parametros/gasto/';

const search = (term) => ({
    type: 'SEARCH_GASTO',
    term
})

const select = (id) => ({
    type: 'SELECT_GASTO',
    id
})

const get_all = () => async (dispatch) => {
    const response = await Service.get(apiEndpoint);
    if (response) {
        const gastos = response.data.results.map(g => ({...g, full_name: g.nombre})).sort((a, b) => {
            let comparison = 0;
            if (a.nombre > b.nombre) {
                comparison = 1;
            } else if (a.nombre < b.nombre) {
                comparison = -1;
            }
            return comparison;
        });

        dispatch({
            type: 'GET_GASTOS',
            payload: gastos
        });
    }
}

const send = (values) => async (dispatch) => {

    let payload = {
      ...values
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
        type: 'POST_GASTO',
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



export const gastosActions = {
    get_all,
    search,
    select,
    send,
}
