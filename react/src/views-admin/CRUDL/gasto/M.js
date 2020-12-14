import React, { useState } from 'react';
import get from 'lodash/get';
import * as Yup from 'yup';
import csvtojson from 'csvtojson';
import { useDispatch } from 'react-redux';

// Components
import Spinner from '../../../components/spinner/spinner';
import { ImportFileDropzone } from '../../../components/dropzone/ImportFileDropzone';
import { useTitulos } from "../../../utility/hooks/dispatchers";
import { gastos } from '../../../utility/options/taxones';
// Styles
import { Table, Alert } from 'reactstrap';
import { gastosActions } from '../../../redux/actions/gastos';

const csvValidations = Yup.object({
  nombre: Yup
    .string('Nombre debe ser un texto valido')
    .required('Nombre es requerido'),
  tipo: Yup
    .string('Tipo de gasto debe ser un texto valido')
    .required('Titulo es requerido'),
  titulo: Yup
    .string('Titulo debe ser un texto valido')
    .required('Titulo es requerido'),
});

const tableHeaders = ['Nombre', 'Tipo', 'Titulo'];

const M = ({ onClose }) => {
  const [csvError, setCSVError] = useState();
  const [csvErrorLine, setCSVErrorLine] = useState();
  const [newIngresos, setNewIngresos] = useState([]);
  const [titulos, loadingTitulos] = useTitulos(true);

  const dispatch = useDispatch();

  const handleSubmit = (event) => {
    event.preventDefault();

    const mappedNewIngresos = newIngresos.map((x) => ({
        ...x,
        taxon: get(gastos.find((val) => val.nombre.toLowerCase() === x.tipo.toLowerCase()), "id", ""),
        titulo: get(titulos.find((val) => val.full_name.toLowerCase() === x.titulo.toLowerCase()), "id", ""),
      }));

    dispatch(gastosActions.send_bulk(mappedNewIngresos))
      .then(onClose);
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
        const { tipo } = row;
        const matchedTipo = gastos.some((val) => val.nombre.toLowerCase() === tipo.toLowerCase());
        if (!matchedTipo) {
          error = `Tipo "${tipo}" no es posible`;
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

      setNewIngresos(csvArr);
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

        {(newIngresos.length) > 0 && (
          <Table responsive>
            <thead>
              <tr>
                {tableHeaders.map((header) => (
                  <th key={header}>{header}</th>
                ))}
              </tr>
            </thead>

            <tbody>
              {[...newIngresos].map((row, index) => {

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

        {csvError && (
          <Alert color="danger" style={{ color: 'white', margin: '0 3em' }}>
            {csvError} {csvErrorLine && `(Linea ${csvErrorLine})`}
          </Alert>
        )}

          <div className="ImportFileDropzone__container">
            <ImportFileDropzone onDrop={handleDrop} />
          </div>

        <div className='row'>
          <div className='col-12 text-right'>
            <button type='button' className='btn btn-secondary mr-2' onClick={onClose}>
              Cancelar
            </button>

            <button
              type='submit'
              className='btn btn-primary'
              disabled={newIngresos.length === 0}
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