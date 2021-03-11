const data = (state = [], action) => {
    switch (action.type) {
      case 'GET_INFORMES_DATA':
        return action.payload
      default:
        return state
    }
  }

export default data