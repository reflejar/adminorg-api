import { Service } from '../../services/general';

let apiEndpoint = 'operative/parametros/ingreso/';

const search = (term) => ({
    type: 'SEARCH_INGRESO',
    term
})

const select = (id) => ({
    type: 'SELECT_INGRESO',
    id
})

const get_all = () => async (dispatch) => {
    const response = await Service.get(apiEndpoint);
    if (response) {
        const ingresos = response.data.results.sort((a, b) => {
            let comparison = 0;
            if (a.nombre > b.nombre) {
                comparison = 1;
            } else if (a.nombre < b.nombre) {
                comparison = -1;
            }
            return comparison;
        });

        dispatch({
            type: 'GET_INGRESOS',
            payload: ingresos
        });
    }
}

// const send = (values) => async (dispatch) => {


//     let payload = {
//         titulo: values.titulo,
//         taxon: "socio",
//         perfil: {
//             nombre: values.nombre,
//             apellido: values.apellido,
//             razon_social: values.razon_social,
//             numero_documento: values.numero_documento,
//             fecha_nacimiento: values.fecha_nacimiento ? values.fecha_nacimiento : null,
//             es_extranjero: values.es_extranjero,
//             mail: values.mail,
//             telefono: values.telefono,
//             domicilio: {
//                 localidad: values.localidad,
//                 calle: values.calle,
//                 numero: values.numero,
//                 provincia: values.provincia
//             },

//         }
//     };

//     let response;

//     if (values.id) {
//         response = await Service.put(apiEndpoint + values.id + "/", payload);
//     } else {
//         response = await Service.post(apiEndpoint, payload);
//     }

//     if (response) {
//         await dispatch(get_all())
//         await dispatch({
//             type: 'POST_INGRESO',
//             payload: response.data
//         });
//         response.result = "success"
//     } else {
//         response = {
//             result: "error"
//         }
//     }


//     return response
// };



export const ingresosActions = {
    get_all,
    search,
    select,
    // send,
}
