const initial = {
  tipo: undefined,
  cuentas: [],
  fechas: [],
  receiptTypes: []
  
}
const filter = (state = initial, action) => {
    switch (action.type) {
      case 'SET_INFORMES_ALL_FILTERS':
        return action.payload
      case 'SET_INFORMES_DATES':
        return {
          ...state,
          fechas: [...state.fechas, action.payload]
        }
        
      default:
        return state
    }
  }

  export default filter