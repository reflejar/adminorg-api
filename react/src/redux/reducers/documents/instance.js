const selected = (state = null, action) => {
  switch (action.type) {
    case 'GET_DOCUMENTO':
      return action.payload;
    default:
      return state
  }
}

export default selected