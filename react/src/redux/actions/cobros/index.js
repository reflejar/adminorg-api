import { Service } from '../../services/general';

const apiEndpoint = 'operative/documentos/cliente/54/';

const send = (payload) => async () => {
  const response = await Service.post(apiEndpoint, payload);

  return response.data;
};

export const cobrosActions = {
  send
};

