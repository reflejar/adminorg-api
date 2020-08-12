import React from "react";

import PropTypes from 'prop-types';

const stylePointer = {
  cursor: 'pointer'
};

const Item = ({ onClick, itemName, active, title }) => (
  <tr 
    className={active ? "bg-primary white" : ""} 
    onClick={onClick}
  >
      {
        title
        ? <th className="text-center success">{itemName}</th>
        : <td style={stylePointer}>{itemName}</td>
      }
      
  </tr>
);

Item.propTypes = {
  onClick: PropTypes.func.isRequired,
  itemName: PropTypes.string.isRequired,
  active: PropTypes.bool,
}

export default Item;
