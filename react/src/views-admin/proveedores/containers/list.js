import { connect } from 'react-redux'
import List from '../../../components/board/list'
import { proveedoresActions } from "../../../redux/actions/proveedores";

const filterProveedor = (items, search) => {
    if(search !== '')
        return items.filter(t => t.full_name.toLocaleLowerCase().includes(search.toLocaleLowerCase()))
    else
        return items
}

const mapStateToProps = state => ({
    items: filterProveedor(state.proveedores.list, state.proveedores.search),
    instance: state.proveedores.instance
})

const mapDispatchToProps = dispatch => ({
    getItems: () => dispatch(proveedoresActions.get_all()),
    setSelectedObject: payload => dispatch(proveedoresActions.select(payload))
})

export default connect(
    mapStateToProps,
    mapDispatchToProps
)(List)