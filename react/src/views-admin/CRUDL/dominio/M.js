import React, { useState } from 'react';
import get from 'lodash/get';
import * as Yup from 'yup';
import csvtojson from 'csvtojson';
import { useDispatch } from 'react-redux';

// Components
import Spinner from '../../../components/spinner/spinner';
import { ImportFileDropzone } from '../../../components/dropzone/ImportFileDropzone';
import { useTitulos } from "../../../utility/hooks/dispatchers";
import { useClientes } from "../../../utility/hooks/dispatchers"

// Styles
import { Table, Alert } from 'reactstrap';
import { dominiosActions } from '../../../redux/actions/dominios';

const csvValidations = Yup.object({
  numero: Yup
    .number('Numero debe ser un numero valido')
    .positive()
    .required('Numero es requerido'),
  propietario: Yup
    .string('Propietario debe ser un socio valido'),
  inquilino: Yup
    .string('Inquilino debe ser un socio valido'),
  "superficie total": Yup
    .number('Superficie total debe ser un numero valido')
    .transform((value, originalValue) => originalValue.trim() === "" ? null: value)
    .nullable(),
  "superficie cubierta": Yup
    .number('Superficie cubierta debe ser un numero valido')
    .transform((value, originalValue) => originalValue.trim() === "" ? null: value)
    .nullable(),
  provincia: Yup
    .string("Provincia debe ser un texto valida"),
  localidad: Yup
    .string("Localidad debe ser un texto valido"),
  calle: Yup
    .string("Calle debe ser un texto valido"),
  "numero calle": Yup
    .number('Numero de calle debe ser un numero valido')
    .transform((value, originalValue) => originalValue.trim() === "" ? null: value)
    .nullable(),
  piso: Yup
    .string("Piso debe ser un texto valido"),
  manzana: Yup
    .string("Manzana debe ser un texto valido"),
  oficina: Yup
    .string("Oficina debe ser un texto valido"),
  sector: Yup
    .string("Sector debe ser un texto valido"),
  torre: Yup
    .string("Torre debe ser un texto valido"),
  parcela: Yup
    .string("Parcela debe ser un texto valido"),
  catastro: Yup
    .string("Catastro debe ser un texto valido"),
  titulo: Yup
    .string('Titulo debe ser un texto valido')
    .required('Titulo es requerido'),
});

const tableHeaders = [
    'Numero', 'Propietario', 'Inquilino', 'Superficie Total', 'Superficie Cubierta', 
    'Provincia', 'Localidad', 'Calle', 'Numero Calle', 'Piso',
    'Manzana', 'Oficina', 'Sector', 'Torre', 'Parcela', 'Catastro', 'Titulo'
];


const M = ({ onClose }) => {
  const [csvError, setCSVError] = useState();
  const [csvErrorLine, setCSVErrorLine] = useState();
  const [newDominios, setNewDominios] = useState([]);
  const [titulos, loadingTitulos] = useTitulos(true);
  const [clientes, loadingClientes] = useClientes();
  const dispatch = useDispatch();

  const handleSubmit = (event) => {
    event.preventDefault();

    const mappedNewClientes = newDominios.map((x) => ({
        ...x,
        numero_calle: x['numero calle'],
        propietario: get(clientes.find((val) => val.full_name.toLowerCase() === x.propietario.toLowerCase()), "id", ""),
        inquilino: get(clientes.find((val) => val.full_name.toLowerCase() === x.inquilino.toLowerCase()), "id", ""),
        titulo: get(titulos.find((val) => val.full_name.toLowerCase() === x.titulo.toLowerCase()), "id", ""),
      }));

    dispatch(dominiosActions.send_bulk(mappedNewClientes))
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
        const { titulo, propietario, inquilino } = row;
        const matchedPropietario = clientes.some((val) => val.full_name.toLowerCase() === propietario.toLowerCase());
        if (!matchedPropietario) {
          error = `Propietario "${propietario}" no encontrado`;
          isWrong = true;
          errorRowLine = index + 1;
          return;
        }

        const matchedInquilino = clientes.some((val) => val.full_name.toLowerCase() === inquilino.toLowerCase());
        if (!matchedInquilino) {
          error = `Inquilino "${inquilino}" no encontrado`;
          isWrong = true;
          errorRowLine = index + 1;
          return;
        }

        // The inserted 'titulo' exists
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

      setNewDominios(csvArr);
    };
  }


  if (loadingTitulos || loadingClientes) {
    return (
      <div className='loading-modal'>
        <Spinner />
      </div>
    );
  }

  return (
    <>
      <form onSubmit={handleSubmit}>

        {(newDominios.length) > 0 && (
          <Table responsive>
            <thead>
              <tr>
                {tableHeaders.map((header) => (
                  <th key={header}>{header}</th>
                ))}
              </tr>
            </thead>

            <tbody>
              {[...newDominios].map((row, index) => {


                return (
                  <tr className={row.id ? "" : "warning"} key={index}>
                    <td>{row.numero}</td>
                    <td>{row.propietario}</td>
                    <td>{row.inquilino}</td>
                    <td>{row["superficie total"]}</td>
                    <td>{row["superficie cubierta"]}</td>
                    <td>{row.provincia}</td>
                    <td>{row.localidad}</td>
                    <td>{row.calle}</td>
                    <td>{row["numero calle"]}</td>
                    <td>{row.piso}</td>
                    <td>{row.manzana}</td>
                    <td>{row.oficina}</td>
                    <td>{row.sector}</td>
                    <td>{row.torre}</td>
                    <td>{row.parcela}</td>
                    <td>{row.catastro}</td>
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
              disabled={newDominios.length === 0}
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