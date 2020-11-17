import React, { useEffect, useState } from 'react';
import { Row, Col, Table, Input } from "reactstrap";
import { receiptTypes } from '../_options/receipt_types';
import './styles.scss'

const TiposDocumentos = ({ filtro, setFiltro, disableInOptions }) => {
  
  const [selection, setSelection] = useState([]);
  const [all, setAll] = useState(false)

  const SelectAll = () => {
    all ? 
    setSelection([]) :
    setSelection(receiptTypes.map(type => type.id))
    setAll(!all)
  }
  const SelectItem = (event) => {
    event.persist();
    const {value} = event.target;
    selection.some(selected => value === selected) ?
    setSelection(selection.filter(selected => selected !== value)) :
    setSelection([...selection, value])
    
  }  

  useEffect(() => {
    setFiltro((state) => ({
      ...state,
      receiptTypes: selection
    }));
  }, [selection, setFiltro])

  return (
    <Row>
      <Col sm="12">
        <hr />
        <div className="Campo">
          <h3 className="mt-2">
            Filtro por tipos de documento
          </h3>             
          <div className="">
            <Table 
              size="sm" 
              responsive
              >
              <thead>
                <tr>
                    <th>Tipo</th>
                    <td className="text-right">
                      <Input 
                        type="checkbox" 
                        onClick={() => SelectAll()} 
                        checked={all} />
                    </td>
                </tr>
              </thead>
              <tbody>
                {receiptTypes.map(type => (
                  <tr>
                    <td>{type.full_name}</td>
                    <td className="text-right">
                      <Input 
                        type="checkbox" 
                        onClick={SelectItem}
                        value={type.id}
                        checked={selection.some(selected => type.id === selected)} />                  
                    </td>
                  </tr>
                ))}
      
              </tbody>
          </Table>

          </div>

        </div>
      </Col>
    </Row>
  );
};


export default TiposDocumentos;