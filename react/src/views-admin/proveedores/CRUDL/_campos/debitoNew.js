import React, { useEffect } from 'react';
import moment from 'moment';
import { Row, Col } from "reactstrap";

// Components
import Spinner from '../../../../components/spinner/spinner';

import { AppendableRowField } from '../../../../components/form/AppendableRowField';
import { mapToOptions } from '../../../../utility/mappers';

import { useGastos, useCajas} from '../../../../utility/hooks/dispatchers';
import { useAppendableField } from '../../../../components/form/hooks';


const filterCompletedObject = (arr) =>
  arr.filter((x) => (x.cuenta && x.monto > 0));


const DebitoNew = ({ documento, setDocumento, errors, update }) => {
  const [gastos, loadingGastos] = useGastos();
  const [cajas, loadingCajas] = useCajas();

  const cleanItem = {
    monto: undefined,
    detalle: '',
    cuenta: '',
    cantidad: null,
    fecha_vencimiento: moment().format('YYYY-MM-DD')
  }

  const [
    debitos,
    handleDebitosChange,
    handleDebitosAppend,
    handleDebitosPop,
    setDebitos
  ] = useAppendableField(update ? documento.debitos : [cleanItem], {
    custom: {
      handleChange: (index) => (event) => {
        const name = event.target.name;
        const value = event.target.value;
        const debito = debitos[index];
        const updatedDebito = { ...debito, [name]: value };

        setDebitos(index, updatedDebito);


      }
    },
    cleanItem
  });
  
  useEffect(() => {
    const updatedDebitos = filterCompletedObject(debitos);
    setDocumento((state) => ({
      ...state,
      debitos: updatedDebitos
    }));
  }, [debitos, setDocumento])


  if (loadingGastos || loadingCajas) {
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
          onAppendClick={handleDebitosAppend}
          onPopClick={handleDebitosPop}
          data={debitos}
          errors={errors && errors.debitos}
          fields={[
          {
            type: 'select',
            name: 'cuenta',
            placeholder: 'Cuenta',
            header: 'Cuenta',
            handleChange: handleDebitosChange,
            options: (
              <>
                <option value=""> --- </option>
                <option value="gastos" className="text-center"> - Cuentas de gastos - </option>
                {mapToOptions(gastos).map((gasto) => (
                  <option key={gasto.value} value={gasto.value}>
                    {gasto.label}
                  </option>
                ))}
                <option value="cajas" className="text-center"> - Cuentas del tesoro - </option>
                {mapToOptions(cajas).map((caja) => (
                  <option key={caja.value} value={caja.value}>
                    {caja.label}
                  </option>
                ))}                
              </>
            ),
          }, {
            type: 'date',
            name: 'fecha_vencimiento',
            placeholder: 'Fecha Vencimiento',
            header: 'Fecha Vencimiento',
            handleChange: handleDebitosChange
          }, {
            type: 'text',
            name: 'detalle',
            placeholder: 'Detalle',
            header: 'Detalle',
            handleChange: handleDebitosChange
          }, {
            type: 'number',
            name: 'cantidad',
            placeholder: 'Cantidad',
            header: 'Cantidad',
            min: 0,
            handleChange: handleDebitosChange
          }, {
            type: 'number',
            name: 'monto',
            placeholder: 'Monto',
            min: 1,
            header: 'Monto',
            handleChange: handleDebitosChange
          }]}
          header={{
            title: "Items del comprobante",
            appendButton: 'Agregar deuda'
          }}
        />
      </Col>
    </Row>
  );
};


export default DebitoNew;