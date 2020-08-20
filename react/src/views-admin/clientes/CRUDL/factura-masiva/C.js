import React, { useState } from 'react';
import { connect, useDispatch } from 'react-redux';
import moment from 'moment';
import get from 'lodash/get';

import { Table, FormGroup, Label, Input } from 'reactstrap';

// Components
import Spinner from '../../../../components/spinner/spinner';
import { AppendableRowField } from '../../../../components/form/AppendableRowField';

// Styles
import './index.scss';

// Redux
import { useClientList } from '../../../../utility/hooks/selectors'
import { useIngresos, usePuntosDeVenta, usePreconceptos, useDominios } from '../../../../utility/hooks/dispatchers'
import { mapToOptions } from '../../../../utility/mappers';
import { masivaActions } from '../../../../redux/actions/masiva';

const preconceptosHeaders = ['-', 'Destinatario', 'Ingreso', 'Periodo', 'Detalle', 'Fecha V', 'Fecha G', 'Monto'];

const Create = (props) => {
  const clients = useClientList();
  const [puntos] = usePuntosDeVenta();
  const dispatch = useDispatch();
  const [preconceptos, preconceptosLoading] = usePreconceptos();
  const [dominios, dominiosLoading] = useDominios();
  const [ingresos, loadingIngresos] = useIngresos();
  const [selectedPreconceptos, setSelectedPreconceptos] = useState([]);
  const [disabledFields, setDisabledFields] = useState({});
  const [invoice, setInvoice] = useState({
    fecha_operacion: moment().format('YYYY-MM-D'),
    descripcion: '',
    receipt: {
      point_of_sales: '',
      issued_date: moment().format('YYYY-MM-D'),
      concept: ''
    },
    distribuciones: [{
      ingreso: '',
      unidad: '',
      fecha_vencimiento: null,
      fecha_gracia: null,
      monto: 0,
    }],
    preconceptos: []
  });

  const isAllowed = !invoice.receipt.point_of_sales || !invoice.fecha_operacion || !invoice.receipt.concept;

  const appendFieldToArray = (path) => () => {
    setInvoice({ ...invoice, [path]: [...invoice[path], {}] });
  };

  const popRowField = (path) => () => {
    setInvoice({
      ...invoice,
      [path]: invoice[path].slice(0, invoice[path].length - 1)
    });
  };

  const handleChange = (event) => {
    const { name, value } = event.target;

    if (name === 'point_of_sales' || name === 'issued_date') {
      return setInvoice({
        ...invoice,
        receipt: {
          ...invoice.receipt,
          [name]: value
        }
      });
    }

    setInvoice({ ...invoice, [name]: value });
  }

  const handleNestedFieldChange = (field) => (event) => {
    event.persist();
    const { name, value } = event.target;

    setInvoice({
      ...invoice,
      [field]: {
        ...invoice[field],
        [name]: value
      }
    });
  };

  const handleArrayFieldChange = (field) => (index) => (event) => {
    event.persist();

    const { name, value } = event.target;

    if (field === 'distribuciones' && name === 'monto' && value <= 0) {
      return;
    }

    if (field === 'distribuciones' && name === 'ingreso' && value) {
      const ingreso = ingresos.find((ingreso) => ingreso.id === +value) || {};

      setDisabledFields({
        fecha_gracia: !(ingreso.interes && !isNaN(ingreso.interes)),
        fecha_vencimiento: !(ingreso.descuento && !isNaN(ingreso.descuento))
      });
    }

    setInvoice({
      ...invoice,
      [field]: invoice[field].map((item, i) => {
        if (i === index) {
          return {
            ...item,
            [name]: value
          }
        }

        return item;
      })
    });
  };

  const handlePreconceptoSelect = (index) => (event) => {
    const { checked } = event.target;

    if (checked) {
      setSelectedPreconceptos([...selectedPreconceptos, index]);
    } else {
      setSelectedPreconceptos(selectedPreconceptos.filter((x) => x !== index));
    }
  }

  const handleSubmit = (event) => {
    event.preventDefault();

    const preconceptosIds = selectedPreconceptos.map((index) => preconceptos[index].id);

    const masivaData = {
      ...invoice,
      preconceptos: preconceptosIds
    };

    dispatch(masivaActions.post(masivaData))
      .then(() => {
        props.onClose();
      });
  }

  if (loadingIngresos || preconceptosLoading || dominiosLoading) {
    return (
      <div className='loading-modal'>
        <Spinner />
      </div>
    )
  }

  return (
    <form className='credito-invoice container' onSubmit={handleSubmit}>
      <div className='row'>
        <div className='form-group col-md-3'>
          <label htmlFor='point_of_sales'>Punto de venta: </label>
          <select
            className='form-control'
            name='point_of_sales'
            id='point_of_sales'
            value={invoice.receipt.point_of_sales}
            onChange={handleNestedFieldChange('receipt')}
          >
            <option value=''>---</option>

            {puntos.map((punto) => (
              <option value={punto.number} key={punto.number}>{punto.number}</option>
            ))}
          </select>
        </div>

        <div className='form-group col-md-3'>
          <label htmlFor='fecha_operacion'>Fecha de operación:</label>
          <input
            type='date'
            className='form-control d-block'
            name='fecha_operacion'
            id='fecha_operacion'
            value={invoice.fecha_operacion}
            onChange={handleChange} />
        </div>

        <div className='form-group col-md-3'>
          <label htmlFor='issued_date'>Fecha de Comprobante:</label>
          <input
            type='date'
            className='form-control d-block'
            name='issued_date'
            id='issued_date'
            value={invoice.receipt.issued_date}
            onChange={handleNestedFieldChange('receipt')} />
        </div>

        <div className='form-group col-md-3'>
          <label htmlFor='concept'>Concepto:</label>

          <select
            className='form-control'
            name='concept'
            id='concept'
            value={invoice.receipt.concept}
            onChange={handleNestedFieldChange('receipt')}
          >
            <option value=''>---</option>
            <option value="servicios">Servicios</option>
            <option value="producto">Producto</option>
            <option value="productos y servicios">Productos y servicios</option>
          </select>
        </div>
      </div>

      <AppendableRowField
        onAppendClick={appendFieldToArray('distribuciones')}
        onPopClick={popRowField('distribuciones')}
        data={invoice.distribuciones}
        fields={[{
          type: 'select',
          name: 'ingreso',
          placeholder: 'Ingreso',
          header: 'Ingreso',
          handleChange: handleArrayFieldChange('distribuciones'),
          options: (
            <>
              <option defaultValue="">---</option>

              {mapToOptions(ingresos).map((ingreso) => (
                <option key={ingreso.value} value={ingreso.value}>
                  {ingreso.label}
                </option>
              ))}
            </>
          ),
        }, {
          type: 'select',
          name: 'unidad',
          placeholder: 'Distribucion',
          header: 'Distribucion',
          handleChange: handleArrayFieldChange('distribuciones'),
          options: (
            <>
              <option value="socio">Total por socio</option>
              <option value="dominio">Total por dominio</option>
              <option value="m2">Total por m2</option>
            </>
          ),
        }, {
          type: 'date',
          name: 'fecha_vencimiento',
          placeholder: 'Fecha Vencimiento',
          header: 'Fecha Vencimiento',
          disabled: disabledFields.fecha_vencimiento,
          handleChange: handleArrayFieldChange('distribuciones')
        }, {
          type: 'date',
          name: 'fecha_gracia',
          placeholder: 'Fecha de Gracia',
          header: 'Fecha de Gracia',
          disabled: disabledFields.fecha_gracia,
          handleChange: handleArrayFieldChange('distribuciones')
        }, {
          type: 'number',
          name: 'monto',
          placeholder: 'Monto',
          header: 'Monto',
          handleChange: handleArrayFieldChange('distribuciones')
        }]}
        header={{
          title: 'Operaciones de distribucion',
          appendButton: 'Agregar deuda'
        }}
      />

      <h3 className="pl-0 credito__row__header__text">
        Preconceptos
      </h3>

      <Table>
        <thead>
          <tr>
            {preconceptosHeaders.map((header) => (
              <th key={header}>{header}</th>
            ))}
          </tr>
        </thead>

        <tbody>
          {preconceptos.map((row, index) => {
            let destinatario = get(clients.find((x) => x.id === row.destinatario), 'perfil.nombre', '');
            if (!destinatario) {
              destinatario = get(dominios.find((x) => x.id === row.destinatario), 'nombre', '');
            }

            const ingreso = get(ingresos.find((x) => x.id === row.ingreso), 'nombre', '');

            return (
              <tr key={index}>
                <td>
                  <FormGroup check style={{ display: 'flex' }}>
                    <Label check>
                      <Input
                        type="checkbox"
                        onChange={handlePreconceptoSelect(index)}
                        checked={!isNaN(selectedPreconceptos.find((x) => x === index))}
                      />
                    </Label>
                  </FormGroup>
                </td>
                <td>{destinatario}</td>
                <td>{ingreso}</td>
                <td>{row.periodo}</td>
                <td>{row.detalle}</td>
                <td>{row.fecha_vencimiento}</td>
                <td>{row.fecha_gracia}</td>
                <td>{row.monto}</td>
              </tr>
            );
          })}
        </tbody>
      </Table>

      <div className='row'>
        <div className='col-12'>
          <h3 className='credito__row__header__text mt-2'>
            Descripción
          </h3>

          <div className='form-group'>
            <textarea
              className='form-control'
              name='descripcion'
              rows={3}
              value={invoice.descripcion}
              onChange={handleChange} />
          </div>
        </div>
      </div>

      <div className='row'>
        <div className='col-12 text-right'>
          <button type='button' className='btn btn-secondary mr-2' onClick={props.onClose}>
            Cancelar
            </button>

          <button type='submit' className='btn btn-primary' disabled={isAllowed}>
            Guardar
          </button>
        </div>
      </div>
    </form>
  );
};

export default connect(null)(Create);
