export default (state = [], action) => {
    switch (action.type) {

        case 'GET_PROVEEDORES':
            return action.payload;

        default:
            return state;
    }
}
