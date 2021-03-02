import React, {Fragment} from "react";
import moment from 'moment';

import { Row, Col, Table } from "reactstrap";


const Operaciones = ({data}) => {

  return (
    <Fragment>
      <Row>
        <Col sm="12">
          hola
        </Col>
      </Row>
      <Row>
        <Col sm="12">
          <Table responsive>
              <thead>
                <tr>
                  <th>Fecha</th>
                  <th>Cuenta</th>
                  <th>Periodo</th>
                  <th>Titulo</th>
                  <th>Tipo Doc</th>
                  <th>Doc N°</th>
                  <th>Cantidad</th>
                  <th>Valor</th>
                  <th>Debe</th>
                  <th>Haber</th>
                  <th>Adeudado</th>
                  <th>Detalle</th>
                  <th>Descripcion</th>
                </tr>
              </thead>          
              <tbody>
                {data.map(x => (
                  <tr>
                    <td>{moment(x.fecha).format("DD/MM/YYYY")}</td>
                    <td>{x.cuenta.nombre}</td>
                    <td>{moment(x.fecha_indicativa).format('YYYY-MM')}</td>
                    <td>{x.titulo.nombre}</td>
                    <td>{x.documento.tipo}</td>
                    <td>{x.documento.numero}</td>
                    <td>{x.cantidad}</td>
                    <td>{x.monto}</td>
                    <td>{x.debe}</td>
                    <td>{x.haber}</td>
                    <td>{x.saldo}</td>
                    <td>{x.detalle}</td>
                    <td>{x.descripcion}</td>
                  </tr>
                ))}
              </tbody>

          </Table>
        </Col>
      </Row>
    </Fragment>
  );
}

export default Operaciones