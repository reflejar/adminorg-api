export default (state = [], action) => {
    switch (action.type) {

        case 'GET_GASTOS':
            return action.payload;

        default:
            return state;
    }
}
