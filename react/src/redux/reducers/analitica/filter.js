const initial = {
  tipo: undefined,
  cuentas: [],
  fechas: [],
  receiptTypes: []
  
}
const filter = (state = initial, action) => {
    switch (action.type) {
      case 'SET_AN_ALL_FILTERS':
        return action.payload
      case 'SET_AN_DATES':
        return {
          ...state,
          fechas: [...state.fechas, action.payload]
        }
        
      default:
        return state
    }
  }

  export default filter