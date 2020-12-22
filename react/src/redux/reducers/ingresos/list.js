export default (state = [], action) => {
    switch (action.type) {

        case 'GET_INGRESOS':
            return action.payload;

        default:
            return state;
    }
}
