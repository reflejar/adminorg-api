import React, { useEffect } from 'react';
import { Row, Col } from "reactstrap";

// Components

import { AppendableRowField } from '../../../../components/form/AppendableRowField';
import { mapToOptions } from '../../../../utility/mappers';

import { useAppendableField } from '../../../../components/form/hooks';

// const basicErrorMessage = "La suma de los montos a perdonar deben ser estrictamente iguales al la suma del los montos de cada portador.";

const filterCompletedObject = (arr) =>
  arr.filter((x) => (x.ingreso && x.unidad && x.monto > 0));


const DistribucionNew = ({ setDocumento, ingresos, errors }) => {

  
  const cleanItem = {
    ingreso: '',
    unidad: '',
    fecha_vencimiento: null,
    fecha_gracia: null,
    monto: '',
  }

  const [
    distribuciones,
    handleDistribucionesChange,
    handleDistribucionesAppend,
    handleDistribucionesPop,
    setDistribucion
  ] = useAppendableField([cleanItem], {
    custom: {
      handleChange: (index) => (event) => {
        const name = event.target.name;
        const value = event.target.value;
        const distribucion = distribuciones[index];
        const updatedDistribucion = { ...distribucion, [name]: value };

        setDistribucion(index, updatedDistribucion);        

      }
    },
    cleanItem
  });

  useEffect(() => {
    const updatedDistribuciones = filterCompletedObject(distribuciones);
    setDocumento((state) => ({
      ...state,
      distribuciones: updatedDistribuciones
    }));
  }, [distribuciones, setDocumento])


  return (
    <Row>
      <Col sm="12">
      <AppendableRowField
        appendButtonDisabled={false}
        popButtonDisabled={false}
        onAppendClick={handleDistribucionesAppend}
        onPopClick={handleDistribucionesPop}
        data={distribuciones}
        errors={errors && errors.distribuciones}
        fields={[{
          type: 'select',
          name: 'ingreso',
          placeholder: 'Ingreso',
          header: 'Ingreso',
          handleChange: handleDistribucionesChange,
          options: (
            <>
              <option defaultValue="">---</option>

              {mapToOptions(ingresos).map((ingreso) => (
                <option key={ingreso.value} value={ingreso.value}>
                  {ingreso.label}
                </option>
              ))}
            </>
          ),
        }, {
          type: 'select',
          name: 'unidad',
          placeholder: 'Distribucion',
          header: 'Distribucion',
          handleChange: handleDistribucionesChange,
          options: (
            <>
              <option value="">---</option>
              <option value="socio">Total por socio</option>
              <option value="dominio">Total por dominio</option>
              <option value="m2">Total por m2</option>
            </>
          ),
        }, {
          type: 'date',
          name: 'fecha_vencimiento',
          placeholder: 'Fecha Vencimiento',
          header: 'Fecha Vencimiento',
          handleChange: handleDistribucionesChange
        }, {
          type: 'date',
          name: 'fecha_gracia',
          placeholder: 'Fecha de Gracia',
          header: 'Fecha de Gracia',
          handleChange: handleDistribucionesChange
        }, {
          type: 'number',
          name: 'monto',
          placeholder: 'Monto',
          header: 'Monto',
          handleChange: handleDistribucionesChange
        }]}
        header={{
          title: 'Operaciones de distribucion',
          appendButton: 'Agregar deuda'
        }}
      />
      </Col>
    </Row>
  );
};


export default DistribucionNew;