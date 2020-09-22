const selected = (state = null, action) => {
    switch (action.type) {
      case 'SELECT_CONTABILIDAD':
        return action.payload;

      default:
        return state
    }
  }

  export default selected