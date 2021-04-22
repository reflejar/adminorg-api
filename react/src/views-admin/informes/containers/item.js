import React, {Fragment, useState} from "react";
import { connect } from "react-redux";
import { Folder, ChevronRight, ChevronDown, FileText } from "react-feather";
import { carpetasActions } from "../../../redux/actions/carpetas";


const Item = ({ indentation, item, children, carpetas, filterChildren, selected, setSelected }) => {
    const indentationItem = indentation + "px";

    const [openItem, setOpenItem] = useState(false);

    const selectItem = () => {
        setSelected(item);
        setOpenItem(!openItem);
    }

    return (
        <Fragment>
            <tr 
            className={selected && (selected.id === item.id ? "bg-primary white" : "")} 
            style={{cursor: 'pointer'}}
            onClick={() => selectItem()}
            > 
                <td style={{"paddingLeft": indentationItem}}>
                    {children && (openItem ? <ChevronDown size={18} /> : <ChevronRight size={18} />)}
                    {children ? <Folder size={18} /> : <FileText size={18} /> } {children ? item.full_name : item.nombre}
                </td>
            </tr>
            {openItem && children && children.map((itemChild, keyChild) => (
                    <Item 
                        indentation={indentation+10}
                        item={itemChild} 
                        key={keyChild}
                        children={filterChildren(carpetas, itemChild)} 
                        carpetas={carpetas}
                        filterChildren={filterChildren}
                        selected={selected}
                        setSelected={setSelected}
                    />))}
            {openItem && item.archivos && item.archivos.sort((a, b) => a.nombre.localeCompare(b.nombre)).map((itemChild, keyChild) => (
                    <Item 
                        indentation={indentation+10}
                        item={itemChild} 
                        key={keyChild}
                        children={null}
                        carpetas={carpetas}
                        filterChildren={filterChildren}
                        selected={selected}
                        setSelected={setSelected}
                    />))}                    
        </Fragment>
    
      )
};

const mapDispatchToProps = dispatch => ({
    setSelected: payload => dispatch(carpetasActions.select(payload))
})

export default connect(
    null,
    mapDispatchToProps
)(Item)