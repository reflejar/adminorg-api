import React from 'react';

import { facturasTypes } from '../_options/receipt_types';
import LStep from '../../../CRUDL/documento/L';

const L = () => {

  return (
    <LStep 
      causante={"cliente"} 
      documentosTypes={facturasTypes} />
  );
};

export default L;
