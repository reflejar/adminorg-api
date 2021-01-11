import React, { useState } from 'react';
import moment from 'moment';
import get from 'lodash/get';
import * as Yup from 'yup';
import csvtojson from 'csvtojson';
import { CSVLink } from "react-csv";

// Components
import Spinner from '../../../../components/spinner/spinner';
import { useDispatch } from 'react-redux';

// Styles
import './index.scss';
import { Table, FormGroup, Label, Input } from 'reactstrap';
import { ImportFileDropzone } from '../../../../components/dropzone/ImportFileDropzone';
import { usePreconceptos, useDominios, useIngresos, useClientes } from '../../../../utility/hooks/dispatchers';
import { preconceptosActions } from '../../../../redux/actions/preconceptos';

const csvValidations = Yup.object({
  destinatario: Yup
    .string('Destinantario debe ser un texto valido')
    .test('len', 'Destinatario debe ser valido', val => val.length > 0)
    .required('Destinantario es requerido'),
  concepto: Yup
    .string('concepto debe ser un texto valido')
    .test('len', 'Concepto debe ser valido', val => val.length > 0)
    .required('concepto es requerido'),
  periodo: Yup
    .string('periodo debe ser una fecha valida')
    .test('date', 'fecha de gracia debe ser una fecha valida', val => moment(new Date(val)).isValid())
    .required('periodo es requerido'),
  detalle: Yup
    .string('detalle debe ser un texto valido'),
  'fecha v': Yup
    .string('fecha de vencimiento debe ser una fecha valida')
    .test('date', 'fecha de vencimiento debe ser una fecha valida', val => moment(new Date(val)).isValid()),
    // .required('fecha de vencimiento es requerido'),
  'fecha g': Yup
    .string('fecha de gracia debe ser una fecha valida')
    .test('date', 'fecha de gracia debe ser una fecha valida', val => moment(new Date(val)).isValid()),
    // .required('fecha de gracia es requerido'),
  monto: Yup
    .number('Monto debe ser un numero valido')
    .moreThan(-1, 'Monto debe ser un numero mayor que cero (0)')
    .required('Monto es requerido'),
  cantidad: Yup
    .number('Cantidad debe ser un numero valido')
    .moreThan(-1, 'Cantidad debe ser un numero mayor que cero (0)')
});

const tableHeaders = ['Destinatario', 'Concepto', 'Periodo', 'Detalle', 'Fecha V', 'Fecha G', 'Cantidad', 'Monto'];

const Preconceptos = ({ onClose }) => {
  const [dropzone, setDropzone] = useState(false)
  const [csvError, setCSVError] = useState([]);
  const [dominios, loadingDominios] = useDominios();
  const [ingresos, loadingIngresos] = useIngresos();
  const [clientes, loadingClientes] = useClientes();
  const [preconceptos, loadingPreconceptos] = usePreconceptos();
  const [newPreconceptos, setNewPreconceptos] = useState([]);
  const [selectedRows, setSelectedRows] = useState([]);
  const dispatch = useDispatch();

  const handleSubmit = (event) => {
    event.preventDefault();

    const mappedNewPreconceptos = newPreconceptos.map((x) => {
      let destinatario = "";
      if (x.destinatario.charAt(0) === "#") {
        const cleanDominio = x.destinatario.substring(1);
        destinatario = get(dominios.find((val) => val.full_name.toString().toLowerCase() === cleanDominio.toLowerCase()), "id", "");
      } else {
        destinatario = get(clientes.find((val) => val.full_name.toLowerCase() === x.destinatario.toLowerCase()), "id", "");
      }

      return ({
        destinatario: destinatario,
        monto: x.monto,
        cantidad: x.cantidad,
        concepto: get(ingresos.find((val) => val.full_name.toLowerCase() === x.concepto.toLowerCase()), "id", ""),
        detalle: x.detalle,
        periodo: x.periodo,
        fecha_gracia: x['fecha g'] || null,
        fecha_vencimiento: x['fecha v'] || null
      })
    });

    dispatch(preconceptosActions.post(mappedNewPreconceptos))
      .then(onClose);
  }

  const handleDelete = () => {
    const promises = selectedRows.reduce((acc, rowId) => {
      const selectedRow = [...preconceptos, ...newPreconceptos][rowId];

      if (!selectedRow || isNaN(selectedRow.id)) {
        return acc;
      }

      return [...acc, dispatch(preconceptosActions.remove(selectedRow.id))];
    }, []);

    Promise.all(promises)
      .then(() => {
        if (newPreconceptos.length > 0) {
          setNewPreconceptos(newPreconceptos.filter((x, index) => !selectedRows.find((y) => y === (index + preconceptos.length))));
        }

        setSelectedRows([]);
      })

  }

  const togglefileDropzone = () => {
    setDropzone(!dropzone)
  }
  const handleRowSelect = (index) => (event) => {
    const { checked } = event.target;

    if (checked) {
      setSelectedRows([...selectedRows, index]);
    } else {
      setSelectedRows(selectedRows.filter((x) => x !== index));
    }
  }

  const handleDrop = (files) => {
    // Cleaning previous errors
    setCSVError([]);

    const reader = new FileReader();

    reader.readAsText(files[0]);

    reader.onloadend = async (event) => {
      const csvArr = await csvtojson().fromString(event.target.result)
        .then((arr) => {
          // Mapping keys to lowercase
          return arr.map((row) => {
            const keys = Object.keys(row);

            return keys.reduce((acc, key) => {
              const loweredKey = key.toLowerCase();
              let value = row[key];

              // Edge case casting
              if (loweredKey === 'monto' || loweredKey === "cantidad") {
                value = Number(value);
              }

              return { ...acc, [loweredKey]: value };
            }, {});

          })
        });

      let errors = [];

      // All fields are present and of a valid type (Running with YUP validations)
      (await Promise.all(csvArr.map((row) => csvValidations.validate(row).catch((err) => err))))
        .find((val, index) => {
          if (val && val.errors && val.errors.length && val.message) {
            const error = val.message;
            const errorRowLine = index + 1;
            const message = `Linea ${errorRowLine}: ` + error;
            errors.push(message);
            return true;
          }
          return false;
        });

      // All relational fields (e.g destinatario, expensa) match correctly and their ids exists
      csvArr.forEach((row, index) => {
        const { destinatario, concepto } = row;

        // The inserted 'concepto' exists
        const matchedConcepto = ingresos.some((val) => val.nombre.toLowerCase() === concepto.toLowerCase());
        if (!matchedConcepto) {
          const error = `Concepto "${concepto}" no encontrado`;
          const errorRowLine = index + 1;
          const message = `Linea ${errorRowLine}: ` + error;    
          errors.push(message);
        }
        if (destinatario.charAt(0) === "#") {
          const cleanDominio = destinatario.substring(1);
          const matchedDominio = dominios.some((val) => val.full_name.toString().toLowerCase() === cleanDominio.toLowerCase());
          if (!matchedDominio) {
            const error = `Dominio "${destinatario}" no encontrado`;
            const errorRowLine = index + 1;
            const message = `Linea ${errorRowLine}: ` + error;    
            errors.push(message);
  
          }
        } else {
          const matchedClient = clientes.some((val) => val.full_name.toLowerCase() === destinatario.toLowerCase());
          if (!matchedClient) {
            const error = `Cliente "${destinatario}" no encontrado`;
            const errorRowLine = index + 1;
            const message = `Linea ${errorRowLine}: ` + error;
            errors.push(message);
        }


        }
      });

      if (errors.length > 0) {
        setCSVError([...errors]);
        return;
      } else {
        setNewPreconceptos(csvArr);
      }
    };
  }

  if (loadingPreconceptos || loadingDominios || loadingIngresos || loadingClientes) {
    return (
      <div className='loading-modal'>
        <Spinner />
      </div>
    );
  }

  return (
    <>
      <form onSubmit={handleSubmit}>
        {preconceptos.length === 0 && (
          <h4>
            No se encontraron preconceptos
          </h4>
        )}

        {(preconceptos.length || newPreconceptos.length) > 0 && (
          <Table>
            <thead>
              <tr>
                {/* Empty th tag for the table checkbox */}
                <th />

                {tableHeaders.map((header) => (
                  <th key={header}>{header}</th>
                ))}
              </tr>
            </thead>

            <tbody>
              {[...preconceptos, ...newPreconceptos].map((row, index) => {
                let destinatario = get(clientes.find((x) => x.id === row.destinatario), 'full_name', '');
                if (!destinatario) {
                  destinatario = get(dominios.find((x) => x.id === row.destinatario), 'full_name', '');
                  if (destinatario) {
                    destinatario = "#" + destinatario
                  }
                }

                const concepto = get(ingresos.find((x) => x.id === row.concepto), 'nombre', '');

                return (
                  <tr className={row.id ? "" : "warning"} key={index}>
                    <td>
                      <FormGroup check style={{ display: 'flex' }}>
                        <Label check>
                          <Input
                            type="checkbox"
                            onChange={handleRowSelect(index)}
                            checked={Boolean(selectedRows.find((x) => x === index))}
                          />
                        </Label>
                      </FormGroup>
                    </td>
                    <td>{destinatario || row.destinatario}</td>
                    <td>{concepto || row.concepto}</td>
                    <td>{row.periodo}</td>
                    <td>{row.detalle}</td>
                    <td>{row.fecha_vencimiento || row['fecha v']}</td>
                    <td>{row.fecha_gracia || row['fecha g']}</td>
                    <td>{row.cantidad}</td>
                    <td>{row.monto}</td>
                  </tr>
                )
              })}
            </tbody>
          </Table>
        )}

        <ul>
          {csvError.length > 0 && csvError.map(error => (
              <li className="danger">{error} </li>
          ))}
        </ul>

        {dropzone && (
          <>
          <div className="ImportFileDropzone__container">
            <ImportFileDropzone onDrop={handleDrop} />
          </div>
            <p>
            Necesitas un archivo modelo? podes hacer <CSVLink filename={"importador-preconceptos.csv"} data={[tableHeaders]}>click aqui</CSVLink>
          </p>            
          </>
        )}

        <div className='row'>
          <div className='col-12 text-right'>
            <button type='button' className='btn btn-secondary mr-2' onClick={onClose}>
              Cancelar
            </button>

            <button
              type='button'
              className='btn btn-danger mr-2'
              disabled={preconceptos.length === 0}
              onClick={handleDelete}
            >
              Eliminar
            </button>

            <button
              type='button'
              className='btn btn-warning mr-2'
              onClick={togglefileDropzone}
            >
              Importar
            </button>

            <button
              type='submit'
              className='btn btn-primary'
              disabled={newPreconceptos.length === 0}
            >
              Guardar
            </button>
          </div>
        </div>
      </form>
    </>
  );
}

export default Preconceptos;