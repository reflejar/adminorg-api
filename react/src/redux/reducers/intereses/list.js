export default (state = [], action) => {
    switch (action.type) {

        case 'GET_INTERESES':
            return action.payload;

        default:
            return state;
    }
}
