import React, { useEffect } from 'react';
import moment from 'moment';
import { Row, Col } from "reactstrap";

// Components
import { AppendableRowField } from '../../../../components/form/AppendableRowField';

import { useAppendableField } from '../../../../components/form/hooks';

// const basicErrorMessage = "La suma de los montos a perdonar deben ser estrictamente iguales al la suma del los montos de cada portador.";

const filterCompletedObject = (arr) =>
  arr.filter((x) => (x.end_date));


const Fechas = ({ update, filtro, setFiltro }) => {
  
  const cleanItem = {
    start_date: "",
    end_date: moment().format('YYYY-MM-DD'),
  }

  const [
    fechas,
    handleFechasChange,
    handleFechasAppend,
    handleFechasPop,
    setFecha
  ] = useAppendableField(update ? filtro.fechas : [cleanItem], {
    custom: {
      handleChange: (index) => (event) => {
        const name = event.target.name;
        const value = event.target.value;
        const fecha = fechas[index];
        const updatedFecha = { ...fecha, [name]: value };

        setFecha(index, updatedFecha);        

      }
    },
    cleanItem
  });

  useEffect(() => {
    const updatedFechas = filterCompletedObject(fechas);
    setFiltro((state) => ({
      ...state,
      fechas: updatedFechas
    }));
  }, [fechas, setFiltro])

  return (
    <Row>
      <Col sm="12">
        <hr />
        <h3 className="mt-2">
          Periodos
        </h3>        
        <AppendableRowField
          appendButtonDisabled={update}
          popButtonDisabled={update}
          onAppendClick={handleFechasAppend}
          onPopClick={handleFechasPop}
          data={fechas}
          fields={[{
            type: 'date',
            name: 'start_date',
            placeholder: 'Fecha Inicio',
            header: 'Fecha Inicio',
            handleChange: handleFechasChange
          }, {
            type: 'date',
            name: 'end_date',
            placeholder: 'Fecha Fin',
            header: 'Fecha Fin',
            handleChange: handleFechasChange
          }]}
          header={{
            appendButton: 'Agregar periodo'
          }}
        />
      </Col>
    </Row>
  );
};


export default Fechas;