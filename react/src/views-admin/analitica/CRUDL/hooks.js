import { useEffect, useState } from 'react';
import moment from 'moment';

import { useDispatch } from 'react-redux';
import get from 'lodash/get';
// import { archivosActions } from '../../../redux/actions/archivos';

export const useFiltro = () => {
    const dispatch = useDispatch();
    const [loading, setLoading] = useState(false);
    const [filtro, setFiltro] = useState({
        cuentas: [],
        fechas: [{
          start_date: "",
          end_date: moment().format('YYYY-MM-DD'),
        }]
        
      });

    // useEffect(() => {
    // const fileId = get(selected, 'id');
    
    // if (onlyRead && fileId && !archivo.nombre) {
    //     setLoading(true);

    //     dispatch(archivosActions.get("archivos", fileId))
    //     .then((doc) => setReporte(doc))
    //     .finally(() => setLoading(false));
    //   }


    // }, [selected, onlyRead, archivo.nombre, dispatch]);      

    return {filtro, setFiltro, loading, setLoading};

};

