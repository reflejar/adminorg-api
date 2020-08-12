const selected = (state = null, action) => {
    switch (action.type) {
      case 'SELECT_GASTO':
        return action.id
      case 'POST_GASTO':
        return action.payload.id
      default:
        return state
    }
  }

  export default selected