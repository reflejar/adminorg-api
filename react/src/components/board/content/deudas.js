import React from 'react';

import { useDeudas, useSaldos } from '../../../utility/hooks/dispatchers';
import Spinner from '../../spinner/spinner';

const Deudas = (props) => {
  const { selected, Table } = props;
  const [deudas, loadingDeudas] = useDeudas(true, selected);
  const [saldos, loadingSaldos] = useSaldos(true, selected);
  
  const data = [...saldos.map((saldo) => ({...saldo, monto: -saldo.monto, saldo: -saldo.saldo})), ...deudas];

  if (loadingDeudas || loadingSaldos) {
    return <Spinner />;
  }
  return (
    <Table data={data} selected={props.selected} />
  );
};

export default Deudas;