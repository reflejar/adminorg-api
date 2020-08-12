import { useSelector } from 'react-redux';
import get from 'lodash/get';

export const useClientInstance = () => {
  return useSelector((state) => get(state, 'clientes.instance', null));
};

export const useClientList = () => {
  return useSelector((state) => get(state, 'clientes.list', []));
};
