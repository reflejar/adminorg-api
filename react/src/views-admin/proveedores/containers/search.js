import React from 'react';
import { connect } from "react-redux";
import { proveedoresActions } from "../../../redux/actions/proveedores";
import Search from "../../../components/board/search";
import ModalNew from '../modals/proveedor';



const mapStateToProps = (state) => ({
    searchTerm: state.proveedores.search,
    addNew: <ModalNew />
});

const mapDispatchToProps = (dispatch) => ({
    onChange: searchTerm => dispatch(proveedoresActions.search(searchTerm)),
});

export default connect(
    mapStateToProps,
    mapDispatchToProps
)(Search);
