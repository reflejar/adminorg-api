import { LOGIN, LOGOUT } from '../../types';
import { authService } from '../../services/auth';


const setUserDetails = (data) => {
    return {
        type: LOGIN,
        user: data.user,
        profile: data.perfil,
        community: data.comunidad.nombre,
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
    if (response && response.data) {
        
        const dataUser = {...response.data};
        delete dataUser.access_token
        const currentUser = setUserDetails(dataUser);
        
        localStorage.setItem('user', JSON.stringify(currentUser));
        localStorage.setItem('token', response.data.access_token);
        dispatch(currentUser);
        
        return currentUser;
    }
};


export const userActions = {
    login,
    logout,
    register
}
