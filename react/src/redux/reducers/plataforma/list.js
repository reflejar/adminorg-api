const list = (state = [], action) => {
    switch (action.type) {
        case 'GET_PLATAFORMA':
            return action.payload;

        default:
            return state;
    }
}
export default list