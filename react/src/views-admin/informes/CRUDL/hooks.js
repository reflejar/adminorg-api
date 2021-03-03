import { useState } from 'react';
import moment from 'moment';


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

