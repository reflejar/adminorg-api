import { useState } from 'react';
import moment from 'moment';

import { useDispatch } from 'react-redux';
import get from 'lodash/get';
// import { archivosActions } from '../../../redux/actions/archivos';

export const useFiltro = () => {
    const [loading, setLoading] = useState(false);
    const [filtro, setFiltro] = useState({
        tipo: "pers",
        cuentas: [],
        fechas: [{
          start_date: "",
          end_date: moment().format('YYYY-MM-DD'),
        }],
        receiptTypes: []
        
      });

    return {filtro, setFiltro, loading, setLoading};

};

