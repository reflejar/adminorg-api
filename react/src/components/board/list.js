import React, { Component } from "react";
import Item from "./item";
import PropTypes from 'prop-types';
import { Table } from 'reactstrap';

import Spinner from "../../components/spinner/spinner";

class List extends Component {

  constructor(props) {
    super(props);
    this.state = {
      loading: false
    }
  }

  async componentDidMount() {
    this.setState({ loading: true });
    await this.props.getItems();
    this.setState({ loading: false });
  }

  render () {
    const { items, instance, setSelectedObject } = this.props;
    const { loading } = this.state;

    if (loading) {
      return <Spinner />
    }

    return (
      <div className="list-group position-relative" id="users-list">
        <div className="users-list-padding">
          <Table size="sm">
            <tbody>
              {items && items.map((item,key) => (
                <Item
                  {...item}
                  key={key}
                  onClick={() => setSelectedObject(item)}
                  itemName={item.full_name}
                  active={instance && instance.id === item.id}
                  title={item.id ? false: true}
                />
              ))}
            </tbody>
          </Table>
        </div>
      </div>
    );
  }

}


List.propTypes = {
  items: PropTypes.array.isRequired,
  getItems: PropTypes.func.isRequired,
  instance: PropTypes.object,
  setSelectedObject: PropTypes.func.isRequired,
};

export default List;
