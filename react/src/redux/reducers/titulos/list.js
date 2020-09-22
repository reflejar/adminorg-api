export default (state = [], action) => {
    switch (action.type) {

        case 'GET_TITULOS':
            return action.payload;

        case 'GET_TITULO':
            return [...state, action.payload];

        default:
            return state;
    }
}
