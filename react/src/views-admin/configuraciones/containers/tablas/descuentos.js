import { connect } from "react-redux";
import { descuentosActions } from "../../../../redux/actions/descuentos";
import Table from "./editSelectTable"

const titles = [
  {
    accessor: 'nombre',
    Header: 'Nombre'
  },
  {
    accessor: 'tipo',
    Header: 'Tipo'
  },
  {
    accessor: 'plazo',
    Header: 'Plazo estipulado'
  },  
  {
    accessor: 'monto',
    Header: 'Monto'
  }, 
]

const mapStateToProps = (state) => ({
    titles: titles,
    items: state.descuentos.list
});

const mapDispatchToProps = dispatch => ({
  getItems: () => dispatch(descuentosActions.get_all()),
})


export default connect(
    mapStateToProps,
    mapDispatchToProps
)(Table);
