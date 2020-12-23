const list = (state = [], action) => {
    switch (action.type) {

        case 'GET_FACTURAS':
            return {
                ...state,
                [action.payload.type]: action.payload.data
            };

        default:
            return state;
    }
}
export default list