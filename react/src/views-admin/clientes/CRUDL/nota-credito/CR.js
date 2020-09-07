import React, { useCallback, useEffect } from 'react';
import { connect, useDispatch } from 'react-redux';
import moment from 'moment';
import get from 'lodash/get';
import { toastr } from "react-redux-toastr";

// Components
import Spinner from '../../../../components/spinner/spinner';

import { documentosActions } from '../../../../redux/actions/documentos';
import Encabezado from '../_campos/encabezados';
import Descripcion from '../_campos/descripcion';
import Cobros from '../_campos/cobros';
import Resultados from '../_campos/resultadoNew';
import Buttons from '../_campos/buttons';
import { notasCreditoTypes } from '../_options/receipt_types';

// Styles
import './index.scss';

import { deudasActions } from '../../../../redux/actions/deudas';
import { saldosActions } from '../../../../redux/actions/saldos';
import { cuentasActions } from '../../../../redux/actions/cuentas';
import { useDocumento } from '../hooks';

const NotaCredito = ({ destinatario, onlyRead, selected, sendNotaCredito, onClose }) => {
  const dispatch = useDispatch();
  
  const {documento, setDocumento, errors, setErrors, loading, setLoading} = useDocumento(selected, destinatario, onlyRead);
  const errorButton = "La suma de los creditos a cobrar deben ser estrictamente iguales al la suma del los resultados a generar";

  useEffect(() => {
    if (!documento.cobros) {   
      setDocumento((state) => ({
        ...state,
        cobros: [],
        resultados: []
      }))
    }

  }, [documento, setDocumento]);   


  const checkCondition = () => {
    let totalCobros = 0;
    let totalResultados = 0;
    if (documento.cobros && documento.cobros.length > 0) {
      totalCobros = documento.cobros.reduce((total, cobro) => Number(total) + Number(cobro.monto), 0);
    }
    if (documento.resultados && documento.resultados.length > 0) {
      totalResultados = documento.resultados.reduce((total, resultado) => Number(total) + Number(resultado.monto), 0);
    }
    if (totalCobros > 0) return totalCobros === totalResultados;
    return false    

  } 


  const updateSituation = useCallback(() => {
    dispatch(deudasActions.get({ destinatario: destinatario.id, fecha: moment().format('YYYY-MM-DD'), capture: true }));
    dispatch(saldosActions.get({ destinatario: destinatario.id, fecha: moment().format('YYYY-MM-DD'), capture: true }));
    dispatch(cuentasActions.get({ destinatario: destinatario.id, fecha: moment().format('YYYY-MM-DD') }));
  }, [dispatch, destinatario] );



  const handleSubmit = useCallback((event) => {
    event.preventDefault();
    setLoading(true);
    sendNotaCredito(documento)
      .then(() => {
        toastr.success('¡Listo! Nota de Credito cargada con éxito');
        updateSituation();
        onClose(false);
      })
      .catch((error) => {
        const { data } = error;
        setErrors(data);
      })
      .finally(() => setLoading(false))
  }, [setLoading, sendNotaCredito, documento, updateSituation, onClose, setErrors]);


  if (loading) {
    return (
      <div className='loading-modal'>
        <Spinner />
      </div>
    )
  }

  return (
    <form className='credito-invoice container' onSubmit={handleSubmit}>
      <Encabezado 
        documento={documento} 
        setDocumento={setDocumento} 
        errors={errors} 
        onlyRead={onlyRead}
        types={notasCreditoTypes}/>

      <Cobros 
        documento={documento} 
        setDocumento={setDocumento} 
        destinatario={destinatario}
        errors={errors} 
        onlyRead={onlyRead}/>

      <Resultados
        documento={documento}
        setDocumento={setDocumento}
        errors={errors}
        onlyRead={onlyRead} />

      <Descripcion 
        documento={documento} 
        setDocumento={setDocumento}
        onlyRead={onlyRead}/>

      <Buttons 
        documento={documento}     
        onlyRead={onlyRead} 
        onClose={onClose}
        required={checkCondition()}
        error={!checkCondition() && errorButton} />

    </form>
  );
};

const mapStateToProps = state => ({
  destinatario: get(state, 'clientes.instance', {}),
})

const mapDispatchToProps = dispatch => ({
  sendNotaCredito: (payload) => dispatch(documentosActions.send("cliente", payload))
});

export default connect(mapStateToProps, mapDispatchToProps)(NotaCredito);