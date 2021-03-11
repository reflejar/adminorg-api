import { Service } from '../../services/general';
import qs from 'querystring';

let apiEndpoint = 'operative/informes/';

const search = (term) => ({
    type: 'SEARCH_INFORMES',
    term
})

const select = (id) => ({
    type: 'SELECT_INFORMES',
    id
})


const get_data = (params) => async (dispatch) => {

  const cuentas = params.cuentas.join();
  const receiptTypes = params.receiptTypes.join();
  dispatch({type: 'SET_INFORMES_LOADING',payload: true});
  
  params.fechas.forEach(async f => {
    const query = qs.stringify({
      cuenta__in: cuentas,
      start_date: f.start_date,
      end_date: f.end_date,
      documento__receipt__receipt_type__description__in: receiptTypes
    });
    const response = await Service.get(apiEndpoint + '?' + query);
    if (response.data) {
      dispatch({
        type: 'GET_INFORMES_DATA',
        payload: response.data.results
      });
      dispatch({type: 'SET_INFORMES_LOADING',payload: false});
    }
  });

  dispatch({
    type: 'SET_INFORMES_ALL_FILTERS',
    payload: params
  });


  return;
};




export const informesActions = {
    get_data,
    search,
    select,
}
