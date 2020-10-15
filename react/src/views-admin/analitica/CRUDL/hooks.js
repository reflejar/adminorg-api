import { useEffect, useState } from 'react';
import { useDispatch } from 'react-redux';
import get from 'lodash/get';
import { archivosActions } from '../../../redux/actions/archivos';

export const useArchivo = (selected, onlyRead) => {
    const dispatch = useDispatch();
    const [loading, setLoading] = useState(false);
    const [errors, setErrors] = useState({}); 
    const [archivo, setArchivo] = useState({
        id: get(selected, 'id', null),
        nombre: onlyRead ? (selected && selected.nombre) : "",
        descripcion: onlyRead ? (selected && selected.descripcion) : "",
        ubicacion: onlyRead ? (selected && selected.ubicacion) : "",        
        carpeta: onlyRead ? (selected && selected.carpeta) : "",        
      });

    useEffect(() => {
    const fileId = get(selected, 'id');
    
    if (onlyRead && fileId && !archivo.nombre) {
        setLoading(true);

        dispatch(archivosActions.get("archivos", fileId))
        .then((doc) => setArchivo(doc))
        .finally(() => setLoading(false));
      }


    }, [selected, onlyRead, archivo.nombre, dispatch]);      

    return {archivo, setArchivo, errors, setErrors, loading, setLoading};

};

