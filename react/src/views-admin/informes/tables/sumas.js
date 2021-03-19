import React, { useState, useEffect} from 'react';
import SumasTable from "../../../components/board/tables/sumas";
import {Numero} from "../../../utility/formats";
import {
  Row,
  Col,
  Form,
  FormGroup,
  Label,
  Input
} from "reactstrap";

import 'react-table/react-table.css';


const columns = [{          
  Header: 'Cuenta',
  accessor: 'cuenta.nombre'
}, {
  Header: 'N° Titulo',
  accessor: 'titulo.numero'
}, {        
  Header: 'Titulo',
  accessor: 'titulo.nombre'
}, {
  Header: 'Concepto',
  accessor: 'concepto'
}, {      
  Header: 'Periodo',
  accessor: 'periodo'
}, {    
  Header: 'Tipo Doc',
  accessor: 'documento.tipo'
}, {            
  Header: 'Doc N°',
  accessor: 'documento.numero'
}, {   
  Header: 'Cantidad',
  accessor: 'cantidad'
}, {              
  Header: 'Monto',
  accessor: 'monto',
  Cell: row => (
    <div
      style={{
        width: '100%',
        textAlign: "right"
      }}
    >
      {Numero(row.value)}
    </div>
  )     
}, {
  Header: 'Debe',
  accessor: 'debe',
  Cell: row => (
    <div
      style={{
        width: '100%',
        textAlign: "right"
      }}
    >
      {Numero(row.value)}
    </div>
  )     
}, {  
  Header: 'Haber',
  accessor: 'haber',
  Cell: row => (
    <div
      style={{
        width: '100%',
        textAlign: "right"
      }}
    >
      {Numero(row.value)}
    </div>
  )     
}, {
  Header: 'S. Capital',
  accessor: 'saldo.capital',
  Cell: row => (
    <div
      style={{
        width: '100%',
        textAlign: "right"
      }}
    >
      {Numero(row.value)}
    </div>
  )     
}, {    
  Header: 'S. Interes',
  accessor: 'saldo.interes',
  Cell: row => (
    <div
      style={{
        width: '100%',
        textAlign: "right"
      }}
    >
      {Numero(row.value)}
    </div>
  )     
}, {  
  Header: 'S. Total',
  accessor: 'saldo.total',
  Cell: row => (
    <div
      style={{
        width: '100%',
        textAlign: "right"
      }}
    >
      {Numero(row.value)}
    </div>
  )     
}];


const Tabla = ({ data }) => {

  const [criterio, setCriterio] = useState([]);
  const [agrupado, setAgrupado] = useState([]);
  const [totales, setTotales] = useState([]);
  const [columnas, setColumnas] = useState([columns[0]])

  const handleCriterio = (event) => {

    const value = event.target.value;

    // let options = [value];
    // value === "cliente" && options.push("dominio")
    // console.log(options);
    // console.log(data);
    // const filteredOperation = data.filter(op => options.includes(op.naturaleza));
    // const selection = new Set(filteredOperation.map(op => (op.cuenta.nombre)));
    // Decidi que si filtra clientes, entonces que el criterio sea de clientes y luego haya un agrupado por lotes
    let selection = [];
    if (value === "titulo") {
      selection = new Set(data.map(op => (op.titulo.nombre)))
    } else {
      const filteredOperation = data.filter(op => op.naturaleza === value);
      selection = new Set(filteredOperation.map(op => (op.cuenta.nombre)))
    }
    setCriterio(selection);
    
  }; 

  const handleAgrupado = (event) => {

    const options = Array.from(event.target.selectedOptions, option => option.value);;
    let agrupados = [];
    options.forEach((val) => {
      let selection = [];
      if (val.includes(".")) {
        const acceso = val.split(".");
        selection = new Set(data.map(op => (op[acceso[0]][acceso[1]])))  
      } else {
        selection = new Set(data.map(op => (op[val])))
      }
      agrupados.push(selection);
    });
    setAgrupado(agrupados);
    

  };   


  useEffect(() => {
    // Esto tengo que hacer
    // Que calcule si ya tiene criterio y totales
    // Que si tiene agrupado
    // Que Haga el listado inicial de objetos
    // Iterar sobre la data
    // Que filtre los que corresponda
    // Que sume los totales


    // Hacer que trabaje con redux y que tenga su propio loading
    // Expresar en la tabla
  }, [criterio, agrupado, totales]);


  return (
    <React.Fragment>
      <Row>
      <Col md={4}>
        <Form>
          <FormGroup>
            <Label for="criterio">Analizar</Label>
            <Input type="select" id="criterio" name="selectCriterio" onChange={(event) => handleCriterio(event)}>
                <option value="">---</option>
                <option value="cliente">Clientes y Dominios</option>
                <option value="proveedor">Proveedores</option>
                <option value="caja">Tesoreria</option>
                <option value="ingreso">Ingresos</option>
                <option value="gasto">Gastos</option>
                <option value="titulo">Titulos contables</option>
            </Input>
          </FormGroup>          
          <FormGroup>
            <Label for="agrupado">Agrupado</Label>
            <Input type="select" id="agrupado" name="selectAgrupado" multiple onChange={(event) => handleAgrupado(event)}>
                <option value="documento.tipo">Documentos</option>
                <option value="concepto">Conceptos</option>
                <option value="periodo">Periodos</option>
            </Input>
          </FormGroup>
          <FormGroup>
            <Label for="totalizadores">Totalizar</Label>
            <Input type="select" id="totalizadores" name="selectTotalizadores"  multiple>
                <option value="monto">Montos</option>
                <option value="cantidad">Cantidades</option>
                <option value="debe">Debe y Haber</option>
                <option value="saldo.capital">Saldos de capital</option>
                <option value="saldo.interes">Saldos de interes</option>
                <option value="saldo.total">Saldos totales</option>
            </Input>
          </FormGroup>          
        </Form>

      </Col>          
      <Col md={8}>
        <SumasTable
          data={[]}
          columns={columnas}
        />   
      </Col>
      </Row>
    </React.Fragment>
  );
};

export default Tabla;


// const mapDispatchToProps = dispatch => ({
//   getDataReporte: (payload) => dispatch(informesActions.get_data(payload))
// });

// export default connect(null, mapDispatchToProps)(Tabla);