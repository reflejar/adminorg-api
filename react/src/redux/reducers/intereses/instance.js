const selected = (state = null, action) => {
    switch (action.type) {
      case 'SELECT_INTERES':
        return action.id
      case 'POST_INTERES':
        return action.payload.id
      default:
        return state
    }
  }

  export default selected