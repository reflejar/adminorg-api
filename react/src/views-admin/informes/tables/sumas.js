import React, { useState, useEffect } from 'react';
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

import { DataFrame } from "danfojs/src/index";


const columns = [{          
  Header: 'N°',
  accessor: 'titulo_numero'
}, {        
  Header: 'Titulo',
  accessor: 'titulo_nombre'
}, {        
  Header: 'Cuenta',
  accessor: 'cuenta'
}, {
  Header: 'Concepto',
  accessor: 'concepto',
  Cell: row => (
    <div
      style={{
        width: '100%',
      }}
    >
      {row.value !== "NaN" && row.value}
    </div>
  )     
}, {      
  Header: 'Periodo',
  accessor: 'periodo'
}, {    
  Header: 'Tipo Doc',
  accessor: 'documento_tipo'
}, {              
  Header: 'Monto',
  accessor: 'monto_sum',
  Cell: row => (
    <div
      style={{
        width: '100%',
        textAlign: "right"
      }}
    >
      {row.value && Numero(row.value)}
    </div>
  )     
}, {
  Header: 'Debe',
  accessor: 'debe_sum',
  Cell: row => (
    <div
      style={{
        width: '100%',
        textAlign: "right"
      }}
    >
      {row.value && Numero(row.value)}
    </div>
  )     
}, {  
  Header: 'Haber',
  accessor: 'haber_sum',
  Cell: row => (
    <div
      style={{
        width: '100%',
        textAlign: "right"
      }}
    >
      {row.value && Numero(row.value)}
    </div>
  )     
}, {
  Header: 'S. Capital',
  accessor: 'capital_sum',
  Cell: row => (
    <div
      style={{
        width: '100%',
        textAlign: "right"
      }}
    >
      {row.value && Numero(row.value)}
    </div>
  )     
}, {    
  Header: 'S. Interes',
  accessor: 'interes_sum',
  Cell: row => (
    <div
      style={{
        width: '100%',
        textAlign: "right"
      }}
    >
      
    </div>
  )     
}, {  
  Header: 'S. Total',
  accessor: 'total_sum',
  Cell: row => (
    <div
      style={{
        width: '100%',
        textAlign: "right"
      }}
    >
      
      {row.value && Numero(row.value)}
    </div>
  )     
}, {   
  Header: 'Cantidad',
  accessor: 'cantidad_sum'
}];


const Tabla = ({ data }) => {

  const [criterio, setCriterio] = useState([]);
  const [agrupado, setAgrupado] = useState([]);
  const [totales, setTotales] = useState([]);
  const [showColumns, setShowColumns] = useState([]);
  const [rows, setRows] = useState([]);

  useEffect(() => {


    // Formacion de las filas
    let df = new DataFrame(data)
    if (criterio.length > 0 && criterio.indexOf("titulo_nombre")) {
      try {
        df = df.query({"column": "naturaleza", "is": "==", "to": criterio[0]})  
      } catch (error) {
        console.log(error)
      }
    } 
    // Agrupado
    let grouped = [];
    if (criterio.indexOf("titulo_nombre") > -1) {
      grouped.push(...criterio)
    } else {
      grouped.push("cuenta")
    }
    if (agrupado.length > 0 ) {
      grouped.push(...agrupado)
    }
    let seeRows = df.groupby([...grouped]);

    // Sumas
    const result = seeRows.col(totales).sum()

    // Seteado de showColumns
    if (totales.length > 0) {
      setShowColumns([...grouped, ...totales.map(t => t + "_sum")]);
      
    }
    
    // Seteado de las filas
    result.to_json().then((json) => setRows(JSON.parse(json)));
    // Hacer que trabaje con redux y que tenga su propio loading

    // Expresar en la tabla

  }, [criterio, totales, agrupado, data]);

  const handleCriterio = (event) => {
    const value = event.target.value
    let option = [value];
    value === "titulo_nombre" && option.push("titulo_numero");
    setCriterio(option);
    
  }

  const handleAgrupado = (event) => {

    const options = Array.from(event.target.selectedOptions, option => option.value);
    setAgrupado(options);

  };   

  const handleTotalizadores = (event) => {
    let options = Array.from(event.target.selectedOptions, option => option.value);
    options.indexOf("debe") > -1 && options.push("haber");
    setTotales(options);
  };     

  
  
  


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
                <option value="titulo_nombre">Titulos contables</option>
            </Input>
          </FormGroup>          
          <FormGroup>
            <Label for="agrupado">Agrupado</Label>
            <Input type="select" id="agrupado" name="selectAgrupado" multiple onChange={(event) => handleAgrupado(event)}>
                <option value="concepto">Conceptos</option>
                <option value="periodo">Periodos</option>
                <option value="documento_tipo">Tipo Documento</option>
            </Input>
          </FormGroup>
          <FormGroup>
            <Label for="totalizadores">Totalizar</Label>
            <Input type="select" id="totalizadores" name="selectTotalizadores" multiple onChange={(event) => handleTotalizadores(event)}>
                <option value="monto">Montos</option>
                <option value="debe">Debe y Haber</option>
                <option value="capital">Saldos de capital</option>
                <option value="interes">Saldos de interes</option>
                <option value="total">Saldos totales</option>
                <option value="cantidad">Cantidades</option>
            </Input>
          </FormGroup>          
        </Form>

      </Col>          
        <Col md={8}>

          <SumasTable
            data={rows}
            columns={totales.length > 0 ? columns.filter(x => showColumns.indexOf(x.accessor) > -1) : []}
          />     

        </Col>
      </Row>
    </React.Fragment>
  );
};

export default Tabla;