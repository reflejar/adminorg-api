import React from 'react';

import { useEstadoCuenta } from '../../../utility/hooks/dispatchers';
import Spinner from '../../spinner/spinner';

const Cuenta = (props) => {
  const { selected, Table } = props;
  const [cuentas, loading] = useEstadoCuenta(selected);
  
  if (loading) {
    return (
    <div className='loading-modal'>
      <Spinner />
    </div>
    );
  }
  return (
    <Table data={cuentas} selected={selected} />
  );
};

export default Cuenta;
