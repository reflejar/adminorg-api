import React, { useState } from 'react';
import get from 'lodash/get';
import * as Yup from 'yup';
import csvtojson from 'csvtojson';
import { CSVLink } from "react-csv";
import { useDispatch } from 'react-redux';

// Components
import Spinner from '../../../components/spinner/spinner';
import { ImportFileDropzone } from '../../../components/dropzone/ImportFileDropzone';
import { useTitulos } from "../../../utility/hooks/dispatchers";
import { gastos } from '../../../utility/options/taxones';

// Styles
import { Table } from 'reactstrap';
import { gastosActions } from '../../../redux/actions/gastos';

const csvValidations = Yup.object({
  nombre: Yup
    .string('Nombre debe ser un texto valido')
    .required('Nombre es requerido'),
  tipo: Yup
    .string('Tipo de gasto debe ser un texto valido')
    .required('Tipo es requerido'),
  titulo: Yup
    .string('Titulo debe ser un texto valido')
    .required('Titulo es requerido'),
});

const tableHeaders = ['Nombre', 'Tipo', 'Titulo'];

const M = ({ onClose }) => {
  const [csvError, setCSVError] = useState([]);
  const [newGastos, setNewGastos] = useState([]);
  const [titulos, loadingTitulos] = useTitulos(true);

  const dispatch = useDispatch();

  const handleSubmit = (event) => {
    event.preventDefault();

    const mappedNewGastos = newGastos.map((x) => ({
        ...x,
        taxon: get(gastos.find((val) => val.nombre.toLowerCase() === x.tipo.toLowerCase()), "id", ""),
        titulo: get(titulos.find((val) => val.full_name.toLowerCase() === x.titulo.toLowerCase()), "id", ""),
      }));

    dispatch(gastosActions.send_bulk(mappedNewGastos))
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
            errors.push(message)
          }
        });

      // All relational fields (e.g destinatario, expensa) match correctly and their ids exists
      csvArr.forEach((row, index) => {
        const { tipo } = row;
        const matchedTipo = gastos.some((val) => val.nombre.toLowerCase() === tipo.toLowerCase());
        if (!matchedTipo) {
          const error = `Tipo "${tipo}" no es posible`;
          const errorRowLine = index + 1;
          const message = `Linea ${errorRowLine}: ` + error;    
          errors.push(message)
        }   
      });

      if (errors.length > 0) {
        setCSVError([...errors]);
        return;
      } else {
        setNewGastos(csvArr);
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

        {(newGastos.length) > 0 && (
          <Table responsive>
            <thead>
              <tr>
                {tableHeaders.map((header) => (
                  <th key={header}>{header}</th>
                ))}
              </tr>
            </thead>

            <tbody>
              {[...newGastos].map((row, index) => {

                return (
                  <tr className={row.id ? "" : "warning"} key={index}>
                    <td>{row.nombre}</td>
                    <td>{row.tipo}</td>
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
            Necesitas un archivo modelo? podes hacer <CSVLink filename={"importador-gastos.csv"} data={[tableHeaders]}>click aqui</CSVLink>
          </p>   

        <div className='row'>
          <div className='col-12 text-right'>
            <button type='button' className='btn btn-secondary mr-2' onClick={onClose}>
              Cancelar
            </button>

            <button
              type='submit'
              className='btn btn-primary'
              disabled={newGastos.length === 0}
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