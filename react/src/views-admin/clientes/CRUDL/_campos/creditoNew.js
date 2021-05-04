import React, { useEffect } from 'react';
import moment from 'moment';
import { Row, Col } from "reactstrap";

// Components
import Spinner from '../../../../components/spinner/spinner';

import { AppendableRowField } from '../../../../components/form/AppendableRowField';
import { mapToOptions } from '../../../../utility/mappers';

import { useDominios, useIngresos, useCajas } from '../../../../utility/hooks/dispatchers';
import { useAppendableField } from '../../../../components/form/hooks';

const filterDomainInclusion = (arr, clientId) =>
  arr.filter((x) => (x.propietario === clientId));

const filterCompletedObject = (arr) =>
  arr.filter((x) => (x.destinatario && x.concepto && x.periodo && x.monto > 0));


const CreditoNew = ({ documento, setDocumento, errors, destinatario, onlyRead }) => {

  const [dominios, loadingDominios] = useDominios();
  const [ingresos, loadingIngresos] = useIngresos();
  const [cajas, loadingCajas] = useCajas();

  const cleanItem = {
    monto: undefined,
    detalle: '',
    destinatario: '',
    concepto: '',
    cantidad: null,
    periodo: moment().format('YYYY-MM-DD'),
    fecha_gracia: moment().format('YYYY-MM-DD'),
    fecha_vencimiento: moment().format('YYYY-MM-DD')
  }

  const [
    creditos,
    handleCreditosChange,
    handleCreditosAppend,
    handleCreditosPop,
    setCreditos
  ] = useAppendableField(onlyRead ? documento.creditos : [cleanItem], {
    custom: {
      handleChange: (index) => (event) => {
        const name = event.target.name;
        const value = event.target.value;
        const credito = creditos[index];
        const updatedCredito = { ...credito, [name]: value };
        
        setCreditos(index, updatedCredito);
      }
    },
    cleanItem
  });

  useEffect(() => {
    const updatedCreditos = filterCompletedObject(creditos);
    setDocumento((state) => ({
      ...state,
      creditos: updatedCreditos
    }));
  }, [creditos, setDocumento])

  
  if (loadingDominios || loadingIngresos || loadingCajas) {
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
          appendButtonDisabled={onlyRead}
          popButtonDisabled={onlyRead}
          onAppendClick={handleCreditosAppend}
          onPopClick={handleCreditosPop}
          data={creditos}
          errors={errors && errors.creditos}
          fields={[
          onlyRead ? {
            type: 'text',
            name: 'destinatario',
            placeholder: 'Destinatario',
            header: 'Destinatario',
            disabled: onlyRead,
            handleChange: handleCreditosChange
          } : {
            type: 'select',
            name: 'destinatario',
            placeholder: 'Destinatario',
            header: 'Destinatario',
            handleChange: handleCreditosChange,
            disabled: onlyRead,
            options: (
              <>
                <option value=""> --- </option>
                <option value={destinatario.id}>{destinatario.perfil.apellido}, {destinatario.perfil.nombre}</option>
                {mapToOptions(filterDomainInclusion(dominios, destinatario.id)).map((dominio) => (
                  <option key={dominio.value} value={dominio.value}>
                    {dominio.label}
                  </option>
                ))}
              </>
            ),
          }, 
          onlyRead ? {
            type: 'text',
            name: 'concepto',
            placeholder: 'Concepto',
            header: 'Concepto',
            disabled: onlyRead,
            handleChange: handleCreditosChange
          } : {
            type: 'select',
            name: 'concepto',
            placeholder: 'Concepto',
            header: 'Concepto',
            disabled: onlyRead,
            handleChange: handleCreditosChange,
            options: (
              <>
                <option value=""> --- </option>
                {mapToOptions(ingresos).map((ingreso) => (
                  <option key={ingreso.value} value={ingreso.value}>
                    {ingreso.label}
                  </option>
                ))}
                {mapToOptions(cajas).map((caja) => (
                  <option key={caja.value} value={caja.value}>
                    {caja.label}
                  </option>
                ))}
              </>
            ),
          }, {
            type: 'date',
            name: 'periodo',
            placeholder: 'Periodo',
            header: 'Periodo',
            disabled: onlyRead,
            handleChange: handleCreditosChange
          }, {
            type: 'date',
            name: 'fecha_gracia',
            placeholder: 'Tope de descuento',
            header: 'Tope de descuento',
            disabled: onlyRead,
            handleChange: handleCreditosChange
          }, {
            type: 'date',
            name: 'fecha_vencimiento',
            placeholder: 'Vencimiento p/intereses',
            header: 'Vencimiento p/intereses',
            disabled: onlyRead,
            handleChange: handleCreditosChange
          },{
            type: 'text',
            name: 'detalle',
            placeholder: 'Detalle',
            header: 'Detalle',
            disabled: onlyRead,
            handleChange: handleCreditosChange
          }, {
            type: 'number',
            name: 'cantidad',
            placeholder: 'Cantidad',
            min: 0,
            header: 'Cantidad',
            disabled: onlyRead,
            handleChange: handleCreditosChange
          }, {
            type: 'number',
            name: 'monto',
            placeholder: 'Monto',
            min: 1,
            header: 'Monto',
            disabled: onlyRead,
            handleChange: handleCreditosChange
          }]}
          header={{
            title: "Items del comprobante",
            appendButton: '+ deuda'
          }}
        />
      </Col>
    </Row>
  );
};


export default CreditoNew;