const selected = (state = null, action) => {
    switch (action.type) {
      case 'SELECT_INFORMES':
        return action.payload;

      case 'POST_INFORMES':
        return action.payload.id;
      default:
        return state
    }
  }

  export default selected