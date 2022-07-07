// ! React

const Encabezado = ({
    documento,
    setDocumento,
    onlyRead,
    types,
    }) => {

    const reload = (e)=> {
        const param = e.target.name
        const value = e.target.value
        var URL = document.URL;
        var NEW = `${param}=${value}`;
        if(URL.indexOf('receipt_type') != -1) {
        var PARAMETER = URL.split("&").filter((par)=> par.indexOf('receipt_type') != -1)[0]
        URL = URL.replace(PARAMETER, NEW)
        }
        else {
        URL = URL + "&" + NEW
        }
        window.location = URL;
}

    return (
        <div className="row">
        <div className="col-md-12">
          <div className="portlet">
            <div className="portlet-heading bg-info">
                <h3 className="portlet-title">Encabezados</h3>
                <div className="portlet-widgets">
                    <a data-toggle="collapse" data-parent="#accordion-encabezados" href="#portlet-encabezados"><i className="fa fa-minus"></i></a>
                </div>
                <div className="clearfix"></div>
            </div>
            <div id="portlet-encabezados" className="panel-collapse collapse in">
                <div className="portlet-body">
                  <div className="row">
                    <div className="col-md-2">
                        <select className="form-control" name="receipt_type" id="receipt_type" onChange={reload}>
                            {Object.keys(types).map((type, i) => (
                                <option key={i} value={type}>{type}</option>
                            ))}
                        </select>
                    </div>
                    <div className="col-md-2">
                        <input className="form-control" name="fecha_operacion" id="date" onChange={reload}/>

                    </div>                    
                  </div>
                </div>
            </div>
          </div>             
        </div>
      </div>
    )
};





const Comprobante = ({ initialData, tipos_cbte, onlyRead }) => {
    
    const [documento, setDocumento] = React.useState({
        id: initialData ? initialData.id : null,
        fecha_operacion: onlyRead ? (initialData && initialData.fecha_operacion) : Date.now(),
        // destinatario: destinatario ? destinatario.id : null,
        descripcion: '',
        receipt: {
          receipt_type: '',
          point_of_sales: '',
          issued_date: onlyRead ? (initialData && initialData.receipt.issued_date) : Date.now(),
        }
      });
  
    React.useEffect(() => {
      if (!documento.creditos) {   
        setDocumento((state) => ({
          ...state,
          contado: false,
          creditos: []
        }))
      }
  
    }, [documento, setDocumento]);    
  
  
    const checkCondition = () => {
      if (documento.creditos && documento.creditos.length > 0) {
        return true;
      }
      return false;
    } 
  
    const handleSubmit = React.useCallback((event) => {
      event.preventDefault();
      console.log("hola")
    }, []);
  

    return (
      <form onSubmit={handleSubmit}>
        <Encabezado 
          documento={documento} 
          setDocumento={setDocumento} 
          onlyRead={onlyRead}
          types={tipos_cbte}
        />
  
        {/* <CreditoNew 
          documento={documento} 
          setDocumento={setDocumento} 
          destinatario={destinatario} 
          errors={errors} 
          onlyRead={onlyRead}/>
  
        <Descripcion 
          documento={documento} 
          setDocumento={setDocumento}
          onlyRead={onlyRead}/>
  
        {!onlyRead && 
          <Contado 
          documento={documento}     
          setDocumento={setDocumento}
          onlyRead={onlyRead} />
        }
        
        <Buttons 
          documento={documento}     
          onlyRead={onlyRead} 
          required={checkCondition()} />
   */}
      </form>
    );
  };


const app = document.querySelector('#app')
const initialData = JSON.parse(document.getElementById('initialData').textContent)
const tipos_cbte = JSON.parse(document.getElementById('tipos_cbte').textContent)
ReactDOM.createRoot(
    app
).render(
    <Comprobante initialData={initialData} tipos_cbte={tipos_cbte} onlyRead={false} />
)