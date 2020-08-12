import React from 'react';

import { useEstadoCuenta } from '../../../utility/hooks/dispatchers';
import Spinner from '../../spinner/spinner';

const Cuenta = (props) => {
  const { selected, Table } = props;
  const [cuentas, loading] = useEstadoCuenta(selected);
  
  if (loading) {
    return <Spinner />;
  }
  return (
    <Table data={cuentas} selected={props.selected} />
  );
};

export default Cuenta;
