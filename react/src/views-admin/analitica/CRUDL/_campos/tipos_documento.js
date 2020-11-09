import React, { useEffect } from 'react';
import { Row, Col, FormGroup } from "reactstrap";
import { Select } from '../../../../components/Select';
import { useTitulos } from "../../../../utility/hooks/dispatchers";
import { receiptTypes } from '../_options/receipt_types';
import { mapToOptions } from '../../../../utility/mappers';
  

const TiposDocumentos = ({ filtro, setFiltro }) => {
  
  const [titulos, loadingTitulos] = useTitulos(true);


  // useEffect(() => {
  //   const updatedTiposDocumentos = filterCompletedObject(fechas);
  //   setFiltro((state) => ({
  //     ...state,
  //     fechas: updatedTiposDocumentos
  //   }));
  // }, [fechas, setFiltro])

  return (
    <Row>
      <Col sm="12">
        <FormGroup>
          <Select
              isMulti
              placeholder=""
              name="tipos_documento"
              id="tipos_documento"
              className="basic-multi-select"
              classNamePrefix="select"
              options={mapToOptions(receiptTypes)}    
              // onChange={(option) => setFieldValue('retiene', option)}
              // value={values.retiene}
          />
        </FormGroup>
      </Col>
    </Row>
  );
};


export default TiposDocumentos;