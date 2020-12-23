const list = (state = [], action) => {
    switch (action.type) {
        case 'GET_SALDOS':
            return action.payload;

        default:
            return state;
    }
}
export default list