const search = (state = '', action) => {
  switch (action.type) {
    case 'SEARCH_TITULO':
      return action.payload;

    default:
      return state
  }
};

export default search