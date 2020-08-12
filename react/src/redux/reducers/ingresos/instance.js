const selected = (state = null, action) => {
    switch (action.type) {
      case 'SELECT_INGRESO':
        return action.id
      case 'POST_INGRESO':
        return action.payload.id
      default:
        return state
    }
  }

  export default selected