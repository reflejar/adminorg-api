import { Service } from '../../services/general';
import qs from 'querystring';

let apiEndpoint = 'operative/analitica/';

const search = (term) => ({
    type: 'SEARCH_ANALITICA',
    term
})

const select = (id) => ({
    type: 'SELECT_ANALITICA',
    id
})


const get_data = (params) => async (dispatch) => {

  const query = qs.stringify({
    cuenta__in: params.cuentas,
    start_date: params.startDate,
    end_date: params.endDate,
  });

  const response = await Service.get(apiEndpoint + '?' + query);

  if (response.data) {
    dispatch({
      type: 'GET_ANALITICA',
      payload: response.data.results
    });

  }

  return response.data.results;
};

export const analiticaActions = {
    get_data,
    search,
    select,
}
