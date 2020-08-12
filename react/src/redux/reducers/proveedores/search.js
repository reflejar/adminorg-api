const search = (state = '', action) => {
  switch (action.type) {
    case 'SEARCH_PROVEEDOR':
      return action.payload;

    default:
      return state
  }
};

export default search