import { useEffect, useState } from 'react';
import { useDispatch } from 'react-redux';
import moment from 'moment';
import get from 'lodash/get';
import { documentosActions } from '../../../redux/actions/documentos';

export const useDocumento = (selected, destinatario, onlyRead) => {
    const dispatch = useDispatch();
    const [loading, setLoading] = useState(false);
    const [errors, setErrors] = useState({}); 
    const [documento, setDocumento] = useState({
        id: get(selected, 'id', null),
        fecha_operacion: moment(onlyRead ? (selected && selected.fecha_operacion) : Date.now()).format('YYYY-MM-DD'),
        destinatario: get(destinatario, 'id', null),
        descripcion: '',
        receipt: {
          receipt_type: '',
          point_of_sales: '',
          concept: 'servicios',
          issued_date: moment(onlyRead ? (selected && selected.receipt.issued_date) : Date.now()).format('YYYY-MM-DD'),
        }
      });

    useEffect(() => {
    const documentId = get(selected, 'id');
    
    if (onlyRead && documentId && !documento.receipt.receipt_number) {
        setLoading(true);

        dispatch(documentosActions.get("cliente", documentId))
        .then((doc) => setDocumento(doc))
        .finally(() => setLoading(false));
      }


    }, [selected, onlyRead, documento.receipt.receipt_number, dispatch]);      

    return {documento, setDocumento, errors, setErrors, loading, setLoading};

};

