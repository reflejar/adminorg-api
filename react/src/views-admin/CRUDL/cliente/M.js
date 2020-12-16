import React, { useState } from 'react';
import moment from 'moment';
import get from 'lodash/get';
import * as Yup from 'yup';
import csvtojson from 'csvtojson';
import { CSVLink } from "react-csv";
import { useDispatch } from 'react-redux';

// Components
import Spinner from '../../../components/spinner/spinner';
import { ImportFileDropzone } from '../../../components/dropzone/ImportFileDropzone';
import { useTitulos } from "../../../utility/hooks/dispatchers";
import { tipo_documentos } from '../../../utility/options/documentos';

// Styles
import { Table } from 'reactstrap';
import { clientesActions } from '../../../redux/actions/clientes';

const csvValidations = Yup.object({
  nombre: Yup
    .string('Nombre debe ser un texto valido')
    .required('Nombre es requerido'),
  apellido: Yup
    .string('Apellido debe ser un texto valido')
    .required('Apellido es requerido'),    
  "razon social": Yup
    .string('Razon Social debe ser un texto valido'),
  "tipo documento": Yup
    .string('Tipo Documento debe ser un texto valido')
    .required('Tipo Documento es requerido'),
  "numero documento": Yup
    .number('Numero Documento debe ser un numero valido')
    .positive("Numero de documento debe ser un numero valido")
    .required('Numero Documento es requerido'),
  "fecha nacimiento": Yup
    .string('Fecha de nacimiento debe ser una fecha valida'),
  mail: Yup
    .string('Email debe ser una cuenta valida')
    .email("Email invalido")
    .required('Email es requerido'),    
  telefono: Yup
    .number('Telefono debe ser un numero valido')
    .transform((value, originalValue) => originalValue.trim() === "" ? null: value)
    .nullable(),
  provincia: Yup
    .string('Provincia debe ser un texto valido')
    .required('Provincia es requerido'),    
  localidad: Yup
    .string('Localidad debe ser un texto valido'),
  calle: Yup
    .string('Calle debe ser un texto valido'),
  numero: Yup
    .number('Numero debe ser un numero valido')
    .nullable(),
  titulo: Yup
    .string('Titulo debe ser un texto valido')
    .required('Titulo es requerido'),
});

const tableHeaders = [
    'Nombre', 'Apellido', 'Razon Social', 'Tipo Documento', 
    'Numero Documento', 'Fecha Nacimiento', 'Mail', 'Telefono', 
    'Provincia', 'Localidad', 'Calle', 'Numero', 'Titulo'
];

const M = ({ onClose }) => {
  const [csvError, setCSVError] = useState([]);
  const [newClientes, setNewClientes] = useState([]);
  const [titulos, loadingTitulos] = useTitulos(true);
  const dispatch = useDispatch();

  const handleSubmit = (event) => {
    event.preventDefault();

    const mappedNewClientes = newClientes.map((x) => ({
        ...x,
        razon_social: x['razon social'],
        tipo_documento: x['tipo documento'],
        numero_documento: x['numero documento'],
        fecha_nacimiento: moment(x['fecha nacimiento']).format('YYYY-MM-DD') || null,
        domicilio_provincia: x['provincia'],
        domicilio_localidad: x['localidad'],
        domicilio_calle: x['calle'],
        domicilio_numero: x['numero'],
        titulo: get(titulos.find((val) => val.full_name.toLowerCase() === x.titulo.toLowerCase()), "id", ""),
      }));

    dispatch(clientesActions.send_bulk(mappedNewClientes))
      .then(onClose);
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
              if (loweredKey === 'numero' || loweredKey === "numero documento") {
                value = Number(value);
              }

              return { ...acc, [loweredKey]: value };
            }, {});

          })
        });

      let errors = [];

      (await Promise.all(csvArr.map((row) => csvValidations.validate(row).catch((err) => err))))
        .find((val, index) => {
          if (val && val.errors && val.errors.length && val.message) {
            const error = val.message;
            const errorRowLine = index + 1;
            const message = `Linea ${errorRowLine}: ` + error;
            errors.push(message)
          }
        });
      
      // All relational fields (e.g destinatario, expensa) match correctly and their ids exists
      csvArr.forEach((row, index) => {
        const { titulo } = row;
        // The inserted 'titulo' exists
        const matchedTitulo = titulos.some((val) => val.nombre.toLowerCase() === titulo.toLowerCase());
        if (!matchedTitulo) {
          const error = `Titulo "${titulo}" no encontrado`;
          const errorRowLine = index + 1;
          const message = `Linea ${errorRowLine}: ` + error;    
          errors.push(message)
        }
        const matchedTipoDoc = tipo_documentos.some((val) => val.toLowerCase() === row["tipo documento"].toLowerCase());
        if (!matchedTipoDoc) {
          const error = `Tipo de Documento "${row["tipo documento"]}" no encontrado`;
          const errorRowLine = index + 1;
          const message = `Linea ${errorRowLine}: ` + error;    
          errors.push(message)
        }
      });
      
      if (errors.length > 0) {
        setCSVError([...errors]);
        return;
      } else {
        setNewClientes(csvArr);
      }
    };
  }

  if (loadingTitulos) {
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
          <Table responsive>
            <thead>
              <tr>
                {tableHeaders.map((header) => (
                  <th key={header}>{header}</th>
                ))}
              </tr>
            </thead>

            <tbody>
              {[...newClientes].map((row, index) => {

                return (
                  <tr className={row.id ? "" : "warning"} key={index}>
                    <td>{row.nombre}</td>
                    <td>{row.apellido}</td>
                    <td>{row['razon social']}</td>
                    <td>{row['tipo documento']}</td>
                    <td>{row['numero documento']}</td>
                    <td>{row['fecha nacimiento']}</td>
                    <td>{row.email}</td>
                    <td>{row.telefono}</td>
                    <td>{row.provincia}</td>
                    <td>{row.localidad}</td>
                    <td>{row.calle}</td>
                    <td>{row.numero}</td>
                    <td>{row.titulo}</td>
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

          <div className="ImportFileDropzone__container">
            <ImportFileDropzone onDrop={handleDrop} />
          </div>
          <p>
            Necesitas un archivo modelo? podes hacer <CSVLink filename={"importador-clientes.csv"} data={[tableHeaders]}>click aqui</CSVLink>
          </p>

        <div className='row'>
          <div className='col-12 text-right'>
            <button type='button' className='btn btn-secondary mr-2' onClick={onClose}>
              Cancelar
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