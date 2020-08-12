import React, { Component } from "react";
import Toggle from "react-toggle";

// import "prismjs/themes/prism-okaidia.css"; //Include CSS

import "react-toggle/style.css";
import "../../assets/scss/views/components/extra/switch.scss";


class Switch extends Component {

    constructor(props) {
        super(props);
        this.state = {
          checked: false
        }
      }
    

   render() {
      const { label, action } = this.props;
      return (
         <form ref="breakfastForm">

            <div className="example">
               <label>
                  <Toggle
                     defaultChecked={this.state.checked}
                     onChange={action}
                  />
                  <span className="label-text">{label}</span>
               </label>
            </div>
         </form>
      );
   }
}

export default Switch;
