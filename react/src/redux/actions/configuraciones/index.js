const select = (id) => ({
    type: 'SELECT_PARAMETRO',
    id
})

const get_all = () => async (dispatch) => {
    const payload = [
      {id: "",full_name: "Area Relaciones Humanas"},
      {id: "cliente",full_name: "Clientes y Socios"},
      {id: "dominio",full_name: "Dominios"},
      {id: "proveedor",full_name: "Proveedores"},
      {id: "",full_name: "Area Economica"},
      {id: "caja",full_name: "Tesoreria"},
      {id: "ingreso",full_name: "Ingresos"},
      {id: "gasto",full_name: "Gastos"},
      {id: "interes",full_name: "Metodologia de Intereses"},
      {id: "descuento",full_name: "Metodologia de Descuentos"},
      {id: "retencion",full_name: "Configuracion de Retenciones"},
      {id: "",full_name: "Area Contable"},
      {id: "titulo",full_name: "Cuentas y titulos contables"},
    ]

    dispatch({
        type: 'GET_PARAMETROS',
        payload: payload
    });
}


export const configuracionesActions = {
    get_all,
    select,
}
