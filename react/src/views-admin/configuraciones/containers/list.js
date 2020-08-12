import { connect } from 'react-redux'
import boardList from '../../../components/board/list'
import { configuracionesActions } from "../../../redux/actions/configuraciones";


const mapStateToProps = state => ({
    items: state.configuraciones.list,
    instance: state.configuraciones.instance
})

const mapDispatchToProps = dispatch => ({
    getItems: () => dispatch(configuracionesActions.get_all()),
    setSelectedObject: payload => dispatch(configuracionesActions.select(payload))
})

export default connect(
    mapStateToProps,
    mapDispatchToProps
)(boardList)