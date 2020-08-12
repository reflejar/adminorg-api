const selected = (state = null, action) => {
    switch (action.type) {
      case 'SELECT_DOMINIO':
        return action.id
      case 'POST_DOMINIO':
        return action.payload.id
      default:
        return state
    }
  }

  export default selected