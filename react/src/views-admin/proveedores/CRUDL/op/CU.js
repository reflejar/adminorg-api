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
import FormasPago from '../_campos/formasPago';
import Buttons from '../_campos/buttons';
import { opTypes } from '../_options/receipt_types';

// Styles
import './index.scss';

import { deudasActions } from '../../../../redux/actions/deudas';
import { saldosActions } from '../../../../redux/actions/saldos';
import { cuentasActions } from '../../../../redux/actions/cuentas';
import { useDocumento } from '../hooks';

const OP = ({ destinatario, update, selected, sendOP, deleteOP, onClose }) => {
  const dispatch = useDispatch();
  
  const {documento, setDocumento, errors, setErrors, loading, setLoading} = useDocumento(selected, destinatario, update);
  const errorButton = "La suma de las formas de pagos deben igualar o superar la suma de deudas a pagar";

  useEffect(() => {
    if (!documento.receipt.receipt_type) {   
      setDocumento((state) => ({
        ...state,
        receipt: {
          ...state.receipt,
          receipt_type: "Orden de Pago X",
        },
        pagos: [],
        cajas: [],
        utilizaciones_saldos: [],
        retenciones: []
      }))
    }

  }, [documento, setDocumento]);   

  const checkCondition = () => {
    let totalPagos = 0;
    let totalCajas = 0;
    let totalUtilizacionesSaldos = 0;
    let totalRetenciones = 0;
    if (documento.pagos && documento.pagos.length > 0) {
      totalPagos = documento.pagos.reduce((total, pago) => Number(total) + Number(pago.monto), 0);
    }

    if (documento.retenciones && documento.retenciones.length > 0) {
      totalRetenciones = documento.retenciones.reduce((total, resultado) => Number(total) + Number(resultado.monto), 0);
      if (totalRetenciones > totalPagos) {
        return false;
      }      
    }    
    if (documento.utilizaciones_saldos && documento.utilizaciones_saldos.length > 0) {
      totalUtilizacionesSaldos = documento.utilizaciones_saldos.reduce((total, resultado) => Number(total) + Number(resultado.monto), 0);
      if (totalUtilizacionesSaldos + totalRetenciones > totalPagos) {
        return false;
      }
    }    
    if (documento.cajas && documento.cajas.length > 0) {
      totalCajas = documento.cajas.reduce((total, resultado) => Number(total) + Number(resultado.monto), 0);
    }

    const totalFormasPago = totalCajas + totalUtilizacionesSaldos + totalRetenciones;
    if (totalFormasPago > 0) {
      return totalFormasPago >= totalPagos;
    }
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
    
    sendOP(documento)
      .then(() => {
        toastr.success('¡Listo! Orden de Pago cargada con éxito');
        updateSituation();
        onClose(false);
      })
      .catch((error) => {
        const { data } = error;
        setErrors(data);
      })
      .finally(() => setLoading(false));
  }, [setLoading, sendOP, documento, updateSituation, onClose, setErrors]);


  const handleDelete = useCallback(() => {
    setLoading(true);
    deleteOP(documento.id)
      .then(response => {
        toastr.success('¡Listo! Orden de Pago eliminada con éxito')
        updateSituation();
        onClose(false);
      })
      .catch((error) => toastr.error(error))
      .finally(() => setLoading(false))
  }, [setLoading, deleteOP, documento, updateSituation, onClose]);




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
        types={opTypes}/>

      <Pagos 
        documento={documento} 
        setDocumento={setDocumento} 
        destinatario={destinatario}
        errors={errors} 
        update={update}/>

      <FormasPago
        documento={documento}
        setDocumento={setDocumento}
        destinatario={destinatario}
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
  sendOP: (payload) => dispatch(documentosActions.send("proveedor", payload)),
  deleteOP: id => dispatch(documentosActions.remove("proveedor", id)),  
});

export default connect(mapStateToProps, mapDispatchToProps)(OP);