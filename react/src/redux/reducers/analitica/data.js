const data = (state = [], action) => {
    switch (action.type) {
      case 'GET_AN_DATA':
        return [...state, ...action.payload]
      default:
        return state
    }
  }

export default data