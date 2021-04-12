/*!

=========================================================
* Argon Dashboard PRO React - v1.2.0
=========================================================

* Product Page: https://www.creative-tim.com/product/argon-dashboard-pro-react
* Copyright 2021 Creative Tim (https://www.creative-tim.com)

* Coded by Creative Tim

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/
import React from "react";

import logo from "./logo.jpg";

// reactstrap components
import {
  Navbar,
  NavbarBrand
} from "reactstrap";

function AlternativeHeader() {
  return (
    <>
      <div className="header pb-6">
        <Navbar style = {styles.mainNavbar}>
          <NavbarBrand>
            <img src={logo} style={{width: 100, marginTop: -7}} />
          </NavbarBrand>
          <div style={styles.rectangle} >
            
          </div>
          <div style={styles.rectangle} >
            
          </div>
          <div style={styles.rectangle} >
            
          </div>
          <div style={styles.rectangle} >
            
          </div>
        </Navbar>
      </div>
    </>
  );
}

const styles = {
  mainNavbar: {
    backgroundColor: 'black',
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  rectangle: {
    width: '200px',
    height: '100px',
    backgroundColor: 'white'
  }
}

export default AlternativeHeader;
