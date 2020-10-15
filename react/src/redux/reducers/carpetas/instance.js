const selected = (state = null, action) => {
    switch (action.type) {
      case 'SELECT_CARPETA':
        return action.payload;

      case 'POST_CARPETA':
        return action.payload.id;
      default:
        return state
    }
  }

  export default selected