import { connect } from "react-redux";
import { interesesActions } from "../../../../redux/actions/intereses";
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
  {
    accessor: 'reconocimiento',
    Header: 'Tipo de reconocimiento'
  },      
  {
    accessor: 'base_calculo',
    Header: 'Base de calculo'
  },      
]

const mapStateToProps = (state) => ({
    titles: titles,
    items: state.intereses.list
});

const mapDispatchToProps = dispatch => ({
  getItems: () => dispatch(interesesActions.get_all()),
})


export default connect(
    mapStateToProps,
    mapDispatchToProps
)(Table);
