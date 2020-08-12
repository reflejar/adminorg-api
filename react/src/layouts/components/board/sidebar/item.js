import React from "react";
import { Link } from "react-router-dom";

import PropTypes from 'prop-types';

const BoardItem = ({ objectName }) => (
  <tr>
    <td>
      <Link to="/clientes" className="text-reset text-decoration-none">
        {objectName}
      </Link>
    </td>
  </tr>
);

BoardItem.propTypes = {
  objectName: PropTypes.string.isRequired,
};

export default BoardItem;
