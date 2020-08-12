import React from 'react';

import { notasCreditoTypes } from '../_options/receipt_types';
import LStep from '../../../CRUDL/documento/L';

const L = () => {

  return (
    <LStep 
      causante={"cliente"} 
      documentosTypes={notasCreditoTypes}/>
  );
};

export default L;
