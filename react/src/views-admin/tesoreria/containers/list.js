import { connect } from 'react-redux'
import boardList from '../../../components/board/list'
import { cajasActions } from "../../../redux/actions/cajas";

const filterCaja = (items, search) => {
    if(search !== '')
        return items.filter(t => t.full_name.toLocaleLowerCase().includes(search.toLocaleLowerCase()))
    else
        return items
}

const mapStateToProps = state => ({
    items: filterCaja(state.cajas.list, state.cajas.search),
    instance: state.cajas.instance
})

const mapDispatchToProps = dispatch => ({
    getItems: () => dispatch(cajasActions.get_all()),
    setSelectedObject: payload => dispatch(cajasActions.select(payload))
})

export default connect(
    mapStateToProps,
    mapDispatchToProps
)(boardList)