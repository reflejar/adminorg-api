const selected = (state = null, action) => {
    switch (action.type) {
      case 'SELECT_DESCUENTO':
        return action.id
      case 'POST_DESCUENTO':
        return action.payload.id
      default:
        return state
    }
  }

  export default selected