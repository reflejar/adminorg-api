import React, { useCallback } from 'react';
import { connect, useDispatch } from 'react-redux';
import { Row, Col } from "reactstrap";
import get from 'lodash/get';
import { toastr } from "react-redux-toastr";

// Components
import Spinner from '../../../../components/spinner/spinner';

import { archivosActions } from '../../../../redux/actions/archivos';

import Ubicacion from '../_campos/ubicacion';
import Carpeta from '../_campos/carpeta';
import Basico from '../_campos/basico';
import Buttons from '../_campos/buttons';

// Styles
import './index.scss';

import { useArchivo } from '../hooks';

const Archivo = ({ instancia, update, selected, sendArchivo, deleteArchivo, onClose }) => {
  const dispatch = useDispatch();
  
  const {archivo, setArchivo, errors, setErrors, loading, setLoading} = useArchivo(selected, update);
  const errorButton = "Debe agregar un nombre";


  const checkCondition = () => {
    return archivo.nombre !== ""
  } 


  const updateSituation = useCallback(() => {
    console.log("hola");
    // const esTitulo = instancia.hasOwnProperty("supertitulo");
    // let query = { destinatario: instancia.id }
    // if (esTitulo) {
    //   query = {...query, titulo:1};
    // }
    // dispatch(cuentasActions.get(query))    
  }, [dispatch, instancia] );

  
  const handleSubmit = useCallback((event) => {
    event.preventDefault();

    setLoading(true);

    sendArchivo(archivo)
      .then(() => {
        toastr.success('¡Listo! Archivo cargado con éxito');
        updateSituation();
        onClose(false);
      })
      .catch((error) => {
        const { data } = error;
        setErrors(data);
      })
      .finally(() => setLoading(false))
  }, [setLoading, sendArchivo, archivo, updateSituation, onClose, setErrors]);


  const handleDelete = useCallback(() => {
    setLoading(true);
    deleteArchivo(archivo.id)
      .then(response => {
        toastr.success('¡Listo! Archivo eliminado con éxito')
        updateSituation();
        onClose(false);
      })
      .catch((error) => toastr.error(error))
      .finally(() => setLoading(false))
  }, [setLoading, deleteArchivo, archivo, updateSituation, onClose]);

  if (loading) {
    return (
      <div className='loading-modal'>
        <Spinner />
      </div>
    )
  }

  return (
    <form className='credito-invoice container' onSubmit={handleSubmit}>

      <Ubicacion 
        archivo={archivo} 
        setArchivo={setArchivo}/>      

      <Carpeta 
        archivo={archivo} 
        setArchivo={setArchivo} />        

      <Basico 
        archivo={archivo} 
        setArchivo={setArchivo} 
        update={update}/>
 

      <Buttons 
        item={archivo}     
        update={update} 
        onClose={onClose}
        required={checkCondition()}
        error={!checkCondition() && errorButton}
        handleDelete={handleDelete} />

    </form>
  );
};

const mapStateToProps = state => ({
  instancia: get(state, 'analitica.instance', {}),
})


const mapDispatchToProps = dispatch => ({
  sendArchivo: (payload) => dispatch(archivosActions.send("asiento", payload)),
  deleteArchivo: id => dispatch(archivosActions.remove("asiento", id)),
});

export default connect(mapStateToProps, mapDispatchToProps)(Archivo);