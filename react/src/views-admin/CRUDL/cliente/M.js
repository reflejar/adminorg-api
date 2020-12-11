import React, { useState } from 'react';
import moment from 'moment';
import get from 'lodash/get';
import * as Yup from 'yup';
import csvtojson from 'csvtojson';
import { useDispatch } from 'react-redux';

// Components
import Spinner from '../../../components/spinner/spinner';
import { ImportFileDropzone } from '../../../components/dropzone/ImportFileDropzone';
import { useTitulos } from "../../../utility/hooks/dispatchers";

// Styles
import { Table, Alert } from 'reactstrap';
import Response from '../../../components/responses/responses';
import { clientesActions } from '../../../redux/actions/clientes';

const csvValidations = Yup.object({
  nombre: Yup
    .string('Nombre debe ser un texto valido')
    .test('len', 'Nombre debe ser valido', val => val.length > 0)
    .required('Nombre es requerido'),
  apellido: Yup
    .string('Apellido debe ser un texto valido')
    .test('len', 'Apellido debe ser valido', val => val.length > 0)
    .required('Apellido es requerido'),    
  razon_social: Yup
    .string('Razon Social debe ser un texto valido')
    .test('len', 'Razon Social debe ser valido', val => val.length > 0),
  tipo_documento: Yup
    .string('Tipo Documento debe ser un texto valido')
    .test('len', 'Tipo Documento debe ser valido', val => val.length > 0)
    .required('Tipo Documento es requerido'),
  numero_documento: Yup
    .number('Numero Documento debe ser un numero valido')
    .moreThan(-1, 'Numero Documento debe ser un numero mayor que cero (0)')
    .required('Numero Documento es requerido'),
  fecha_nacimiento: Yup
    .string('Fecha de nacimiento debe ser una fecha valida')
    .test('date', 'Fecha de nacimiento debe ser una fecha valida', val => moment(new Date(val)).isValid())
    .required('Fecha de nacimiento es requerido'),
  mail: Yup
    .string('Email debe ser una cuenta valida')
    .email("Email invalido")
    .required('Email es requerido'),    
  telefono: Yup
    .number('Telefono debe ser un numero valido')
    .moreThan(-1, 'Telefono debe ser un numero mayor que cero (0)'),
  provincia: Yup
    .string('Provincia debe ser un texto valido')
    .test('len', 'Provincia debe ser valido', val => val.length > 0)
    .required('Provincia es requerido'),    
  localidad: Yup
    .string('Localidad debe ser un texto valido')
    .test('len', 'Localidad debe ser valido', val => val.length > 0),
  calle: Yup
    .string('Calle debe ser un texto valido')
    .test('len', 'Calle debe ser valido', val => val.length > 0),
  numero: Yup
    .number('Numero debe ser un numero valido')
    .moreThan(-1, 'Numero debe ser un numero mayor que cero (0)'),
  titulo: Yup
    .string('Titulo debe ser un texto valido')
    .test('len', 'Titulo debe ser valido', val => val.length > 0)
    .required('Titulo es requerido'),        
});

const tableHeaders = [
    'Nombre', 'Apellido', 'Razon Social', 'Tipo de Doc', 
    'Numero de Doc', 'Fecha Nac', 'Mail', 'Telefono', 
    'Provincia', 'Localidad', 'Calle', 'Numero', 'Titulo'
];

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
      nombre: "",
      apellido: "",
      razon_social: "",
      tipo_documento: "",
      numero_documento: 0,
      fecha_nacimiento: moment().format('YYYY-MM-D'),
      mail: "",
      telefono: null,
      provincia: "",
      localidad: "",
      calle: "",
      numero: null,
      titulo: null
    },
  ]
};

const M = ({ onClose }) => {
  const [state, setState] = useState(initialState);
  const [csvError, setCSVError] = useState();
  const [csvErrorLine, setCSVErrorLine] = useState();
  const [newClientes, setNewClientes] = useState([]);
  const [selectedRows, setSelectedRows] = useState([]);
  const [titulos, loadingTitulos] = useTitulos(true);
  const dispatch = useDispatch();

  const handleSubmit = (event) => {
    event.preventDefault();

    const mappedNewClientes = newClientes.map((x) => ({
        ...x,
        titulo: get(titulos.find((val) => val.full_name.toLowerCase() === x.titulo.toLowerCase()), "id", ""),
      }));

    dispatch(clientesActions.post(mappedNewClientes))
      .then(onClose);
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
        const { titulo } = row;

        // The inserted 'concepto' exists
        const matchedTitulo = titulos.some((val) => val.nombre.toLowerCase() === titulo.toLowerCase());
        if (!matchedTitulo) {
          error = `Titulo "${titulo}" no encontrado`;
          isWrong = true;
          errorRowLine = index + 1;
          return;
        }
      });

      if (isWrong) {
        setCSVError(error);
        setCSVErrorLine(errorRowLine);
        return;
      }

      // Success! >)

      setNewClientes(csvArr);
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

  if (loading || loadingTitulos) {
    return (
      <div className='loading-modal'>
        <Spinner />
      </div>
    );
  }

  return (
    <>
      <form onSubmit={handleSubmit}>

        {(newClientes.length) > 0 && (
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
              {[...newClientes].map((row, index) => {

                const titulo = get(titulos.find((x) => x.id === row.titulo), 'nombre', '');

                return (
                  <tr className={row.id ? "" : "warning"} key={index}>
                    <td>{row.nombre}</td>
                    {/* <td>{concepto || row.concepto}</td>
                    <td>{row.periodo}</td>
                    <td>{row.detalle}</td>
                    <td>{row.fecha_vencimiento || row['fecha v']}</td>
                    <td>{row.fecha_gracia || row['fecha g']}</td>
                    <td>{row.cantidad}</td>
                    <td>{row.monto}</td> */}
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
              className='btn btn-warning mr-2'
              onClick={togglefileDropzone}
            >
              importar
            </button>

            <button
              type='submit'
              className='btn btn-primary'
              disabled={newClientes.length === 0}
            >
              Guardar
            </button>
          </div>
        </div>
      </form>
    </>
  );
}

export default M;