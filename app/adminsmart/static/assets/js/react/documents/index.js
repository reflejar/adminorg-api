// ! React

const initialData = JSON.parse(document.getElementById('initialData').textContent)
const CHOICES = JSON.parse(document.getElementById('choices').textContent)

const Portlet = ({
  title,
  handler,
  children
}) => {

  return (
    <div className="row">
    <div className="col-md-12">
      <div className="portlet">
        <div className="portlet-heading bg-info">
            <h3 className="portlet-title">{title}</h3>
            <div className="portlet-widgets">
                <a data-toggle="collapse" data-parent={`#accordion-${handler}`} href={`#portlet-${handler}`}><i className="fa fa-minus"></i></a>
            </div>
            <div className="clearfix"></div>
        </div>
        <div id={`#portlet-${handler}`} className="panel-collapse collapse in">
            <div className="portlet-body">
              {children}
            </div>
        </div>
      </div>             
    </div>
  </div>
  )
}


const Encabezado = ({
    documento,
    setDocumento,
    onlyRead,
    }) => {

    const types = Object.keys(CHOICES.receipt.receipt_type)
    const point_of_sales = Object.keys(CHOICES.receipt.point_of_sales)

    const reload = (e)=> {
        let param = e.target.name
        if (param.split('.').length > 1) param = param.split('.')[1]
        const value = e.target.value
        var URL = document.URL;
        var NEW = `${param}=${value}`;
        if(URL.indexOf(param) != -1) {
          var PARAMETER = URL.split("&").filter((par)=> par.indexOf(param) != -1)[0]
          URL = URL.replace(PARAMETER, NEW)
        }
        else {
          URL = URL + "&" + NEW
        }
        window.location = URL;
    }

    const handleChange = (e) => {
      const name = e.target.name
      const subfields = name.split(".")
      subfields.length > 1 ?
        setDocumento({
          ...documento,
          [subfields[0]]: {
            ...documento[subfields[0]],
            [subfields[1]]: e.target.value
          }
        }) :
        setDocumento({
          ...documento,
          [name]: e.target.value
        })
    }

    return (
        <Portlet title="Encabezados" handler='encabezados'>
          <div className="row">
            <div className="col-md-2">
              <label htmlFor="receipt.receipt_type">Tipo</label>
              <select 
                className="form-control" 
                name="receipt.receipt_type" 
                id="receipt.receipt_type" 
                onChange={reload}
                value={documento.receipt.receipt_type || ''}
                >
                <option value=''> --- </option>
                {types.map((type, i) => (
                    <option key={i} value={type}>{type}</option>
                ))}
              </select>
            </div>
            <div className="col-md-2">
              <label htmlFor="receipt.point_of_sales">Punto Vta</label>
              <select 
              className="form-control"
              name="receipt.point_of_sales" 
              id="receipt.point_of_sales" 
              onChange={handleChange}
              value={documento.receipt.point_of_sales || ''}
            >
              <option value=''> --- </option>
                {point_of_sales.map((point, i) => (
                    <option key={i} value={point}>{point}</option>
                ))}
              </select>
            </div>            
            <div className="col-md-2">
              <label htmlFor="receipt.receipt_number">N°</label>
              <input 
                type="number" 
                className="form-control" 
                name="receipt.receipt_number" 
                id="receipt.receipt_number" 
                onChange={handleChange}
                value={documento.receipt.receipt_number || ''}
              />
            </div>              
            <div className="col-md-2">
              <label htmlFor="receipt.issued_date">Fecha Cbte.</label>
              <input className="form-control" name="receipt.issued_date" type="date" onChange={handleChange}/>
            </div>               
            <div className="col-md-2">
              <label htmlFor="fecha_operacion">Fecha Op.</label>
              <input 
                className="form-control" 
                name="fecha_operacion" 
                type="date" 
                onChange={reload}
                value={documento && documento.fecha_operacion || ''}
              />
            </div>                    
          </div>
        </Portlet>
    )
};



const Appendable = ({ documento, setDocumento, onlyRead, title, handler, fields, cleanedField }) => {

  const [grouped, setGrouped] = React.useState([...documento[handler], cleanedField])

  const handleChange = (e) => {
    e.preventDefault()
    const [row, name] = e.target.name.split('.')
    setGrouped(() => {
      grouped[row][name] = e.target.value
      return [...grouped]
    })
  }

  React.useEffect(() => {
    setDocumento(() => ({
      ...documento,
      [handler]: grouped
    }))

  }, [grouped])

  const renderField = (field, value, fi) => {
    switch (field.type) {
      case 'select':
        return <select className="form-control input-sm" name={`${fi}.${field.name}`} value={value || ''} onChange={handleChange}>
          <option value=''> --- </option>
          {Object.keys(field.choices).map((c, i) => (
            <option key={i} value={c}>{field.choices[c]}</option>
          ))}
        </select>
      case 'date':
        return <input className="form-control input-sm" type="date" name={`${fi}.${field.name}`} value={value || ''} onChange={handleChange} />
      case 'text':
        return <input className="form-control input-sm" type="text" name={`${fi}.${field.name}`} value={value || ''} onChange={handleChange} />
      case 'number':
        return <input className="form-control input-sm" type="number" name={`${fi}.${field.name}`} value={value || ''} onChange={handleChange} />        
      default:
        break;
    }
  }

  return (
    <Portlet title={title} handler={handler}>
      <div className="row">
        <div className="col-md-12">
          <table className="table table-condensed">
            <thead>
              <tr>
                {fields.map((field, i) => (<th key={i}>
                  {field.label}
                </th>))}
              </tr>
            </thead>
            <tbody>
              {grouped.map((fieldset, fi) => (
                <tr key={fi}>
                {fields.map((field, i) =>(
                  <td key={i}>
                    {renderField(field, fieldset[field.name], fi)}
                  </td>
                ))}
                </tr>
              ))}

            </tbody>
          </table>
        </div>            
        <div className="col-md-offset-11">
          <button className="btn btn-sm btn-danger text-right"><span className="fa fa-minus"></span></button>
          <button className="btn btn-sm btn-success text-right"><span className="fa fa-plus"></span></button>
        </div>
      </div>
    </Portlet>
)  
};

const Selectable = ({ documento, setDocumento, onlyRead, title, handler, rows }) => {



  return (
    <Portlet title={title} handler={handler}>
      <div className="row">
        <div className="col-md-12">
          <table className="table table-condensed">
            <thead>
              <tr>
                <th>Apa1</th>
                <th>Apalalala2</th>
              </tr>
            </thead>
            <tbody>
              {Object.keys(rows).map((row, i) => (
                <tr key={i}>
                  <td><input className="form-control" type="checkbox" name={`algo`} /></td>
                  <td><input className="form-control" type="number" name={`monto`} /></td>
                </tr>
              ))}

            </tbody>
          </table>
        </div>
      </div>
    </Portlet>
)  
};


const Comprobante = ({ initialData, onlyRead }) => {
    var URL = document.URL
    let queryParams 
    if((URL).indexOf('?') != -1) {
      var search = location.search.substring(1);
      queryParams = JSON.parse('{"' + decodeURI(search).replace(/"/g, '\\"').replace(/&/g, '","').replace(/=/g,'":"') + '"}')
    }
    let fieldsLists = {}
    Object.keys(initialData).forEach(field => {
      if (initialData[field] instanceof Array) {
        fieldsLists[field] = initialData[field]
      }
      
    })

    const [documento, setDocumento] = React.useState({
        id: initialData ? initialData.id : null,
        fecha_operacion: (queryParams && queryParams.fecha_operacion) ? 
          queryParams.fecha_operacion : 
          initialData.fecha_operacion ? 
          initialData.fecha_operacion : 
          Date.now(),
        descripcion: '',
        receipt: {
          receipt_type: (queryParams && queryParams.receipt_type) ? queryParams.receipt_type : initialData.receipt.receipt_type,
          point_of_sales: initialData.receipt.point_of_sales ? initialData.receipt.point_of_sales : '',
          issued_date: initialData.receipt.issued_date ? initialData.receipt.issued_date : Date.now(),
          receipt_number: initialData.receipt.receipt_number ? initialData.receipt.receipt_number : '',
        },
        ...fieldsLists
      });  
  
    const canSend = () => {
      return false;
    } 
  
    const handleSubmit = React.useCallback((event) => {
      event.preventDefault();
      console.log(event)
    }, []);

    const handleBack = (e) => {
      history.back()
    }

    return (
      <form onSubmit={handleSubmit}>
        <Encabezado 
          documento={documento} 
          setDocumento={setDocumento} 
          onlyRead={onlyRead}
        />

        {/* Clientes: Seccion de Creditos */}
        {Object.keys(fieldsLists).length > 0 && fieldsLists.creditos && <Appendable 
          documento={documento} 
          setDocumento={setDocumento} 
          onlyRead={onlyRead}
          title="Creditos"
          handler="creditos"
          fields={[
            {
              type: 'select',
              name: 'destinatario',
              label: 'Destinatario',
              choices: CHOICES.creditos.destinatario
            },
            {
              type: 'select',
              name: 'concepto',
              label: 'Concepto',
              choices: CHOICES.creditos.concepto
            },
            {
              type: 'date',
              name: 'fecha_indicativa',
              label: 'Periodo',
            },
            {
              type: 'date',
              name: 'fecha_descuento',
              label: 'Descuento',
            },            
            {
              type: 'date',
              name: 'fecha_vencimiento',
              label: 'Vencimiento',
            },
            {
              type: 'text',
              name: 'detalle',
              label: 'Detalle',
            },
            {
              type: 'number',
              name: 'cantidad',
              label: 'Cantidad',
            },            
            {
              type: 'number',
              name: 'monto',
              label: 'Monto',
            },                        
          ]}
          cleanedField={{
            destinatario: '',
            concepto: '',
            fecha_indicativa: '',
            fecha_descuento: '',
            fecha_vencimiento: '',
            detalle: '',
            cantidad: 0,
            monto: 0,
          }}
          />
        }
        {/* Clientes: Seccion de Cobros */}
        {Object.keys(fieldsLists).length > 0 && fieldsLists.cobros && <Selectable 
          documento={documento} 
          setDocumento={setDocumento} 
          onlyRead={onlyRead}
          title="Items pendientes de cobro"
          handler="cobros"
          rows={CHOICES.cobros.vinculo}
          />
        }        
  
        
        {/* Seccion de Cajas */}
        {Object.keys(fieldsLists).length > 0 && fieldsLists.cajas && <Appendable 
          documento={documento} 
          setDocumento={setDocumento} 
          onlyRead={onlyRead}
          title="Formas de pago"
          handler="cajas"
          fields={[
            {
              type: 'select',
              name: 'cuenta',
              label: 'Cuenta',
              choices: CHOICES.cajas.cuenta
            },
            {
              type: 'text',
              name: 'detalle',
              label: 'Detalle',
            },                 
            {
              type: 'date',
              name: 'fecha_vencimiento',
              label: 'Vencimiento',
            },          
            {
              type: 'number',
              name: 'monto',
              label: 'Monto',
            },                        
          ]}
          cleanedField={{
            cuenta: '',
            detalle: '',
            fecha_vencimiento: '',
            monto: 0,
          }}
          />
        }

        {/* Seccion de Cajas */}
        {Object.keys(fieldsLists).length > 0 && fieldsLists.resultados && <Appendable 
          documento={documento} 
          setDocumento={setDocumento} 
          onlyRead={onlyRead}
          title="Resultados a generar"
          handler="resultados"
          fields={[
            {
              type: 'select',
              name: 'cuenta',
              label: 'Cuenta',
              choices: CHOICES.resultados.cuenta
            },
            {
              type: 'text',
              name: 'detalle',
              label: 'Detalle',
            },                 
            {
              type: 'date',
              name: 'fecha_indicativa',
              label: 'Período',
            },          
            {
              type: 'number',
              name: 'monto',
              label: 'Monto',
            },                        
          ]}
          cleanedField={{
            cuenta: '',
            detalle: '',
            fecha_indicativa: '',
            monto: 0,
          }}
          />
        }                
  
        <Portlet 
          title="Descripción"
          handler="descripcion">
          <div className="row">
            <div className="col-md-12">
              <label htmlFor="descripcion">Descripción</label>
              <input 
                type="text" 
                id='descripcion' 
                name="descripcion" 
                className="form-control" 
                value={documento.descripcion || ''}
                onChange={(e) => setDocumento({...documento, descripcion: e.target.value})}
              />
            </div>            
          </div>                        
        </Portlet>
  
        {/* {!onlyRead && 
          <Contado 
          documento={documento}     
          setDocumento={setDocumento}
          onlyRead={onlyRead} />
        } */}
        
        <div className="panel-footer">
          <div className="row">
            <div className="col-xs-6">
              <button onClick={handleBack} className="btn btn-bordered btn-default btn-block">Cancelar</button>
            </div>
            <div className="col-xs-6">
              <button type="submit" disabled={!canSend()} onClick={handleSubmit} className="btn btn-bordered btn-primary btn-block">Guardar</button>
            </div>
          </div>
        </div>
      </form>
    );
  };


const app = document.querySelector('#app')

ReactDOM.createRoot(
    app
).render(
    <Comprobante initialData={initialData} onlyRead={false} />
)