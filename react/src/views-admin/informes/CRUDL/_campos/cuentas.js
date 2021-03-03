import React, { useEffect, useState, Fragment } from 'react';
import { Row, Col, Table, Input } from "reactstrap";
import { useTitulos } from "../../../../utility/hooks/dispatchers";

import { Folder, ChevronRight, ChevronDown, FileText } from "react-feather";


const recursiveSelection = (arr) => {
  let group = [];
  arr.forEach(x => {
    group.push(x)
    x.hasOwnProperty("supertitulo") && recursiveSelection(x.cuentas).forEach(c => group.push(c))
  })
  return group;
}




const Item = ({ indentation, item, children, titulos, filterChildren, selection, setSelection, disabled }) => {
    const indentationItem = indentation + "px";

    const [openItem, setOpenItem] = useState(false);

    const OpenItem = () => {
        setOpenItem(!openItem);
    }
    
    const SelectItem = () => {
      selection.some(selected => item === selected) ?
      setSelection(selection.filter(x => x !== item)) :
      (item.hasOwnProperty("supertitulo") ? setSelection([...selection, ...recursiveSelection([item, ...filterChildren(titulos, item)])]): setSelection([...selection, item]))
    }

    return (
        <Fragment>
            <tr 
            style={{cursor: 'pointer'}}

            > 
                <td onClick={() => OpenItem()} style={{"padding-left": indentationItem}}>
                    {children && (openItem ? <ChevronDown size={18} /> : <ChevronRight size={18} />)}
                    {children ? <Folder size={18} /> : <FileText size={18} /> } {children ? item.full_name : item.nombre}
                </td>
                <td className="text-right">{item.numero}</td>
                <td className="text-right">
                  <Input 
                    type="checkbox" 
                    onClick={() => SelectItem()} 
                    checked={selection.some(selected => item === selected)} 
                    disabled={disabled} />
                </td>
            </tr>
            {openItem && children && children.map(itemChild => (
                    <Item 
                        indentation={indentation+10}
                        item={itemChild} 
                        children={filterChildren(titulos, itemChild)} 
                        titulos={titulos}
                        filterChildren={filterChildren}
                        selection={selection}
                        setSelection={setSelection}
                    />))}
            {openItem && item.cuentas && item.cuentas.sort((a, b) => a.nombre.localeCompare(b.nombre)).map(itemChild => (
                    <Item 
                        indentation={indentation+10}
                        item={itemChild} 
                        children={null}
                        titulos={titulos}
                        filterChildren={filterChildren}
                        selection={selection}
                        setSelection={setSelection}
                    />))}                    
        </Fragment>
    
      )
};


const filterParents = (arr) => arr.filter(x => !x.supertitulo);
const filterChildren = (arr, item) => arr.filter(x => x.supertitulo === item.id);

const filterCuentas = (arr) => {
  let cuentas = [];
  arr.forEach(x => {
    x.hasOwnProperty("supertitulo") ? 
    x.cuentas.forEach(c => cuentas.push(c.id)) : 
    cuentas.push(x.id)
  });
  return cuentas
}

const Cuentas = ({ filtro, setFiltro, disableInOptions }) => {
  
  const [titulos] = useTitulos(true);
  const [selection, setSelection] = useState([]);
  const [all, setAll] = useState(false)


  useEffect(() => {
    if (filtro.tipo === "rdos") {
      setSelection(recursiveSelection(titulos.filter(x => x.numero >= 400000)))
    }
    if (filtro.tipo === "sys") {
      setSelection(recursiveSelection(titulos))
    }    
  }, [filtro.tipo, titulos])


  const SelectAll = () => {
    all ? 
    setSelection([]) :
    setSelection(recursiveSelection(titulos))
    setAll(!all)
    
  }

  useEffect(() => {

    const updatedCuentas = filterCuentas(selection);
    const cuentas = Array.from(new Set(updatedCuentas));
    setFiltro((state) => ({
      ...state,
      cuentas: cuentas
    }));
  }, [selection, setFiltro])

  return (
    <Row>
      <Col sm="12">
        <hr />
        <h3 className="mt-2">
          Cuentas a analizar
        </h3>             
        <Table 
          size="sm" 
          responsive
          style={disableInOptions.some(x => x === filtro.tipo) ? {backgroundColor: '#f1f1f1'} : {}}
          >
          <thead>
            <tr>
                <th>Titulo/Cuenta</th>
                <th className="text-right">N°</th>
                <td className="text-right">
                  <Input 
                    type="checkbox" 
                    onClick={() => SelectAll()} 
                    checked={all} 
                    disabled={disableInOptions.some(x => x === filtro.tipo)}/>
                </td>
            </tr>
          </thead>
          <tbody>
          {titulos && filterParents(titulos).map(item => (
          <Item 
            indentation={0}
            item={item} 
            children={filterChildren(titulos, item)}
            titulos={titulos}
            filterChildren={filterChildren}
            selection={selection}
            setSelection={setSelection}
            disabled={disableInOptions.some(x => x === filtro.tipo)}
          />))}

          </tbody>
      </Table>
      </Col>
    </Row>
  );
};


export default Cuentas;