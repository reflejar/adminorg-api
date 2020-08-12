import React, { useEffect } from 'react';
import { Row, Col } from "reactstrap";

// Components
import Spinner from '../../../../components/spinner/spinner';

import { AppendableRowField } from '../../../../components/form/AppendableRowField';
import { mapToOptions } from '../../../../utility/mappers';

import { useCajas} from '../../../../utility/hooks/dispatchers';
import { useAppendableField } from '../../../../components/form/hooks';


const filterCompletedObject = (arr) =>
  arr.filter((x) => (x.cuenta && x.monto > 0));


const CargaNew = ({ documento, setDocumento, errors, update }) => {
  const [cajas, loadingCajas] = useCajas();

  const cleanItem = {
    monto: undefined,
    detalle: '',
    cuenta: '',
  }

  const [
    cargas,
    handleCargasChange,
    handleCargasAppend,
    handleCargasPop,
    setCargas
  ] = useAppendableField(update ? documento.cargas : [cleanItem], {
    custom: {
      handleChange: (index) => (event) => {
        const name = event.target.name;
        const value = event.target.value;
        const carga = cargas[index];
        const updatedCarga = { ...carga, [name]: value };

        setCargas(index, updatedCarga);


      }
    },
    cleanItem
  });
  
  useEffect(() => {
    const updatedCargas = filterCompletedObject(cargas);
    setDocumento((state) => ({
      ...state,
      cargas: updatedCargas
    }));
  }, [cargas, setDocumento])


  return (
    <Row>
      <Col sm="12">
        {loadingCajas ?
            <div className="loading-modal">
              <Spinner />
            </div>
            :        
        <AppendableRowField
          onAppendClick={handleCargasAppend}
          onPopClick={handleCargasPop}
          data={cargas}
          errors={errors && errors.cargas}
          fields={[
          {
            type: 'select',
            name: 'cuenta',
            placeholder: 'Cuenta',
            header: 'Cuenta',
            handleChange: handleCargasChange,
            options: (
              <>
                <option value=""> --- </option>
                {mapToOptions(cajas).map((caja) => (
                  <option key={caja.value} value={caja.value}>
                    {caja.label}
                  </option>
                ))}                
              </>
            ),
          }, {
            type: 'text',
            name: 'detalle',
            placeholder: 'Detalle',
            header: 'Detalle',
            handleChange: handleCargasChange
          }, {
            type: 'number',
            name: 'monto',
            placeholder: 'Monto',
            min: 1,
            header: 'Monto',
            handleChange: handleCargasChange
          }]}
          header={{
            title: documento.id ? 'Cargas generadas' : "Cargas a generar",
            appendButton: 'Agregar carga'
          }}
        />
        }
      </Col>
    </Row>
  );
};


export default CargaNew;