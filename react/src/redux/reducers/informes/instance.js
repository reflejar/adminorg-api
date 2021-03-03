const selected = (state = null, action) => {
    switch (action.type) {
      case 'SELECT_ANALITICA':
        return action.payload;

      case 'POST_ANALITICA':
        return action.payload.id;
      default:
        return state
    }
  }

  export default selected