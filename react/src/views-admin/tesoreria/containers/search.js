import React from 'react';
import { connect } from "react-redux";
import { cajasActions } from "../../../redux/actions/cajas";
import Search from "../../../components/board/search";
import ModalNew from '../modals/caja';



const mapStateToProps = (state) => ({
    searchTerm: state.cajas.search,
    addNew: <ModalNew />
});

const mapDispatchToProps = (dispatch) => ({
    onChange: searchTerm => dispatch(cajasActions.search(searchTerm)),
});

export default connect(
    mapStateToProps,
    mapDispatchToProps
)(Search);
