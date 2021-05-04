import React, { useEffect } from 'react';
import { Row, Col } from "reactstrap";

// Components
import Spinner from '../../../../components/spinner/spinner';

import { AppendableRowField } from '../../../../components/form/AppendableRowField';
import { mapToOptions } from '../../../../utility/mappers';

import { useGastos } from '../../../../utility/hooks/dispatchers';
import { useAppendableField } from '../../../../components/form/hooks';

const filterCompletedObject = (arr) =>
  arr.filter((x) => (x.cuenta && x.monto > 0));


const ResultadoNew = ({ documento, setDocumento, errors, update }) => {
  const [gastos, loadingGastos] = useGastos();

  const cleanItem = {
    monto: '',
    detalle: '',
    cuenta: '',
  }

  const [
    resultados,
    handleResultadosChange,
    handleResultadosAppend,
    handleResultadosPop,
    setResultado
  ] = useAppendableField(update ? documento.resultados : [cleanItem], {
    custom: {
      handleChange: (index) => (event) => {
        const name = event.target.name;
        const value = event.target.value;
        const resultado = resultados[index];
        const updatedResultado = { ...resultado, [name]: value };

        setResultado(index, updatedResultado);


      }
    },
    cleanItem
  });

  useEffect(() => {
    const updatedResultados = filterCompletedObject(resultados);
    setDocumento((state) => ({
      ...state,
      resultados: updatedResultados
    }));
  }, [resultados, setDocumento])


  if (loadingGastos) {
    return (
      <div className='loading-modal'>
        <Spinner />
      </div>
    )
  }

  return (
    <Row>
      <Col sm="12">
        <AppendableRowField
          appendButtonDisabled={update}
          popButtonDisabled={update}
          onAppendClick={handleResultadosAppend}
          onPopClick={handleResultadosPop}
          data={resultados}
          errors={errors && errors.resultados}
          fields={[ {
            type: 'select',
            name: 'cuenta',
            placeholder: 'Cuenta',
            header: 'Cuenta',
            handleChange: handleResultadosChange,
            options: (
              <>
                <option defaultValue="">---</option>
                {mapToOptions(gastos).map((gasto) => (
                  <option key={gasto.value} value={gasto.value}>
                    {gasto.label}
                  </option>
                ))}
              </>
            ),
          },{
            type: 'text',
            name: 'detalle',
            placeholder: 'Detalle',
            header: 'Detalle',
            handleChange: handleResultadosChange
          }, {
            type: 'number',
            name: 'monto',
            placeholder: 'Monto',
            min: 0,
            header: 'Monto',
            handleChange: handleResultadosChange
          }]}
          header={{
            title: documento.id ? 'Resultados generados' : "Resultados a generar",
            appendButton: '+ deuda'
          }}
        />
      </Col>
    </Row>
  );
};


export default ResultadoNew;