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
import FormasCobro from '../_campos/formasCobro';
import Buttons from '../_campos/buttons';
import { recibosTypes } from '../_options/receipt_types';

// Styles
import './index.scss';

import { deudasActions } from '../../../../redux/actions/deudas';
import { saldosActions } from '../../../../redux/actions/saldos';
import { cuentasActions } from '../../../../redux/actions/cuentas';
import { useDocumento } from '../hooks';

const ReciboX = ({ destinatario, onlyRead, selected, sendReciboX, deleteReciboX, onClose }) => {
  const dispatch = useDispatch();
  
  const {documento, setDocumento, errors, setErrors, loading, setLoading} = useDocumento(selected, destinatario, onlyRead);
  const errorButton = "La suma de las formas de cobros deben igualar o superar la suma de creditos a cobrar";

  useEffect(() => {
    if (!documento.receipt.receipt_type) {   
      setDocumento((state) => ({
        ...state,
        receipt: {
          ...state.receipt,
          receipt_type: "Recibo X",
        },
        condonacion: false,
        cobros: [],
        cajas: [],
        utilizaciones_saldos: [],
        utilizaciones_disponibilidades: [],
      }))
    }

  }, [documento, setDocumento]);   

  const checkCondition = () => {
    let totalCobros = 0;
    let totalCajas = 0;
    let totalUtilizacionesSaldos = 0;
    let totalUtilizacionesDisponibilidades = 0;
    if (documento.cobros && documento.cobros.length > 0) {
      totalCobros = documento.cobros.reduce((total, cobro) => Number(total) + Number(cobro.monto), 0);
    }
    if (documento.utilizaciones_saldos && documento.utilizaciones_saldos.length > 0) {
      totalUtilizacionesSaldos = documento.utilizaciones_saldos.reduce((total, resultado) => Number(total) + Number(resultado.monto), 0);
      if (totalUtilizacionesSaldos > totalCobros) {
        return false;
      }
    }        
    if (documento.cajas && documento.cajas.length > 0) {
      totalCajas = documento.cajas.reduce((total, resultado) => Number(total) + Number(resultado.monto), 0);
    }

    if (documento.utilizaciones_disponibilidades && documento.utilizaciones_disponibilidades.length > 0) {
      totalUtilizacionesSaldos = documento.utilizaciones_disponibilidades.reduce((total, resultado) => Number(total) + Number(resultado.monto), 0);
    }        

    const totalFormasPago = totalUtilizacionesSaldos + totalCajas + totalUtilizacionesDisponibilidades;
    if (totalFormasPago > 0) {
      return totalFormasPago >= totalCobros;
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
    
    sendReciboX(documento)
      .then(() => {
        toastr.success('¡Listo! Recibo X cargado con éxito');
        updateSituation();        
        onClose(false);
      })
      .catch((error) => {
        const { data } = error;
        setErrors(data);
      })
      .finally(() => setLoading(false));
  }, [setLoading, sendReciboX, documento, updateSituation, onClose, setErrors]);


  const handleDelete = useCallback(() => {
    setLoading(true);
    deleteReciboX(documento.id)
      .then(response => {
        toastr.success('¡Listo! Orden de Pago eliminada con éxito')
        updateSituation();
        onClose(false);
      })
      .catch((error) => toastr.error(error))
      .finally(() => setLoading(false))
  }, [setLoading, deleteReciboX, documento, updateSituation, onClose]);




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
        types={recibosTypes}/>

      <Cobros 
        documento={documento} 
        setDocumento={setDocumento} 
        destinatario={destinatario}
        errors={errors} 
        onlyRead={onlyRead}/>

      <FormasCobro
        documento={documento}
        setDocumento={setDocumento}
        destinatario={destinatario}
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
        error={!checkCondition() && errorButton} 
        handleDelete={handleDelete} />

    </form>
  );
};

const mapStateToProps = state => ({
  destinatario: get(state, 'clientes.instance', {}),
})

const mapDispatchToProps = dispatch => ({
  sendReciboX: (payload) => dispatch(documentosActions.send("cliente", payload)),
  deleteReciboX: id => dispatch(documentosActions.remove("cliente", id)),  
});

export default connect(mapStateToProps, mapDispatchToProps)(ReciboX);