import { LOGIN, LOGOUT } from '../../types';

const INITIAL_STATE = JSON.parse(localStorage.getItem('user'));

const auth = (state = INITIAL_STATE, action) => {
    switch (action.type) {
        case LOGIN:
            return {
                user: action.user,
                profile: action.profile,
                community: action.community,
            };

        case LOGOUT:
            return null

        default:
            return state;
    }
}
export default auth