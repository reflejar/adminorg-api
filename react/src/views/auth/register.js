// import external modules
import React, { useState, useCallback } from "react";
import { NavLink } from "react-router-dom";
import { toastr } from "react-redux-toastr";
import {
   Row,
   Col,
   Input,
   Form,
   FormGroup,
   Button,
   Label,
   Card,   
   CardBody,
   CardFooter
} from "reactstrap";

import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';

import { userActions } from '../../redux/actions/user';
import Spinner from '../../components/spinner/spinner';

const Register = ({history, register, logout}) => {
   
   logout();

   const [isChecked, setIsChecked] = useState(true);
   const [loading, setLoading] = useState(false);
   const [errors, setErrors] = useState({}); 

   const [data, setData] = useState({
      comunidad:"",
      numero_documento:"",
      username:"",
      password:"",
      password_confirmation:"",
      first_name:"",
      last_name:"",
      email:""
   })

   const registerUser = useCallback((event) => {
      event.preventDefault();
      
      setLoading(true);
      
      register(data)
        .then(() => {
          toastr.success('¡Listo! Recibo X cargado con éxito');
          history.push('/deudas');
        })
        .catch((error) => {
          const { data } = error;
          setErrors(data);
        })
        .finally(() => setLoading(false));
    }, [setLoading, register]);

   if (loading) {
      return <Spinner />
   }
   
   return (
      <div className="container">
         <Row className="full-height-vh">
            <Col xs="12" className="d-flex align-items-center justify-content-center">
               <Card className="gradient-blue-grey-blue text-center width-400">
                  <CardBody>
                     <h2 className="white">Registrate</h2>
                     <hr />
                     <Form>
                        <p className="white">Datos de la comunidad</p>
                        <FormGroup>
                           <Col md="12">
                              <Input
                                 type="text"
                                 className="form-control"
                                 name="comunidad"
                                 id="comunidad"
                                 placeholder="Comunidad"
                                 required
                              />
                              {errors.comunidad && (
                                 <div className="invalid-feedback">
                                    {errors.comunidad}
                                 </div>
                              )}                                                    
                           </Col>
                        </FormGroup>     
                        <FormGroup>
                           <Col md="12">
                              <Input
                                 type="number"
                                 className="form-control"
                                 name="numero_documento"
                                 id="numero_documento"
                                 placeholder="Numero de Documento"
                                 required
                              />
                              {errors.numero_documento && (
                                 <div className="invalid-feedback">
                                    {errors.numero_documento}
                                 </div>
                              )}                              
                           </Col>
                        </FormGroup>                                            
                        <hr/>
                        <p className="white">Datos del usuario</p>
                     
                        <FormGroup>
                           <Col md="12">
                              <Input
                                 type="text"
                                 className="form-control"
                                 name="username"
                                 id="username"
                                 placeholder="Usuario"
                                 required
                              />
                           </Col>
                        </FormGroup>          
                        <FormGroup>
                           <Col md="12">
                              <Input
                                 type="password"
                                 className="form-control"
                                 name="password"
                                 id="password"
                                 placeholder="Contraseña"
                                 required
                              />
                           </Col>
                        </FormGroup>
                        
                        <FormGroup>
                           <Col md="12">
                              <Input
                                 type="password"
                                 className="form-control"
                                 name="password_confirmation"
                                 id="password_confirmation"
                                 placeholder="Confirme contraseña"
                                 required
                              />
                           </Col>
                        </FormGroup>                                             
                        <FormGroup>
                           <Col md="12">
                              <Input
                                 type="text"
                                 className="form-control"
                                 name="first_name"
                                 id="first_name"
                                 placeholder="Nombre"
                                 required
                              />
                           </Col>
                        </FormGroup>
                        <FormGroup>
                           <Col md="12">
                              <Input
                                 type="text"
                                 className="form-control"
                                 name="last_name"
                                 id="last_name"
                                 placeholder="Apellido"
                                 required
                              />
                           </Col>
                        </FormGroup>
                        <FormGroup>
                           <Col md="12">
                              <Input
                                 type="email"
                                 className="form-control"
                                 name="email"
                                 id="email"
                                 placeholder="Email"
                                 required
                              />
                           </Col>
                        </FormGroup>                     

                    

                        <FormGroup>
                           <Row>
                              <Col md="12">
                                 <div className="custom-control custom-checkbox mb-2 mr-sm-2 mb-sm-0 ml-3">
                                    <Input
                                       type="checkbox"
                                       className="custom-control-input"
                                       checked={isChecked}
                                       onChange={() => setIsChecked(!isChecked)}
                                       id="rememberme"
                                    />
                                    <Label className="custom-control-label float-left white" for="rememberme">
                                       Acepto los términos y condiciones
                                    </Label>
                                 </div>
                              </Col>
                           </Row>
                        </FormGroup>
                        <FormGroup>
                           <Col md="12">
                              <Button type="submit" color="success" block className="btn-raised" onClick={(event) => registerUser(event) }>
                                 Registrarme
                              </Button>
                           </Col>
                        </FormGroup>
                     </Form>
                  </CardBody>
                  <CardFooter>
                     <div className="float-left">
                        <NavLink to="/forgot-password" className="text-white">
                           Olvidaste la contraseña?
                        </NavLink>
                     </div>
                     <div className="float-right">
                        <NavLink to="/login" className="text-white">
                           Login
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
   register: (payload) => dispatch(userActions.register(payload)),
   logout: () => dispatch(userActions.logout()),
})


export default withRouter(connect(null, mapDispatchToProps)(Register));