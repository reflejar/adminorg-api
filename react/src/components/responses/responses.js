import React, { Fragment } from 'react';
import PropTypes from 'prop-types';
import { CheckCircle } from "react-feather";

const types = {
  "success": <CheckCircle size={96} className="success mr-4" />,
  "error": <CheckCircle size={96} className="danger mr-4" />,
}

const Response = ({ type, message }) => (
  <Fragment>
    {types[type]}
    <label className="fonticon-classname">{message}</label>
  </Fragment>
)

export default Response;

Response.propTypes = {
  type: PropTypes.string.isRequired,
  message: PropTypes.string.isRequired
}