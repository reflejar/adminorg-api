import React, { useState } from 'react';
import moment from 'moment';
import get from 'lodash/get';
import * as Yup from 'yup';
import csvtojson from 'csvtojson';

// Components
import Spinner from '../../../../components/spinner/spinner';
import Response from '../../../../components/responses/responses';
import { useDispatch } from 'react-redux';

// Styles
import './index.scss';
import { Table, FormGroup, Label, Input, Alert } from 'reactstrap';
import { ImportFileDropzone } from './ImportFileDropzone';
import { usePreconceptos, useDominios, useIngresos } from '../../../../utility/hooks/dispatchers';
import { useClientList } from '../../../../utility/hooks/selectors';
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
    .test('date', 'fecha de vencimiento debe ser una fecha valida', val => moment(new Date(val)).isValid())
    .required('fecha de vencimiento es requerido'),
  'fecha g': Yup
    .string('fecha de gracia debe ser una fecha valida')
    .test('date', 'fecha de gracia debe ser una fecha valida', val => moment(new Date(val)).isValid())
    .required('fecha de gracia es requerido'),
  monto: Yup
    .number('Monto debe ser un numero valido')
    .moreThan(-1, 'Monto debe ser un numero mayor que cero (0)')
    .required('Monto es requerido'),
  cantidad: Yup
    .number('Cantidad debe ser un numero valido')
    .moreThan(-1, 'Cantidad debe ser un numero mayor que cero (0)')
});

const tableHeaders = ['Destinatario', 'Concepto', 'Periodo', 'Detalle', 'Fecha V', 'Fecha G', 'Cantidad', 'Monto'];

const initialState = {
  selectedRows: [],
  fileDropzone: {
    open: false,
    file: null
  },
  loading: false,
  result: null,
  data: [
    {
      monto: 0,
      cantidad:0,
      detalle: '',
      destinatario: null,
      concepto: 0,
      periodo: moment().format('YYYY-MM-D'),
      fecha_gracia: moment().format('YYYY-MM-D'),
      fecha_vencimiento: moment().format('YYYY-MM-D')
    },
    {
      monto: 0,
      cantidad:0,
      detalle: '',
      destinatario: null,
      concepto: 0,
      periodo: moment().format('YYYY-MM-D'),
      fecha_gracia: moment().format('YYYY-MM-D'),
      fecha_vencimiento: moment().format('YYYY-MM-D')
    },
    {
      monto: 0,
      cantidad:0,
      detalle: '',
      destinatario: null,
      concepto: 0,
      periodo: moment().format('YYYY-MM-D'),
      fecha_gracia: moment().format('YYYY-MM-D'),
      fecha_vencimiento: moment().format('YYYY-MM-D')
    }
  ]
};

const Preconceptos = ({ onClose }) => {
  const [state, setState] = useState(initialState);
  const [csvError, setCSVError] = useState();
  const [csvErrorLine, setCSVErrorLine] = useState();
  const [dominios, loadingDominios] = useDominios();
  const [ingresos, loadingIngresos] = useIngresos();
  const [preconceptos, preconceptosLoading] = usePreconceptos();
  const [newPreconceptos, setNewPreconceptos] = useState([]);
  const [selectedRows, setSelectedRows] = useState([]);
  const dispatch = useDispatch();
  const clients = useClientList();

  const handleSubmit = (event) => {
    event.preventDefault();

    const mappedNewPreconceptos = newPreconceptos.map((x) => {
      let destinatario = "";
      if (x.destinatario.charAt(0) === "#") {
        const cleanDominio = x.destinatario.substring(1);
        destinatario = get(dominios.find((val) => val.full_name.toString().toLowerCase() === cleanDominio.toLowerCase()), "id", "");
      } else {
        destinatario = get(clients.find((val) => val.full_name.toLowerCase() === x.destinatario.toLowerCase()), "id", "");
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
    setState((oldState) => ({
      ...oldState,
      fileDropzone: {
        ...oldState.fileDropzone,
        open: !oldState.fileDropzone.open
      }
    }))
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
    setCSVError(null);
    setCSVErrorLine(null);

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

      // Preconceptos CSV validations
      let isWrong = false;
      let error = null;
      let errorRowLine;

      // All fields are present and of a valid type (Running with YUP validations)
      (await Promise.all(csvArr.map((row) => csvValidations.validate(row).catch((err) => err))))
        .find((val, index) => {
          if (val && val.errors && val.errors.length && val.message) {
            isWrong = true;
            error = val.message;
            errorRowLine = index + 1;
            return true;
          }

          return false;
        });

      if (isWrong) {
        setCSVError(error);
        setCSVErrorLine(errorRowLine);
        return;
      }

      // All relational fields (e.g destinatario, expensa) match correctly and their ids exists
      csvArr.forEach((row, index) => {
        const { destinatario, concepto } = row;

        // The inserted 'concepto' exists
        const matchedConcepto = ingresos.some((val) => val.nombre.toLowerCase() === concepto.toLowerCase());
        if (!matchedConcepto) {
          error = `Concepto "${concepto}" no encontrado`;
          isWrong = true;
          errorRowLine = index + 1;
          return;
        }
        if (destinatario.charAt(0) === "#") {
          const cleanDominio = destinatario.substring(1);
          const matchedDominio = dominios.some((val) => val.full_name.toString().toLowerCase() === cleanDominio.toLowerCase());
          if (!matchedDominio) {
            error = `Dominio "${destinatario}" no encontrado`;
            isWrong = true;
            errorRowLine = index + 1;
            return;
  
          }
        } else {
          const matchedClient = clients.some((val) => val.full_name.toLowerCase() === destinatario.toLowerCase());
          if (!matchedClient) {
            error = `Cliente "${destinatario}" no encontrado`;
            isWrong = true;
            errorRowLine = index + 1;
            return;

        }


        }
      });

      if (isWrong) {
        setCSVError(error);
        setCSVErrorLine(errorRowLine);
        return;
      }

      // Success! >)

      setNewPreconceptos(csvArr);
    };
  }

  const { loading, result, fileDropzone } = state;

  if (!loading && result) {
    return (
      <div className='loading-modal'>
        <Response
          type={result}
          message={
            // Change this messages depending on the backend error
            result === 'success'
              ? 'Cargado con exito'
              : 'Hubo un error. Por favor intente mas tarde'
          }
        />
      </div>
    )
  }

  if (loading || preconceptosLoading || loadingDominios || loadingIngresos) {
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
                let destinatario = get(clients.find((x) => x.id === row.destinatario), 'full_name', '');
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

        {csvError && (
          <Alert color="danger" style={{ color: 'white', margin: '0 3em' }}>
            {csvError} {csvErrorLine && `(Linea ${csvErrorLine})`}
          </Alert>
        )}

        {fileDropzone.open && (
          <div className="ImportFileDropzone__container">
            <ImportFileDropzone onDrop={handleDrop} />
          </div>
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
              importar
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