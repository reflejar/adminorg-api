export default (state = [], action) => {
    switch (action.type) {
        case 'GET_STATUS_CUENTAS':
            return action.payload;

        default:
            return state;
    }
}
