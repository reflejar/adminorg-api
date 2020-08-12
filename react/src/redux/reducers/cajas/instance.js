const selected = (state = null, action) => {
    switch (action.type) {
      case 'SELECT_CAJA':
        return action.id
      case 'POST_CAJA':
        return action.payload.id
      default:
        return state
    }
  }

  export default selected