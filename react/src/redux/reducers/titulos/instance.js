const selected = (state = null, action) => {
    switch (action.type) {
      case 'SELECT_TITULO':
        return action.payload;

      case 'POST_TITULO':
        return action.payload.id;
      default:
        return state
    }
  }

  export default selected