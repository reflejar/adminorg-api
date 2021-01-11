import React, { useState, useEffect, useCallback } from 'react';
import moment from 'moment';
import { Row, Col } from "reactstrap";
import get from 'lodash/get';
// Components
import Spinner from '../../../../components/spinner/spinner';
import { usePreconceptos } from '../../../../utility/hooks/dispatchers';
import { PreconceptosTable } from "../_campos/tables/preconceptos";


const filterCompletedObject = (arr) =>
  arr.filter(d => d.checked)

const HandlePreconceptos = ({ setDocumento, preconceptos, clientes, dominios, ingresos, errors }) => {
  
    const getPreconceptos = useCallback(() => {
    const data = preconceptos.map((preconcepto) => ({
      id: preconcepto.id,
      destinatario: clientes.find((x) => x.id === preconcepto.destinatario) ? 
        get(clientes.find((x) => x.id === preconcepto.destinatario), "full_name", null) :
        get(dominios.find((x) => x.id === preconcepto.destinatario), "full_name", null) ,
      concepto: get(ingresos.find((x) => x.id === preconcepto.concepto), "full_name", null),
      periodo: moment(preconcepto.periodo).format('YYYY-MM'),
      fecha_vencimiento: preconcepto.fecha_vencimiento,
      fecha_gracia: preconcepto.fecha_gracia,
      detalle: preconcepto.detalle,
      monto: preconcepto.monto,
      checked: false
    }))
  return data
  }, [preconceptos, ingresos, clientes, dominios]);
  
  const [selectedPreconceptos, setSelectedPreconceptos] = useState(getPreconceptos());
  const [all, setAll] = useState(false);

  
  const handlePreconceptosTableRowSelect = (index) => {
    let updatedPreconceptos = [...selectedPreconceptos];
    updatedPreconceptos[index].checked = !updatedPreconceptos[index].checked;
    setSelectedPreconceptos(updatedPreconceptos);
  };
  
  const handlePreconceptosTableAllSelect = () => {
    
    let updatedPreconceptos = []
    all ? 
    updatedPreconceptos = [...selectedPreconceptos.map(x => ({...x, checked:false}))] :
    updatedPreconceptos = [...selectedPreconceptos.map(x => ({...x, checked:true}))]
    setAll(!all)
    setSelectedPreconceptos(updatedPreconceptos);
    
  };
  


  useEffect(() => {
    const updatedPreconceptos = filterCompletedObject(selectedPreconceptos);
    setDocumento((state) => ({
      ...state,
      preconceptos: [...updatedPreconceptos.map(x => x.id)]
    }));
  }, [selectedPreconceptos, setDocumento])  

  return (
    <Row>
      <Col sm="12">
        <h3 className="pl-0 credito__row__header__text">
          Seleccion de preconceptos
        </h3>
          {
            selectedPreconceptos.length > 0 ? 
              <PreconceptosTable
                errors={errors && errors.preconceptos}
                all={all}
                onAllSelect={handlePreconceptosTableAllSelect}
                dataTable={selectedPreconceptos.map((preconcepto) => ({
                  ...preconcepto,
                  onRowSelect: handlePreconceptosTableRowSelect,
              }))}/> :
              <p className="red">--- No existen preconceptos ---</p>
            }
      </Col>
    </Row>
  );
};


const Preconceptos = ({ setDocumento, clientes, dominios, ingresos, errors }) => {
  const [preconceptos, loadingPreconceptos] = usePreconceptos();

  return (
    <Row>
      <Col sm="12">
        {loadingPreconceptos ?
          <div className="loading-modal">
            <Spinner />
          </div>
          :
          <HandlePreconceptos
            setDocumento={setDocumento}
            preconceptos={preconceptos}
            clientes={clientes}
            dominios={dominios}
            ingresos={ingresos}
            errors={errors} />
          }
      </Col>
    </Row>
  );
};


export default Preconceptos;
