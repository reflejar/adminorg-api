import React, { Component } from "react";


class Contabilidad extends Component {
  constructor(props) {
    super(props);
    this.state = {
      activeTab: "1"
    };
  }

  toggle(tab) {
    if (this.state.activeTab !== tab) {
      this.setState({
        activeTab: tab
      });
    }
  }

  render() {
    return (
      <div className="chat-application">
      </div>
    );
  }

}

export default Contabilidad;