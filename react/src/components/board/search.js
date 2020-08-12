import React from "react";
import { Form, Input } from "reactstrap";
import PropTypes from 'prop-types';

const Search = ({onChange, searchTerm, addNew}) => (
    <div className="chat-fixed-search p-2">
        <Form>
            <div className="position-relative has-icon-left">
                <Input
                    className="form-control"
                    id="searchUser"
                    name="searchUser"
                    type="text"
                    onChange={e => onChange(e.target.value)}
                    value= {searchTerm}
                />
                <div className="form-control-position">
                    { addNew }
                </div>
            </div>
        </Form>
    </div>
);

Search.propTypes = {
    onChange: PropTypes.func.isRequired,
    addNew: PropTypes.element,
    searchTerm: PropTypes.string.isRequired,
}

export default Search;