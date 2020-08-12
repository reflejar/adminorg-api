import React, { Component, Fragment } from "react";
import PropTypes from 'prop-types';
import { ButtonGroup } from "reactstrap";

class Options extends Component {
    state = {
        rSelected: [],
    };

    onRadioBtnClick = (rSelected) => {
        this.setState({ rSelected });
    };

  render() {
    const { leftOps, rightOps } = this.props;

    return (
        <section className="chat-app-form bg-blue-grey bg-lighten-5 d-flex justify-content-between">
          <ButtonGroup>
            {leftOps.map((button, i) => {
              return (
                <Fragment key={i}>
                  {button}
                </Fragment>
              );
            })}
          </ButtonGroup>

            <ButtonGroup>
              {rightOps.map((button, i) => {
                return (
                  <Fragment key={i}>
                    {button}
                  </Fragment>
                )
              })}
            </ButtonGroup>
        </section>
    );
  }
}

Options.propTypes = {
  leftOps: PropTypes.array,
  rightOps: PropTypes.array
};

export default Options;
