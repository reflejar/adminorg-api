const list = (state = [], action) => {
    switch (action.type) {
        case 'GET_DOCUMENTOS':
            return action.payload;
  
        case 'GET_DOCUMENTO':
            return [...state, action.payload];
  
        default:
            return state;
    }
  }
  export default list