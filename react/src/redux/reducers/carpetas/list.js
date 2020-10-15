export default (state = [], action) => {
    switch (action.type) {

        case 'GET_CARPETAS':
            return action.payload;

        case 'GET_CARPETA':
            return [...state, action.payload];

        default:
            return state;
    }
}
