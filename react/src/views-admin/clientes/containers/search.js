import React from 'react';
import { connect } from "react-redux";
import { clientesActions } from "../../../redux/actions/clientes";
import Search from "../../../components/board/search";
import ModalNew from '../modals/cliente';



const mapStateToProps = (state) => ({
    searchTerm: state.clientes.search,
    addNew: <ModalNew />
});

const mapDispatchToProps = (dispatch) => ({
    onChange: searchTerm => dispatch(clientesActions.search(searchTerm)),
});

export default connect(
    mapStateToProps,
    mapDispatchToProps
)(Search);
