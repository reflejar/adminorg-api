export default (state = [], action) => {
    switch (action.type) {
        case 'GET_TITULOS':
            return action.payload.results

        default:
            return state;
    }
}