const report = (state = null, action) => {
    switch (action.type) {
      case 'MAKE_REPORT':
        return action.payload;
      default:
        return state
    }
  }

  export default report