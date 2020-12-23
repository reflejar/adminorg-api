const list = (state = [], action) => {
    switch (action.type) {

        case 'GET_CLIENTES':
            return action.payload;

        case 'GET_CLIENTE':
            return [...state, action.payload];

        default:
            return state;
    }
}
export default list