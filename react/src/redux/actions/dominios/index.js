import { Service } from '../../services/general';
import get from 'lodash/get';

let apiEndpoint = 'operative/parametros/dominio/';

const search = (term) => ({
    type: 'SEARCH_DOMINIO',
    term
})

const select = (id) => ({
    type: 'SELECT_DOMINIO',
    id
})

const get_all = () => async (dispatch) => {
    const response = await Service.get(apiEndpoint);
    if (response) {    
        const dominios = response.data.results.map(c => {
            let full_name = get(c, 'numero', "");
            return ({...c, full_name})
        }).sort((a, b) => {
            let comparison = 0;
            if (a.numero > b.numero) {
                comparison = 1;
            } else if (a.numero < b.numero) {
                comparison = -1;
            }
            return comparison;
        });

        dispatch({
            type: 'GET_DOMINIOS',
            payload: dominios
        });
    }
}

const send = (values) => async (dispatch) => {


    let payload = {
        titulo: values.titulo,
        nombre: values.nombre,
        numero: values.numero,
        propietario:values.propietario,
        inquilino:values.inquilino,
        domicilio: {
            provincia: values.domicilio_provincia,
            localidad: values.domicilio_localidad,
            calle: values.domicilio_calle,
            numero: values.domicilio_numero,
            piso: values.piso,
            oficina: values.oficina,
            sector: values.sector,
            torre: values.torre,
            manzana: values.manzana,
            parcela: values.parcela,
            catastro: values.catastro,
            superficie_total: values.superficie_total,
            superficie_cubierta: values.superficie_cubierta,
        },
    };

    let response;

    if (values.id) {
        response = await Service.put(apiEndpoint + values.id + "/", payload);
    } else {
        response = await Service.post(apiEndpoint, payload);
    }

    if (response) {
        await dispatch(get_all())
        await dispatch({
            type: 'POST_DOMINIO',
            payload: response.data
        });
        response.result = "success"
    } else {
        response = {
            result: "error"
        }
    }


    return response
};



export const dominiosActions = {
    get_all,
    search,
    select,
    send,
}
