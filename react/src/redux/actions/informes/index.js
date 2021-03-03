import { Service } from '../../services/general';
import qs from 'querystring';

let apiEndpoint = 'operative/informes/';

const search = (term) => ({
    type: 'SEARCH_ANALITICA',
    term
})

const select = (id) => ({
    type: 'SELECT_ANALITICA',
    id
})


const get_data = (params) => async (dispatch) => {

  const cuentas = params.cuentas.join();
  const receiptTypes = params.receiptTypes.join();
  
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
        type: 'GET_AN_DATA',
        payload: response.data.results
      });
    }
  });

  console.log(params);
  dispatch({
    type: 'SET_AN_ALL_FILTERS',
    payload: params
  });




  return;
};




export const informesActions = {
    get_data,
    search,
    select,
}
