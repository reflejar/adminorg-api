import set from 'lodash/set';
import qs from 'querystring';

import { Service } from '../../services/general';

let apiEndpoint = 'operative/documentos/cliente/';

export const FACTURAS_TYPES = {
  'factura_c': 11,
  'factura c': 11,
  'notas_de_debito': 12,
  'recibos_x': 54,
  'notas_de_credito': 13,
};

const get = (type, params) => async (dispatch) => {
  if (!type) {
    return null;
  }

  const query = qs.stringify({
    receipt__point_of_sales__number: params.points,
    receipt__receipt_number: params.id,
    receipt__issued_date_from: params.startDate,
    receipt__issued_date_to: params.endDate
  });

  const response = await Service.get(apiEndpoint + type + '/?' + query);

  if (response.data) {
    dispatch({
      type: 'GET_FACTURAS',
      payload: {
        data: response.data,
        type
      }
    });

  }

  return response.data;
};

const send = (payload) => async (dispatch) => {
  set(payload, 'receipt.point_of_sales', Number(payload.receipt.point_of_sales));

  const response = await Service.post(apiEndpoint + payload.receipt.receipt_type + '/', payload);

  if (response.status >= 400) throw response;

  if (response) {
    dispatch({
      type: 'SEND_FACTURAS',
      payload: response.data
    });
  }
};

export const facturasActions = {
  get,
  send,
  FACTURAS_TYPES
};
