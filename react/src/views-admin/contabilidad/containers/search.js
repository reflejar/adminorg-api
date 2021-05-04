import React from 'react';
import { connect } from "react-redux";
import { titulosActions } from "../../../redux/actions/titulos";
import ModalNew from '../modals/titulo';
import { Form, Input } from "reactstrap";

const Search = ({onChange}) => (
    <div className="chat2-fixed-search p-2">
        <Form>
            <div className="position-relative has-icon-left">
                <Input
                    className="form-control"
                    id="searchUser"
                    name="searchUser"
                    type="text"
                    disabled

                    onChange={e => onChange(e.target.value)}
                    value= "+ nuevo titulo"
                />
                <div className="form-control-position">
                    <ModalNew />
                </div>
            </div>
        </Form>
    </div>
);


const mapDispatchToProps = (dispatch) => ({
    onChange: searchTerm => dispatch(titulosActions.search(searchTerm)),
});

export default connect(
    null,
    mapDispatchToProps
)(Search);
