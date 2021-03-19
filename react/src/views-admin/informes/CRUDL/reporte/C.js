import React, { useCallback } from 'react';
import { 
  connect, 
  // useDispatch 
} from 'react-redux';

// Components
import Spinner from '../../../../components/spinner/spinner';

import { informesActions } from '../../../../redux/actions/informes';
import Tipo from '../_campos/tipo';
import Fechas from '../_campos/fechas';
import Cuentas from '../_campos/cuentas';
import TiposDocumento from '../_campos/tipos_documento';
import Buttons from '../_campos/buttons';

// Styles
// import './index.scss';

import { useFiltro } from '../hooks';

const Reporte = ({ getDataReporte, onClose }) => {
  
  const {filtro, setFiltro, loading, setLoading} = useFiltro();

  const disableInOptions = ["sys", "rdos"];
  const checkCondition = () => {
    if (filtro.cuentas && filtro.cuentas.length > 0) {
      return filtro.receiptTypes && filtro.receiptTypes.length > 0;
    }
    return false;
  } 
  

  const handleSubmit = useCallback((event) => {
    event.preventDefault();
    setLoading(true);
    
    getDataReporte(filtro)
      .then(() => {
        onClose(false);
      })
      .catch((error) => {
        const { data } = error;
      })
      .finally(() => setLoading(false))
  }, [setLoading, getDataReporte, filtro, onClose]);

  if (loading) {
    return (
      <div className='loading-modal'>
        <Spinner />
      </div>
    )
  }

  return (
    <form className='credito-invoice container' onSubmit={handleSubmit}>
      {/* {console.log(filtro)} */}
      
      <Tipo 
        filtro={filtro} 
        setFiltro={setFiltro} />

      <Fechas 
        filtro={filtro} 
        setFiltro={setFiltro} />

      <Cuentas 
        filtro={filtro} 
        setFiltro={setFiltro} 
        disableInOptions={disableInOptions}/>

      <TiposDocumento
        filtro={filtro} 
        setFiltro={setFiltro}
        disableInOptions={disableInOptions}/>
      
      <Buttons 
        filtro={filtro}     
        onClose={onClose}
        required={checkCondition()} />

    </form>
  );
};


const mapDispatchToProps = dispatch => ({
  getDataReporte: (payload) => dispatch(informesActions.get_data(payload))
});

export default connect(null, mapDispatchToProps)(Reporte);