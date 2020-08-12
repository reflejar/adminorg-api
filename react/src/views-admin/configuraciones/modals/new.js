import React, { useState } from 'react';
import { Button } from 'reactstrap';

import BasicModal from '../../../components/modal/basic';


const ModalNew = ({component}) => {

  const [modal, setModal] = useState(false)

  const handleToggle = () => {
    setModal(!modal)
  };

  return (
    <BasicModal
      header="Nuevo"
      open={modal}
      className={""}
      onToggle={handleToggle}
      component={component}
      footer={false}
      button={(
        <Button outline color="primary">Nuevo</Button>
      )}
    />
  );
}

export default ModalNew;