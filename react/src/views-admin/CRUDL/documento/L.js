import React, { useMemo, useState, useRef, useCallback } from 'react';
import { useDispatch } from 'react-redux';
import ReactToPrint from 'react-to-print';
import { CSVLink } from 'react-csv';
import { Table, Button, Form, Input, Row, Col, FormGroup, Label } from 'reactstrap';

import Spinner from '../../../components/spinner/spinner';
import { documentosActions } from '../../../redux/actions/documentos';
import { usePuntosDeVenta } from '../../../utility/hooks/dispatchers';

class DocumentosTable extends React.Component {
  render () {
    return (
      <Table responsive borderless>
        <thead>
          <tr>
            {this.props.headers.map(h => (
              <th>{h.label}</th>
            ))}
          </tr>
        </thead>

        <tbody>
          {this.props.data.map((documento) => {
            

            return (
              <tr key={documento.id}>
                <td>{documento.receipt.receipt_type}</td>
                <td>{documento.receipt.issued_date}</td>
                <td>{documento.receipt.point_of_sales}</td>
                <td>{documento.receipt.receipt_number}</td>
                <td>{documento.portador}</td>
                <td>{documento.receipt.total_amount}</td>
              </tr>
            );
          })}
        </tbody>
      </Table>
    )
  }
}



const initialFields = {
  receipt_type: '',
  point: '',
  numero: '',
  startDate: '',
  endDate: '',
};

const headers = [
  { label: 'Tipo', key: 'receipt.receipt_type' },
  { label: 'Fecha', key: 'receipt.issued_date' },
  { label: 'Punto de Venta', key: 'receipt.point_of_sales' },
  { label: 'Numero', key: 'receipt.receipt_number' },
  { label: 'Portador', key: 'destinatario' },
  { label: 'Total', key: 'receipt.total_amount' }
];

const LStep = ({ causante, documentosTypes }) => {
  const dispatch = useDispatch();
  const [table, setTable] = useState(false);
  const [fields, setFields] = useState(initialFields);
  const puntos = usePuntosDeVenta();
  const [loading, setLoading] = useState(false);
  const [documentos, setDocumentos] = useState([]);
  const ref = useRef(null);
  

  const dataForTable = useMemo(() => {
    if (table) {
      if (documentos && !documentos.length) {
        return [];
      }
      return documentos;
    }
  }, [table, documentos]);

  const handleSearch = useCallback(async (event) => {
    event.preventDefault();
    setLoading(true);

    const response = await dispatch(documentosActions.getList(causante, fields))
    .then((response) => {
      setDocumentos(response);
      setTable(true);
    })
    .finally(() => setLoading(false));;

    if (!response || !Array.isArray(response.results) || response.results.length === 0) {
      return;
    }

    ;
  }, [dispatch, causante, fields]);

  const handleChange = (key) => {
    return (event) => {
      const value = event.target.value;

      setFields(old => ({
        ...old,
        [key]: value
      }))
    };
  };

  if (loading) {
    return (
      <div className='loading-modal'>
        <Spinner />
      </div>
    )
  }

  if (!table) {
    return (
      <Form className="registration__filters" onSubmit={handleSearch}>
        <FormGroup>
          <Label>Tipo de documento</Label>
          <Input type="select" name="select" required={true} onChange={handleChange('receipt_type')}>
            <option value=''>---</option>
            {documentosTypes.map((type, i) => (
              <option key={i} value={type.id}>{type.nombre}</option>
            ))}
          </Input>
        </FormGroup>  

        <FormGroup>
          <Label>Punto de venta</Label>

          <Input type="select" name="select" onChange={handleChange('point')}>
            <option value=''>---</option>
            {puntos.map((punto, i) => (
              <option key={i} value={punto.number}>{punto.number}</option>
            ))}
          </Input>
        </FormGroup>

        <FormGroup>
          <Label>Numero de documento</Label>
          <Input
            value={fields.numero}
            placeholder="#12345"
            label="Numero de documento"
            onChange={handleChange('numero')} />
        </FormGroup>

        <Row>
          <Col md={6}>
            <FormGroup>
              <Label>Desde</Label>
              <Input
                type="date"
                name="start_date"
                placeholder="Fecha desde"
                onChange={handleChange('startDate')}
              />
            </FormGroup>
          </Col>

          <Col md={6}>
            <FormGroup>
              <Label>Hasta</Label>
              <Input
                type="date"
                name="end_date"
                placeholder="Fecha hasta"
                onChange={handleChange('endDate')}
              />
            </FormGroup>
          </Col>
        </Row>

        <Button type="submit" color="primary">
          Buscar
        </Button>
      </Form>
    );
  }

  return (
    <div className="registration__results">
      <div className="registration__actions">
        <ReactToPrint
          trigger={() => <Button outline>Imprimir</Button>}
          content={() => ref.current}
        />
        <CSVLink
          headers={headers}
          data={dataForTable}
          target="_blank"
          filename="admincu-documentos.csv">
          <Button outline>
            CSV
          </Button>
        </CSVLink>
      </div>

      <DocumentosTable headers={headers} data={dataForTable} ref={ref} />
    </div>
  );
};

export default LStep;
