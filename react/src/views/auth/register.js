// import external modules
import React, { useState, useCallback } from "react";
import { NavLink } from "react-router-dom";
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
   CardFooter,
   FormFeedback
} from "reactstrap";

import { connect } from 'react-redux';

import { userActions } from '../../redux/actions/user';
import Spinner from '../../components/spinner/spinner';

const Register = ({history, register, logout}) => {
   
   logout();

   const [isChecked, setIsChecked] = useState(true);
   const [loading, setLoading] = useState(false);
   const [errors, setErrors] = useState({}); 
   const [response, setResponse] = useState(); 

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
   
   const handleChange = prop => event => {
      setData({...data, [prop]: event.target.value });
   }


   const registerUser = useCallback((event) => {
      event.preventDefault();
      
      setLoading(true);
      
      register(data)
        .then((response) => {
         setResponse(response.message)
        })
        .catch((errors) => {
         const { data } = errors;
          setErrors(data);
        })
        .finally(() => setLoading(false));
    }, [setLoading, register, data]);

   if (loading) {
      return <Spinner />
   }


   if (response) {
      return (
         <div className="container">
            <Row className="full-height-vh">
               <Col xs="12" className="d-flex align-items-center justify-content-center">
                  <Card className="gradient-blue-grey-blue text-center width-800">
                     <CardBody>
                        <h2 className="white">Registracion</h2>
                        <hr />
                        <Row>
                           <Col md="12">
                           <p class="white">
                              <i class="fa fa-check"></i> {response}
                           </p>
                           </Col>                   
                        </Row>
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
   }

   
   return (
      <div className="container">
         <Row className="full-height-vh">
            <Col xs="12" className="d-flex align-items-center justify-content-center">
               <Card className="gradient-blue-grey-blue text-center width-800">
                  <CardBody>
                     <h2 className="white">Registrate</h2>
                     <hr />
                     <Form onSubmit={(event) => registerUser(event) }>
                     <Row>
                        
                        <Col xs="6">
                           <p className="white">Datos del usuario</p>
                        
                           <FormGroup>
                              <Col md="12">
                                 <Input
                                    type="text"
                                    className="form-control"
                                    name="username"
                                    id="username"
                                    placeholder="Usuario"
                                    minLength="4"
                                    onChange={handleChange('username')}
                                    invalid={errors.username}
                                    required
                                 />
                                 <FormFeedback invalid>{errors.username}</FormFeedback>                                 
                              </Col>
                           </FormGroup>          
                           <FormGroup>
                              <Col md="12">
                                 <Input
                                    type="password"
                                    className="form-control"
                                    name="password"
                                    id="password"
                                    minLength="8"
                                    placeholder="Contraseña"
                                    onChange={handleChange('password')}
                                    invalid={errors.password}
                                    required
                                 />
                                 <FormFeedback invalid>{errors.password}</FormFeedback>                                            
                              </Col>
                           </FormGroup>
                           
                           <FormGroup>
                              <Col md="12">
                                 <Input
                                    type="password"
                                    className="form-control"
                                    name="password_confirmation"
                                    id="password_confirmation"
                                    minLength="8"
                                    placeholder="Confirme contraseña"
                                    onChange={handleChange('password_confirmation')}
                                    required
                                    invalid={errors.password_confirmation || (data.password_confirmation.length > 3 && data.password !== data.password_confirmation)}
                                 />
                                 <FormFeedback invalid>Las contraseñas no coinciden</FormFeedback>                                   
                              </Col>
                           </FormGroup>                                             
                           <FormGroup>
                              <Col md="12">
                                 <Input
                                    type="text"
                                    className="form-control"
                                    name="first_name"
                                    id="first_name"
                                    minLength="2"
                                    onChange={handleChange('first_name')}
                                    placeholder="Nombre"
                                    required
                                    invalid={errors.first_name}
                                 />
                                 <FormFeedback invalid>{errors.first_name}</FormFeedback>                                     
                              </Col>
                           </FormGroup>
                           <FormGroup>
                              <Col md="12">
                                 <Input
                                    type="text"
                                    className="form-control"
                                    name="last_name"
                                    id="last_name"
                                    minLength="2"
                                    onChange={handleChange('last_name')}
                                    placeholder="Apellido"
                                    required
                                    invalid={errors.last_name}
                                 />
                                 <FormFeedback invalid>{errors.last_name}</FormFeedback>          
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
                                    onChange={handleChange('email')}
                                    required
                                    invalid={errors.email}
                                 />
                                 <FormFeedback invalid>{errors.email}</FormFeedback>                              
                              </Col>
                           </FormGroup>                                    
                        </Col>
                        <Col xs="6">
                           <p className="white">Datos para el acceso a la comunidad</p>
                           <FormGroup>
                              <Col md="12">
                                 <Input
                                    type="text"
                                    className="form-control"
                                    name="comunidad"
                                    id="comunidad"
                                    placeholder="Comunidad"
                                    onChange={handleChange('comunidad')}
                                    required
                                    invalid={errors.comunidad}
                                 />
                                 <FormFeedback invalid>{errors.comunidad}</FormFeedback>
                              </Col>
                           </FormGroup>     
                           <FormGroup>
                              <Col md="12">
                                 <Input
                                    type="number"
                                    className="form-control"
                                    name="numero_documento"
                                    id="numero_documento"
                                    minLength="4"
                                    placeholder="Numero de Documento"
                                    onChange={handleChange('numero_documento')}
                                    invalid={errors.numero_documento}
                                    required
                                 />
                                 <FormFeedback invalid>{errors.numero_documento}</FormFeedback>
                              </Col>
                           </FormGroup>                                            
                        </Col>
                        
                                             
                     </Row>
                  
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
                              <Button type="submit" color="success" block className="btn-raised">
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


export default connect(null, mapDispatchToProps)(Register);