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
import Pagos from '../_campos/pagos';
import Resultados from '../_campos/resultadoNew';
import Buttons from '../_campos/buttons';
import { notasCreditoTypes } from '../_options/receipt_types';

// Styles
import './index.scss';

import { deudasActions } from '../../../../redux/actions/deudas';
import { saldosActions } from '../../../../redux/actions/saldos';
import { cuentasActions } from '../../../../redux/actions/cuentas';
import { useDocumento } from '../hooks';

const NotaCredito = ({ destinatario, update, selected, sendNotaCredito, deleteDocumento, onClose }) => {
  const dispatch = useDispatch();
  
  const {documento, setDocumento, errors, setErrors, loading, setLoading} = useDocumento(selected, destinatario, update);
  const errorButton = "La suma de las deudas a condonar deben ser estrictamente iguales al la suma del los resultados a generar";

  useEffect(() => {
    if (!documento.pagos) {   
      setDocumento((state) => ({
        ...state,
        pagos: [],
        resultados: []
      }))
    }

  }, [documento, setDocumento]);   


  const checkCondition = () => {
    let totalPagos = 0;
    let totalResultados = 0;
    if (documento.pagos && documento.pagos.length > 0) {
      totalPagos = documento.pagos.reduce((total, pago) => Number(total) + Number(pago.monto), 0);
    }
    if (documento.resultados && documento.resultados.length > 0) {
      totalResultados = documento.resultados.reduce((total, resultado) => Number(total) + Number(resultado.monto), 0);
    }
    if (totalPagos > 0) return totalPagos === totalResultados;
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
        documento.contado ? onClose("cobrar") : onClose(false);
      })
      .catch((error) => {
        const { data } = error;
        setErrors(data);
      })
      .finally(() => setLoading(false))
  }, [setLoading, sendNotaCredito, documento, updateSituation, onClose, setErrors]);


  const handleDelete = useCallback(() => {
    setLoading(true);
    deleteDocumento(documento.id)
      .then(response => {
        toastr.success('¡Listo! Nota de Credito eliminado con éxito')
        updateSituation();
        onClose(false);
      })
      .catch((error) => toastr.error(error))
      .finally(() => setLoading(false))
  }, [setLoading, deleteDocumento, documento, updateSituation, onClose]);


  
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
        update={update}
        types={notasCreditoTypes}/>

      <Pagos 
        documento={documento} 
        setDocumento={setDocumento} 
        destinatario={destinatario}
        errors={errors} 
        update={update}/>

      <Resultados
        documento={documento}
        setDocumento={setDocumento}
        errors={errors}
        update={update} />

      <Descripcion 
        documento={documento} 
        setDocumento={setDocumento}
        update={update}/>

      <Buttons 
        documento={documento}     
        update={update} 
        onClose={onClose}
        required={checkCondition()}
        error={!checkCondition() && errorButton}
        handleDelete={handleDelete} />

    </form>
  );
};

const mapStateToProps = state => ({
  destinatario: get(state, 'proveedores.instance', {}),
})

const mapDispatchToProps = dispatch => ({
  sendNotaCredito: (payload) => dispatch(documentosActions.send("proveedor", payload)),
  deleteDocumento: id => dispatch(documentosActions.remove("proveedor", id)),
});

export default connect(mapStateToProps, mapDispatchToProps)(NotaCredito);