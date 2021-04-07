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
  Header: 'N°',
  accessor: 'numero'
}, {        
  Header: 'Titulo',
  accessor: 'titulo'
}, {        
  Header: 'Cuenta',
  accessor: 'cuenta'
}, {
  Header: 'Concepto',
  accessor: 'concepto'
}, {      
  Header: 'Periodo',
  accessor: 'periodo'
}, {    
  Header: 'Tipo Doc',
  accessor: 'documento'
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
  accessor: 'capital',
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
  accessor: 'interes',
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
  accessor: 'total',
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
  Header: 'Cantidad',
  accessor: 'cantidad'
}];

const removeDuplicated = (arr, field=undefined) => {
  
  const result = arr.reduce((unique, o) => {
    if (field) {
      if(!unique.some(obj => obj[field] === o[field])) {
        unique.push(o);
      }
      return unique;
    } else {
      if(!unique.some(obj => obj === o)) {
        unique.push(o);
      }
      return unique;
    }
  },[]);
  return result
}


const Tabla = ({ data }) => {

  const [criterio, setCriterio] = useState({});
  const [agrupado, setAgrupado] = useState({});
  const [totales, setTotales] = useState({});
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
      selection = new Set(data.map(op => (op.titulo))) 
      setCriterio({titulo: removeDuplicated([...selection], "id").map(s => (s))});
    } else {
      const filteredOperation = data.filter(op => op.naturaleza === value);
      selection = new Set(filteredOperation.map(op => (op.cuenta)))
      setCriterio({cuenta: removeDuplicated([...selection], "id").map(s => (s))});
    }
    // setCriterio({criterio: removeDuplicated([...selection], "id").map(s => (s))});
    
  }; 

  const handleAgrupado = (event) => {

    const options = Array.from(event.target.selectedOptions, option => option.value);;
    let agrupados = [];
    options.forEach((val) => {
      let selection = [];
      if (val.includes(".")) {
        const acceso = val.split(".");
        const atr = acceso[0];
        selection = new Set(data.map(op => (op[acceso[1]])))
        let result = {};
        result[atr] = [...selection];
        agrupados.push(result);
      } else {
        const atr = val;
        selection = new Set(data.map(op => (op[val])))
        let result = {};
        result[atr] = [...selection];
        agrupados.push(result);
      }
    });
    setAgrupado(agrupados);
  };   

  const handleTotalizadores = (event) => {

    const options = Array.from(event.target.selectedOptions, option => option.value);
    let totalizadores = {};
    options.forEach((val) => {
      if (val.includes(".")) {
        const acceso = val.split(".");
        const atr = acceso[1];
        totalizadores[atr] = 0.00;
      } else {
        const atr = val;
        totalizadores[atr] = 0.00;
        if (val === "debe") {
          totalizadores.haber = 0.00;
        }
      }
    });
    setTotales(totalizadores);
    

  };     


  useEffect(() => {
    let objetos = [];
    if (Object.keys(criterio).length !== 0 && Object.keys(totales).length !== 0){ // Solo si tiene criterios y totales
    // Que Haga el listado inicial de objetos
      let colData = {...criterio}; // Establece la primer key (el criterio de calculo), con su value como lista de sus posibles valores
      // Y que si tiene agrupado
      if (agrupado.length > 0) {
        agrupado.forEach(grupo => {
          colData = Object.assign(colData, grupo) // Le agrega las otras keys (Los grupos), con sus values particulares que son tambien listas de posibles valores
        });
      }
      let qObjects = 1;
      Object.keys(colData).forEach(col => {qObjects = qObjects * colData[col].length}) // Calcula la cantidad de objetos que debe haber

      
      // for (var i = 1; i <= qObjects; i++) { // Itera la cantidad de objetos que debe hacer
      //   // let objeto = {...totales} // Inicia el objeto con los totales
      //   let objeto = {};
      //   Object.keys(colData).forEach(col => {
      //     // Esta logica hay que testear y modificar. Si esta bien, KELOCO (ANALIZAR!!!) Si no, modificarla
      //     objeto[col] = colData[col][i%colData[col].length]  // Le agrega cada una de las propiedades
      //     })
      //     objetos.push(objeto) 
      //   }
        // Termina el listado inicial de objetos
        // Seteado de columnas
        
    }


    // Iterar sobre la data y Que sume los totales
    const finalObjects = objetos.map(objeto => {
      let result = {...objeto}
      data.forEach(operacion => {
        console.log(operacion)
      });
      // data.filter()
      return result

    });

    // Hacer que trabaje con redux y que tenga su propio loading

    // Expresar en la tabla
    if (finalObjects.length > 0) {
      setColumnas(columns.filter(col => Object.keys(finalObjects[0]).some(key => (key === col.accessor))))
    }


  }, [criterio, totales, agrupado, data]);


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
                {/* <option value="documento.tipo">Documentos</option> */}
                <option value="concepto">Conceptos</option>
                <option value="periodo">Periodos</option>
            </Input>
          </FormGroup>
          <FormGroup>
            <Label for="totalizadores">Totalizar</Label>
            <Input type="select" id="totalizadores" name="selectTotalizadores" multiple onChange={(event) => handleTotalizadores(event)}>
                <option value="monto">Montos</option>
                <option value="debe">Debe y Haber</option>
                <option value="saldo.capital">Saldos de capital</option>
                <option value="saldo.interes">Saldos de interes</option>
                <option value="saldo.total">Saldos totales</option>
                <option value="cantidad">Cantidades</option>
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