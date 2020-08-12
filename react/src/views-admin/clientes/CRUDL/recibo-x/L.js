import React from 'react';

import { recibosTypes } from '../_options/receipt_types';
import LStep from '../../../CRUDL/documento/L';

const L = () => {

  return (
    <LStep 
      causante={"cliente"} 
      documentosTypes={recibosTypes}/>
  );
};

export default L;
