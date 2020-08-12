export default (state = [], action) => {
    switch (action.type) {

        case 'GET_PUNTOS':
            return action.payload;

        default:
            return state;
    }
}
