import React from 'react';

import { notasDebitoTypes } from '../_options/receipt_types';
import LStep from '../../../CRUDL/documento/L';

const L = () => {

  return (
    <LStep 
      causante={"cliente"} 
      documentosTypes={notasDebitoTypes}/>
  );
};

export default L;
