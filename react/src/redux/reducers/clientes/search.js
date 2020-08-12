const search = (state = '', action) => {
  switch (action.type) {
    case 'SEARCH_CLIENTE':
      return action.payload;

    default:
      return state
  }
};

export default search