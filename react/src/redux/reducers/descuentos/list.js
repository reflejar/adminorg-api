const list = (state = [], action) => {
    switch (action.type) {

        case 'GET_DESCUENTOS':
            return action.payload;

        default:
            return state;
    }
}
export default list