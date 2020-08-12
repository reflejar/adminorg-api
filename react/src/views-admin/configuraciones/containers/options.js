import React from "react";
import { connect } from 'react-redux';

import Options from '../../../components/board/options';
import { Button } from 'reactstrap';

import ModalNew from '../modals/new';



const ConfiguracionesOptions = ({selected, edit}) => {

  return (
    <Options
      leftOps={[
        !selected && <Button disabled={true} outline color="primary">Nuevo</Button>,
        selected && <ModalNew component={edit[selected.id]} />,
      ]}
      rightOps={[]}        
    />
  );
}


const mapStateToProps = ({ configuraciones }) => ({
  selected: configuraciones.instance
});

export default connect(mapStateToProps)(ConfiguracionesOptions);

