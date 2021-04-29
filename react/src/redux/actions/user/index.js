import { LOGIN, LOGOUT } from '../../types';
import { authService } from '../../services/auth';
import { Service } from '../../services/general';


const setUserDetails = (data) => {
    return {
        type: LOGIN,
        user: data.user,
        profile: data.perfil,
        community: data.comunidad.nombre,
        admin_of: data.admin_of,
        afip: data.comunidad.afip
    }
};


const login = (username, password) => async (dispatch) => {

    let apiEndpoint = 'users/login/';
    let payload = {username, password};


    const response = await authService.post(apiEndpoint, payload)
    if (response && response.data.access_token) {
        
        const dataUser = {...response.data};
        delete dataUser.access_token
        const currentUser = setUserDetails(dataUser);
        
        localStorage.setItem('user', JSON.stringify(currentUser));
        localStorage.setItem('token', response.data.access_token);
        dispatch(currentUser);
        
        return currentUser;
    }
};

const logout = () => async (dispatch) => {
    dispatch({
        type: LOGOUT
    })
}

const register = (payload) => async (dispatch) => {

    let apiEndpoint = 'users/signup/';

    const response = await authService.post(apiEndpoint, payload)
    if (response.status >= 400) throw response;
    return response.data
    
};

const recovery = (payload) => async (dispatch) => {

    let apiEndpoint = 'users/passwordRecovery/';
    console.log(payload)

    const response = await authService.post(apiEndpoint, payload)
    if (response && response.data) {
        console.log("Hola");
    }
};

const changeCommunity = (payload) => async (dispatch) => {

    let apiEndpoint = 'users/changeCommunity/';

    const response = await Service.post(apiEndpoint, {payload})
    if (response.status >= 400) throw response;
    dispatch({
        type: "CHANGE_COMMUNITY",
        payload: payload
    });
    return response.data
    
};



export const userActions = {
    login,
    logout,
    register,
    recovery,
    changeCommunity,
}
