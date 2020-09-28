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
import CargaNew from '../_campos/cargaNew';
import FormasPago from '../_campos/formasPago';
import Buttons from '../_campos/buttons';
import { transferenciasTypes } from '../_options/receipt_types';

// Styles
import './index.scss';

import { deudasActions } from '../../../../redux/actions/deudas';
import { saldosActions } from '../../../../redux/actions/saldos';
import { cuentasActions } from '../../../../redux/actions/cuentas';
import { useDocumento } from '../hooks';

const Transferencia = ({ destinatario, update, selected, sendTransferencia, deleteTransferencia, onClose }) => {
  const dispatch = useDispatch();
  
  const {documento, setDocumento, errors, setErrors, loading, setLoading} = useDocumento(selected, destinatario, update);
  const errorButton = "La suma de las cargas deben igualar a la suma de las descargas";

  useEffect(() => {
    if (!documento.cargas) {   
      setDocumento((state) => ({
        ...state,
        receipt: {
          ...state.receipt,
          receipt_type: "Transferencia X",
        },        
        cargas: [],
        cajas: [],
        utilizaciones_disponibilidades: [],
      }))
    }

  }, [documento, setDocumento]);    


  const checkCondition = () => {
    let totalCargas = 0;
    let totalCajas = 0;
    let totalUtilizacionesDisponibilidades = 0;

    if (documento.cargas && documento.cargas.length > 0) {
      totalCargas = documento.cargas.reduce((total, carga) => Number(total) + Number(carga.monto), 0);
    }

    if (documento.cajas && documento.cajas.length > 0) {
      totalCajas = documento.cajas.reduce((total, caja) => Number(total) + Number(caja.monto), 0);
    }    

    if (documento.utilizaciones_disponibilidades && documento.utilizaciones_disponibilidades.length > 0) {
      totalUtilizacionesDisponibilidades = documento.utilizaciones_disponibilidades.reduce((total, utilizacion_disponibilidad) => Number(total) + Number(utilizacion_disponibilidad.monto), 0);
    }        

    const totalFormasPago = totalCajas + totalUtilizacionesDisponibilidades;
    if (totalCargas > 0) {
      return totalCargas === totalFormasPago;
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

    sendTransferencia(documento)
      .then(() => {
        toastr.success('¡Listo! Transferencia cargado con éxito');
        updateSituation();
        documento.contado ? onClose("cobrar") : onClose(false);
      })
      .catch((error) => {
        const { data } = error;
        setErrors(data);
      })
      .finally(() => setLoading(false))
  }, [setLoading, sendTransferencia, documento, updateSituation, onClose, setErrors]);


  const handleDelete = useCallback(() => {
    setLoading(true);
    deleteTransferencia(documento.id)
      .then(response => {
        toastr.success('¡Listo! Transferencia eliminado con éxito')
        updateSituation();
        onClose(false);
      })
      .catch((error) => toastr.error(error))
      .finally(() => setLoading(false))
  }, [setLoading, deleteTransferencia, documento, updateSituation, onClose]);

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
        types={transferenciasTypes}/>

      <FormasPago
        documento={documento}
        setDocumento={setDocumento}
        errors={errors}
        update={update} />
      
      <CargaNew 
        documento={documento} 
        setDocumento={setDocumento} 
        errors={errors} 
        update={update}/>

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
  destinatario: get(state, 'cajas.instance', {}),
})

const mapDispatchToProps = dispatch => ({
  sendTransferencia: (payload) => dispatch(documentosActions.send("tesoreria", payload)),
  deleteTransferencia: id => dispatch(documentosActions.remove("tesoreria", id)),
});

export default connect(mapStateToProps, mapDispatchToProps)(Transferencia);