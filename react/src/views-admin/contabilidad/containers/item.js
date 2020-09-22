import React, {Fragment, useState} from "react";
import { connect } from "react-redux";
import { Folder, ChevronRight, ChevronDown, FileText } from "react-feather";
import { titulosActions } from "../../../redux/actions/titulos";


const Item = ({ indentation, item, children, titulos, filterChildren, selected, setSelected }) => {
    const indentationItem = indentation + "px";

    const [openItem, setOpenItem] = useState(false);

    const selectItem = () => {
        setSelected(item);
        setOpenItem(!openItem);
    }

    return (
        <Fragment>
            <tr 
            className={selected === item ? "bg-primary white" : ""} 
            style={{cursor: 'pointer'}}
            onClick={() => selectItem()}
            > 
                <td style={{"padding-left": indentationItem}}>
                    {children && (openItem ? <ChevronDown size={18} /> : <ChevronRight size={18} />)}
                    {children ? <Folder size={18} /> : <FileText size={18} /> } {children ? item.full_name : item.nombre}
                </td>
                <td className="text-right">{item.numero}</td>
            </tr>
            {openItem && children && children.map(itemChild => (
                    <Item 
                        indentation={indentation+10}
                        item={itemChild} 
                        children={filterChildren(titulos, itemChild)} 
                        titulos={titulos}
                        filterChildren={filterChildren}
                        selected={selected}
                        setSelected={setSelected}
                    />))}
            {openItem && item.cuentas && item.cuentas.map(itemChild => (
                    <Item 
                        indentation={indentation+10}
                        item={itemChild} 
                        children={null}
                        titulos={titulos}
                        filterChildren={filterChildren}
                        selected={selected}
                        setSelected={setSelected}
                    />))}                    
        </Fragment>
    
      )
};

const mapDispatchToProps = dispatch => ({
    setSelected: payload => dispatch(titulosActions.select(payload))
})

export default connect(
    null,
    mapDispatchToProps
)(Item)