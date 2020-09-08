import { Service } from '../../services/general';
import get from 'lodash/get';

let apiEndpoint = 'operative/parametros/interes/';

const search = (term) => ({
    type: 'SEARCH_INTERES',
    term
})

const select = (id) => ({
    type: 'SELECT_INTERES',
    id
})

const get_all = () => async (dispatch) => {
    const response = await Service.get(apiEndpoint);
    if (response) {
        const intereses = response.data.results.map(c => {
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
            type: 'GET_INTERESES',
            payload: intereses
        });
    }
}

const send = (values) => async (dispatch) => {

    let payload = {
      nombre: values.nombre,
      tipo: values.tipo,
      plazo: values.plazo,
      monto: values.monto,
      reconocimiento: values.reconocimiento,
      base_calculo: values.base_calculo
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
        type: 'POST_INTERES',
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



export const interesesActions = {
    get_all,
    search,
    select,
    send,
}
