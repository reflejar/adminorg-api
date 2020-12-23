const list = (state = [], action) => {
    switch (action.type) {
        case 'GET_DEUDAS':
            return action.payload;

        default:
            return state;
    }
}
export default list