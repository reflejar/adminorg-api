const selected = (state = null, action) => {
    switch (action.type) {
      case 'SELECT_PROVEEDOR':
        return action.payload;
        
      case 'POST_PROVEEDOR':
        return action.payload.id
      default:
        return state
    }
  }

  export default selected