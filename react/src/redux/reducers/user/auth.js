import { LOGIN, LOGOUT } from '../../types';

const INITIAL_STATE = JSON.parse(localStorage.getItem('user'));

const auth = (state = INITIAL_STATE, action) => {
    switch (action.type) {
        case LOGIN:
            return {
                user: action.user,
                profile: action.profile,
                community: action.community,
                admin_of: action.admin_of
            };

        case LOGOUT:
            return null

        case "CHANGE_COMMUNITY":
            return {...state, community: action.payload};

        default:
            return state;
    }
}
export default auth