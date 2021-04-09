import React, { useCallback, useEffect } from 'react';
import { connect } from 'react-redux';
import { toastr } from "react-redux-toastr";

// Components
import Spinner from '../../../../components/spinner/spinner';

import { documentosActions } from '../../../../redux/actions/documentos';
import Encabezado from '../_campos/encabezados';
import Descripcion from '../_campos/descripcion';
import DistribucionNew from '../_campos/distribucionNew';
import Preconceptos from '../_campos/preconceptos';
import Buttons from '../_campos/buttons';
import { facturasTypes } from '../_options/receipt_types';
import { useDominios, useIngresos, useClientes } from '../../../../utility/hooks/dispatchers';

// Styles
import './index.scss';

import { useDocumento } from '../hooks';

const ComprobanteMasivo = ({ selected, sendComprobanteMasivo, onClose }) => {

  const destinatario = null;
  
  const {documento, setDocumento, errors, setErrors, loading, setLoading} = useDocumento(selected, destinatario);
  const [ingresos, loadingIngresos] = useIngresos();
  const [clientes, loadingClientes] = useClientes();
  const [dominios, loadingDominios] = useDominios();

  useEffect(() => {
    if (!documento.distribuciones) {   
      setDocumento((state) => ({
        ...state,
        distribuciones: [],
        preconceptos: []
      }))
    }

  }, [documento, setDocumento]);    
  

  const handleSubmit = useCallback((event) => {
    event.preventDefault();
    setLoading(true);
    
    sendComprobanteMasivo(documento)
      .then(() => {
        toastr.success('¡Listo! Comprobantes masivos solicitados con éxito');
        onClose(false);   
      })
      .catch((error) => {
        const { data } = error;
        setErrors(data);
      })
      .finally(() => setLoading(false))
  }, [setLoading, sendComprobanteMasivo, documento, onClose, setErrors]);

  if (loading || loadingClientes || loadingDominios || loadingIngresos) {
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
        types={facturasTypes}/>

      <DistribucionNew 
        setDocumento={setDocumento} 
        ingresos={ingresos}
        errors={errors} />

      <Preconceptos 
        setDocumento={setDocumento} 
        clientes={clientes}
        dominios={dominios}
        ingresos={ingresos}
        errors={errors} />        

      <Descripcion 
        documento={documento} 
        setDocumento={setDocumento}/>
      
      <Buttons 
        documento={documento}     
        onClose={onClose}
        required={true} />

    </form>
  );
};

const mapDispatchToProps = dispatch => ({
  sendComprobanteMasivo: (payload) => dispatch(documentosActions.send("cliente", payload))
});

export default connect(null, mapDispatchToProps)(ComprobanteMasivo);