import { Service } from '../../services/general';
import get from 'lodash/get';

let apiEndpoint = 'operative/parametros/descuento/';

const search = (term) => ({
    type: 'SEARCH_DESCUENTO',
    term
})

const select = (id) => ({
    type: 'SELECT_DESCUENTO',
    id
})

const get_all = () => async (dispatch) => {
    const response = await Service.get(apiEndpoint);
    if (response) {
        const descuentos = response.data.results.map(c => {
          let full_name = get(c, 'nombre', "");
          return ({...c, full_name})
      }).sort((a, b) => {
            let comparison = 0;
            if (a.numero > b.numero) {
                comparison = 1;
            } else if (a.numero < b.numero) {
                comparison = -1;
            }
            return comparison;
        });

        dispatch({
            type: 'GET_DESCUENTOS',
            payload: descuentos
        });
    }
}

const send = (values) => async (dispatch) => {

    let payload = {
      nombre: values.nombre,
      tipo: values.tipo,
      plazo: values.plazo,
      monto: values.monto,
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
        type: 'POST_DESCUENTO',
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




export const descuentosActions = {
    get_all,
    search,
    select,
    send,
}
