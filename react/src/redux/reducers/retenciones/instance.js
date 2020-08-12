const selected = (state = null, action) => {
    switch (action.type) {
      case 'SELECT_RETENCION':
        return action.id
      case 'POST_RETENCION':
        return action.payload.id
      default:
        return state
    }
  }

  export default selected