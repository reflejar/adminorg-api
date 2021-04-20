// import external modules
import React, { Fragment, useState } from "react";
import { connect } from 'react-redux';

import {
   Row,
   Col,
   Card,
   CardTitle,
   CardHeader,
   CardBody,
   Button
} from "reactstrap";
import BasicModal from '../../components/modal/basic';

import { Briefcase, User } from "react-feather";


const UserProfile = ({user}) => {

   const [modal, setModal] = useState(false);

   const handleToggle = () => {
      setModal(!modal)
    };

      return (
         <Fragment>
            <BasicModal
               open={modal}
               onToggle={handleToggle}
               header={"Cambiar contraseña"}
               footer={false}
               component={""}
            />
            <Row>
               <Col lg="6" id="profile">
                  <Card>
                     <CardHeader>
                        <CardTitle className="mb-0">Perfil institucional</CardTitle>
                     </CardHeader>
                     <CardBody>
                        <Row>
                           <Col sm="12">
                           <Briefcase size={50} className="info mb-3" />
                            <h4 className="mb-3"><b>Nombre: </b> {user.profile.nombre}</h4>
                            <h4 className="mb-3"><b>Apellido: </b>{user.profile.apellido}</h4>
                            <h4 className="mb-3"><b>Razon social: </b>{user.profile.razon_social}</h4>
                            <h4 className="mb-3"><b>DNI: </b>{user.profile.numero_documento}</h4>
                            <h4 className="mb-3"><b>Comunidad: </b>{user.community}</h4>
                           </Col>
                        </Row>                        
                     </CardBody>
                  </Card>                  
               </Col>
               <Col lg="6" id="user">
                  <Card>
                     <CardHeader>
                        <CardTitle className="mb-0">Usuario</CardTitle>
                     </CardHeader>
                     <CardBody>
                        <Row>
                           <Col sm="12">
                           <User size={50} className="info mb-3" />
                            <h4 className="mb-3"><b>Usuario: </b>{user.user.username}</h4>
                            <h4 className="mb-3"><b>Tipo: </b>{user.user.group}</h4>
                            <h4 className="mb-3"><b>Email: </b>{user.user.email}</h4>
                            <p>Deseas cambiar la contraseña? <Button className="mb-1" color="link" onClick={handleToggle} size="sm">click aqui</Button></p>
                           </Col>
                        </Row>   
                     </CardBody>
                  </Card>                  
               </Col>               
            </Row>
         </Fragment>
      );
   }

const mapStateToProps = (state) => ({
  user: state.user.auth,
});

export default connect(mapStateToProps, null)(UserProfile);
