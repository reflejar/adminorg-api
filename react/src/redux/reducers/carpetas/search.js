const search = (state = '', action) => {
  switch (action.type) {
    case 'SEARCH_CARPETA':
      return action.payload;

    default:
      return state
  }
};

export default search