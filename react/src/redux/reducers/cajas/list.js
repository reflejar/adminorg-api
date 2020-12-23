const list = (state = [], action) => {
    switch (action.type) {

        case 'GET_CAJAS':
            return action.payload;

        default:
            return state;
    }
}
export default list