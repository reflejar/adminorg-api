// import external modules
import React, {useState, useCallback} from "react";

import { NavLink } from "react-router-dom";
import { Row, Col, Input, Form, FormGroup, Button, Card, CardBody, CardFooter } from "reactstrap";

import { connect } from 'react-redux';

import { userActions } from '../../redux/actions/user';
import Spinner from '../../components/spinner/spinner';

const ForgotPassword = ({logout, recovery}) => {
   logout();

   const [loading, setLoading] = useState(false);
   const [success, setSuccess] = useState(false);
   const [data, setData] = useState();

   const recoveryPass = useCallback((event) => {
      event.preventDefault();
      
      setLoading(true);

      recovery({email:data})
        .then(() => {
            setSuccess(true)
        })
        .finally(() => setLoading(false));
    }, [setLoading, recovery, data]);

   if (loading) {
      return <Spinner />
   }
   
   return (
      <div className="container">
         <Row className="full-height-vh">
            <Col xs="12" className="d-flex align-items-center justify-content-center">
               <Card className="gradient-blue-grey-blue text-center width-400">                  
                  <CardBody>
                     <div className="text-center">
                        <h5 className="text-uppercase text-bold-400 white py-4">Olvidaste tu contraseña?</h5>
                     </div>
                     {success ?
                     <FormGroup>
                        <p class="white">
                           <i class="fa fa-check"></i> Hemos enviado por correo electrónico las instrucciones para configurar su nueva password. <br />
                           Si existe en nuestra base de datos una cuenta con el correo electrónico que ingresó debería recibirlo en breve.
                        </p>

                        <p class="white">
                           <i class="fa fa-warning"></i>
                           Si no recibe un correo electrónico, 
                           asegúrese de haber ingresado la dirección con la que se encuentra registrado en nustra base de datos, consulte con el administrador del consorcio. <br />                            (No se olvide de revisar su carpeta de spam).
                        </p>                        

                     </FormGroup> 
                     : <Form className="pt-2">
                        <FormGroup>
                           <Col md="12">
                              <Input
                                 type="email"
                                 className="form-control"
                                 name="email"
                                 id="email"
                                 placeholder="Tu direccion de email"
                                 onChange={(e) => setData(e.target.value)}
                                 required
                              />
                           </Col>
                        </FormGroup>
                        <FormGroup className="pt-2">
                           <Col md="12">
                              <div className="text-center mt-3">
                                 <Button color="warning" block onClick={(event) => recoveryPass(event)}>
                                    Recuperar contraseña
                                 </Button>
                              </div>
                           </Col>
                        </FormGroup>
                     </Form>
                     }
                  </CardBody>
                  <CardFooter>
                     <div className="float-left white">
                        <NavLink exact className="text-white" to="/login">
                           Login
                        </NavLink>
                     </div>
                     <div className="float-right white">
                        <NavLink exact className="text-white" to="/register">
                           Registrate ahora
                        </NavLink>
                     </div>
                  </CardFooter>
               </Card>
            </Col>
         </Row>
      </div>
   );
};

const mapDispatchToProps = dispatch => ({
   logout: () => dispatch(userActions.logout()),
   recovery: (email) => dispatch(userActions.recovery(email)),
})


export default connect(null, mapDispatchToProps)(ForgotPassword);