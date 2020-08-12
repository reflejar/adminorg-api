import { connect } from 'react-redux'
import List from '../../../components/board/list'
import { clientesActions } from "../../../redux/actions/clientes";

const filterCliente = (items, search) => {
    if(search !== '')
        return items.filter(t => t.full_name.toLocaleLowerCase().includes(search.toLocaleLowerCase()))
    else
        return items
}

const mapStateToProps = state => ({
    items: filterCliente(state.clientes.list, state.clientes.search),
    instance: state.clientes.instance
})

const mapDispatchToProps = dispatch => ({
    getItems: () => dispatch(clientesActions.get_all()),
    setSelectedObject: payload => dispatch(clientesActions.select(payload))
})

export default connect(
    mapStateToProps,
    mapDispatchToProps
)(List)