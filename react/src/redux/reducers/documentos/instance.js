const selected = (state = null, action) => {
    switch (action.type) {
      case 'SELECT_DOCUMENTO':
        return action.payload;

      case 'POST_DOCUMENTO':
        return action.payload.id;
      default:
        return state
    }
  }

  export default selected