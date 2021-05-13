import React from "react";

var style = {
   backgroundColor: "#F8F8F8",
   textAlign: "center",
   padding: "20px",
   position: "fixed",
   left: "0",
   bottom: "0",
   height: "60px",
   width: "100%",
}
const Footer = props => (
   <footer>
      <div className="container-fluid">
         <div style={style}>
            <p className="text-center">
               © 2021{" "}
               <a
                  href="https://admin-smart.com"
                  rel="noopener noreferrer"
                  target="_blank"
               >
                  AdminSmart 2.0{" "}
               </a>
               {/* Crafted by <i className="ft-heart font-small-3" />
               <a href="https://pixinvent.com/" rel="noopener noreferrer" target="_blank">
                  {" "}
                  AdminSmart
               </a> */}
            </p>
         </div>

      </div>
   </footer>
);

export default Footer;
