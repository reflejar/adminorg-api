import { Service } from '../../services/general';

const get = () => async (dispatch) => {
    const response = await Service.get('operative/parametros/titulo/')
    if (response) {
        dispatch({
            type: 'GET_TITULOS',
            payload: response.data
        })
    }
}

export const titulosActions = {
    get
}
