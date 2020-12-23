const initialState = {
  items: [],
  loading: false,
  error: null
};

const list = (state = initialState, action) => {
  switch (action.type) {
    case 'GET_PRECONCEPTOS_PENDING':
      return {
        ...state,
        loading: true,
      };

    case 'GET_PRECONCEPTOS_SUCCESSFULLY':
      return {
        ...state,
        items: action.payload
      };
    case 'GET_PRECONCEPTOS_ERROR':
      return {
        ...state,
        error: action.payload
      };
    case 'GET_PRECONCEPTOS_FINISHED':
      return {
        ...state,
        loading: false
      };
    case 'DELETE_PRECONCEPTO':
      return {
        ...state,
        items: state.items.filter((x) => x.id !== action.payload),
        loading: false
      };
    default:
      return state;
  }
};
export default list