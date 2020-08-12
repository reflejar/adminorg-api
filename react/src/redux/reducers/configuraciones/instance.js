const selected = (state = null, action) => {
    switch (action.type) {
      case 'SELECT_PARAMETRO':
        return action.id
      case 'POST_PARAMETRO':
        return action.payload.id
      default:
        return state
    }
  }

  export default selected