import React from "react";
import { Table } from 'reactstrap';
import PropTypes from 'prop-types';

import BoardItem from "./item";


const BoardSidebar = ({ objects }) => (
    <div className="list-group position-relative" id="users-list">
        <div className="users-list-padding">
          <Table>
            <tbody>
              {objects.map(object => (
                  <BoardItem
                      key={object.id}
                      {...object}
                      objectName={object.name}
                  />
              ))}
            </tbody>
          </Table>
        </div>
    </div>
);

BoardSidebar.propTypes = {
    objects: PropTypes.array.isRequired,
}
export default BoardSidebar;
