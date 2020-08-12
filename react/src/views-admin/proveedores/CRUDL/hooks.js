import { useEffect, useState } from 'react';
import { useDispatch } from 'react-redux';
import moment from 'moment';
import get from 'lodash/get';
import { documentosActions } from '../../../redux/actions/documentos';
import { saldosActions } from '../../../redux/actions/saldos';

export const useDocumento = (selected, destinatario, update) => {
    const dispatch = useDispatch();
    const [loading, setLoading] = useState(false);
    const [errors, setErrors] = useState({}); 
    const [documento, setDocumento] = useState({
        id: get(selected, 'id', null),
        fecha_operacion: moment(update ? (selected && selected.fecha_operacion) : Date.now()).format('YYYY-MM-DD'),
        destinatario: get(destinatario, 'id', null),
        descripcion: '',
        receipt: {
          receipt_type: '',
          point_of_sales: '',
          receipt_number: '',
          issued_date: moment(update ? (selected && selected.receipt.issued_date) : Date.now()).format('YYYY-MM-DD'),
        }
      });

    useEffect(() => {
    const documentId = get(selected, 'id');

    if (update && documentId && !documento.receipt.receipt_number) {
        setLoading(true);

        dispatch(documentosActions.get("proveedor", documentId))
        .then((doc) => setDocumento(doc))
        .finally(() => setLoading(false));
      }


    }, [selected, update, documento.receipt.receipt_number, dispatch]);      

    return {documento, setDocumento, errors, setErrors, loading, setLoading};

};

export const useDisponibilidades = (date) => {
  const [loading, setLoading] = useState(false);

  const [disponibilidades, setDisponibilidades] = useState([]);
  
  const dispatch = useDispatch();

  useEffect(() => {
    async function fetchDispo() {
      setLoading(true);
  
      const data = await dispatch(saldosActions.get({ destinatario: "caja", fecha: moment(date).format('YYYY-MM-DD') }));
      setDisponibilidades(data);
      setLoading(false);
    }
    fetchDispo();
  }, [dispatch, date]);

  return [disponibilidades, loading];

};