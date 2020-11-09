import React, { useCallback } from 'react';
import { connect, useDispatch } from 'react-redux';

// Components
import Spinner from '../../../../components/spinner/spinner';

import { analiticaActions } from '../../../../redux/actions/analitica';
import Fechas from '../_campos/fechas';
import Cuentas from '../_campos/cuentas';
import TiposDocumento from '../_campos/tipos_documento';
import Buttons from '../_campos/buttons';

// Styles
// import './index.scss';

import { useFiltro } from '../hooks';

const Reporte = ({ sendReporte, onClose }) => {
  
  const {filtro, setFiltro, loading, setLoading} = useFiltro();


  // const checkCondition = () => {
  //   if (filtro.creditos && filtro.creditos.length > 0) {
  //     return true;
  //   }
  //   return false;
  // } 
  

  const handleSubmit = useCallback((event) => {
    event.preventDefault();
    setLoading(true);
    
    sendReporte(filtro)
      .then(() => {
        onClose(false);
      })
      .catch((error) => {
        const { data } = error;
      })
      .finally(() => setLoading(false))
  }, [setLoading, sendReporte, filtro, onClose]);

  if (loading) {
    return (
      <div className='loading-modal'>
        <Spinner />
      </div>
    )
  }

  return (
    <form className='credito-invoice container' onSubmit={handleSubmit}>
      {console.log(filtro)}

      <Fechas 
        update={false}
        filtro={filtro} 
        setFiltro={setFiltro} />

      <Cuentas 
        filtro={filtro} 
        setFiltro={setFiltro} />

      <TiposDocumento
        filtro={filtro} 
        setFiltro={setFiltro}/>
      
      <Buttons 
        filtro={filtro}     
        onClose={onClose}
        // required={checkCondition()} 
        />

    </form>
  );
};


const mapDispatchToProps = dispatch => ({
  sendReporte: (payload) => dispatch(analiticaActions.send("cliente", payload))
});

export default connect(null, mapDispatchToProps)(Reporte);