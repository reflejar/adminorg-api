import { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import moment from 'moment';
import get from 'lodash/get';

import { clientesActions } from '../../redux/actions/clientes';
import { dominiosActions } from '../../redux/actions/dominios';
import { proveedoresActions } from '../../redux/actions/proveedores';
import { puntosActions } from '../../redux/actions/puntos';
import { deudasActions } from '../../redux/actions/deudas';
import { saldosActions } from '../../redux/actions/saldos';
import { cuentasActions } from '../../redux/actions/cuentas';
import { titulosActions } from '../../redux/actions/utils/titulos';
import { preconceptosActions } from '../../redux/actions/preconceptos';
import { ingresosActions } from '../../redux/actions/ingresos';
import { gastosActions } from '../../redux/actions/gastos';
import { plataformaActions } from '../../redux/actions/plataforma';
import { cajasActions } from '../../redux/actions/cajas';
import { retencionesActions } from '../../redux/actions/retenciones';

// Parametros
export const useClientes = () => {
  const [loading, setLoading] = useState(false);
  const clientes = useSelector((state) => get(state, 'clientes.list', []));
  const [listado, setListado] = useState(undefined);
  const dispatch = useDispatch();
  
  useEffect(() => {
    async function fetchCli() {
      setLoading(true);
      await dispatch(clientesActions.get_all())
        .finally(() => setLoading(false));
    }
    if (!listado) {
      fetchCli();
      setListado([...clientes])
    }
  }, [setLoading, dispatch, listado, setListado, clientes]);

  return [clientes, loading];
};

export const useDominios = () => {
  const [loading, setLoading] = useState(false);
  const dominios = useSelector((state) => get(state, 'dominios.list', []));
  const [listado, setListado] = useState(undefined);
  const dispatch = useDispatch();

  useEffect(() => {
    async function fetchDom() {
      setLoading(true)
      await dispatch(dominiosActions.get_all())
        .finally(() => setLoading(false));
    }
    if (!listado) {
      fetchDom();
      setListado([...dominios])
    }
  }, [setLoading, dispatch, listado, setListado, dominios]);


  return [dominios, loading];
};

export const useProveedores = () => {
  const [loading, setLoading] = useState(false);
  const proveedores = useSelector((state) => get(state, 'proveedores.list', []));
  const [listado, setListado] = useState(undefined);
  const dispatch = useDispatch();

  useEffect(() => {
    async function fetchProv() {
      setLoading(true)
      await dispatch(proveedoresActions.get_all())
        .finally(() => setLoading(false));
    }
    if (!listado) {
      fetchProv();
      setListado([...proveedores])
    }
  }, [setLoading, dispatch, listado, setListado, proveedores]);


  return [proveedores, loading];
};

export const usePuntosDeVenta = () => {
  const [loading, setLoading] = useState(false);
  const puntos = useSelector((state) => get(state, 'puntos.list.results', []));
  const [listado, setListado] = useState(undefined);
  const dispatch = useDispatch();

  useEffect(() => {
    async function fetchPtos() {
      setLoading(true);
      await dispatch(puntosActions.get_all())
        .finally(() => setLoading(false));
    }
    if (!listado) {
      fetchPtos();
      setListado([...puntos])
    }
  }, [setLoading, dispatch, listado, setListado, puntos]);

  return [puntos, loading];
};

export const useTitulos = () => {
  const [loading, setLoading] = useState(false);
  const titulos = useSelector((state) => get(state, 'utils.titulos', []));
  const [listado, setListado] = useState(undefined);
  const dispatch = useDispatch();

  useEffect(() => {
    async function fetchTit() {
      setLoading(true);
      await dispatch(titulosActions.get())
        .finally(() => setLoading(false));
    }
    if (!listado) {
      fetchTit();
      setListado([...titulos])
    }
  }, [setLoading, dispatch, listado, setListado, titulos]);

  return [titulos, loading];
};

export const useIngresos = () => {
  const [loading, setLoading] = useState(false);
  const ingresos = useSelector((state) => get(state, 'ingresos.list', []));
  const [listado, setListado] = useState(undefined);
  const dispatch = useDispatch();

  useEffect(() => {
    async function fetchIng() {
      setLoading(true);
      await dispatch(ingresosActions.get_all())
        .finally(() => setLoading(false));
    }
    if (!listado) {
      fetchIng();
      setListado([...ingresos])
    }
  }, [setLoading, dispatch, listado, setListado, ingresos]);

  return [ingresos, loading];
};

export const useGastos = () => {
  const [loading, setLoading] = useState(false);
  const gastos = useSelector((state) => get(state, 'gastos.list', []));
  const [listado, setListado] = useState(undefined);
  const dispatch = useDispatch();

  useEffect(() => {
    async function fetchGas() {
      setLoading(true);
      await dispatch(gastosActions.get_all())
        .finally(() => setLoading(false));
    }
    if (!listado) {
      fetchGas();
      setListado([...gastos])
    }
  }, [setLoading, dispatch, listado, setListado, gastos]);

  return [gastos, loading];
};

export const usePlataformas = () => {
  const [loading, setLoading] = useState(false);
  const plataforma = useSelector((state) => get(state, 'plataforma.list', []));
  const [listado, setListado] = useState(undefined);
  const dispatch = useDispatch();

  useEffect(() => {
    async function fetchPlat() {
      setLoading(true);
      await dispatch(plataformaActions.get_all())
        .finally(() => setLoading(false));
    }
    if (!listado) {
      fetchPlat();
      setListado([...plataforma])
    }
  }, [setLoading, dispatch, listado, setListado, plataforma]);

  return [plataforma, loading];
};

export const useCajas = () => {
  const [loading, setLoading] = useState(false);
  const cajas = useSelector((state) => get(state, 'cajas.list', []));
  const [listado, setListado] = useState(undefined);
  const dispatch = useDispatch();

  useEffect(() => {
    async function fetchCaj() {
      setLoading(true);
      await dispatch(cajasActions.get_all())
        .finally(() => setLoading(false));
    }
    if (!listado) {
      fetchCaj();
      setListado([...cajas])
    }
  }, [setLoading, dispatch, listado, setListado, cajas]);

  return [cajas, loading];
};

export const useRetenciones = () => {
  const [loading, setLoading] = useState(false);
  const retenciones = useSelector((state) => get(state, 'retenciones.list', []));
  const [listado, setListado] = useState(undefined);
  const dispatch = useDispatch();

  useEffect(() => {
    async function fetchRet() {
      setLoading(true);
      await dispatch(retencionesActions.get_all())
        .finally(() => setLoading(false));
    }
    if (!listado) {
      fetchRet();
      setListado([...retenciones])
    }
  }, [setLoading, dispatch, listado, setListado, retenciones]);

  return [retenciones, loading];
};

// Otros
export const useEstadoCuenta = (selected) => {
  const [loading, setLoading] = useState(false);

  const { cuentas } = useSelector((state) => ({
    cuentas: get(state, 'cuentas.list', [])
  }));

  const dispatch = useDispatch();

  useEffect(() => {
    if (selected) {
      setLoading(true);

      dispatch(cuentasActions.get({ destinatario: selected.id, fecha: moment().format('YYYY-MM-DD') }))
        .finally(() => setLoading(false));
    }
  }, [selected, dispatch]);

  return [cuentas, loading];
};

export const useSaldos = (capture, selected, date) => {
  const [loading, setLoading] = useState(false);
  const [saldos, setSaldos] = useState([]);

  const { saldosRedux } = useSelector((state) => ({
    saldosRedux: get(state, 'saldos.list', []) 
  }));
  
  const dispatch = useDispatch();
  useEffect(() => {
    if (selected) {
      setLoading(true);
  
      dispatch(saldosActions.get({ destinatario: selected.id, fecha: moment(date).format('YYYY-MM-DD'), capture }))
        .then((response) => setSaldos(response))
        .finally(() => setLoading(false));
    }
  }, [selected, dispatch, date, capture, setSaldos]);

  if (capture) {
    return [saldosRedux, loading];
  }
  return [saldos, loading];

};

export const useDeudas = (capture, selected, date, condonacion=false) => {
  const [loading, setLoading] = useState(false);
  const [deudas, setDeudas] = useState([]);

  const { deudasRedux } = useSelector((state) => ({
    deudasRedux: get(state, 'deudas.list', [])
  }));

  
  const dispatch = useDispatch();
  useEffect(() => {
    if (selected) {
      setLoading(true);
  
      dispatch(deudasActions.get({ destinatario: selected.id, fecha: moment(date).format('YYYY-MM-DD'), condonacion, capture }))
        .then((response) => setDeudas(response))
        .finally(() => setLoading(false));
    }
  }, [selected, dispatch, date, condonacion, capture, setDeudas]);

  if (capture) {
    return [deudasRedux, loading];
  }
  return [deudas, loading];
};

export const usePreconceptos = () => {
  const [loading, setLoading] = useState(false);
  const dispatch = useDispatch();

  const { preconceptos } = useSelector((state) => ({
    preconceptos: get(state, 'preconceptos.list.items', []),
  }));

  useEffect(() => {
    (async () => {
      setLoading(true);

      dispatch(preconceptosActions.get_all())
        .finally(() => setLoading(false));

    })()
  }, [dispatch]);

  return [preconceptos, loading];
};

export const useDisponibilidades = (date) => {
  const [loading, setLoading] = useState(false);

  const [disponibilidades, setDisponibilidades] = useState([]);
  
  const dispatch = useDispatch();

  useEffect(() => {
    async function fetchDispo() {
      setLoading(true);
  
      const data = await dispatch(saldosActions.get({ destinatario: "caja", fecha: moment(date).format('YYYY-MM-DD') }));
      setDisponibilidades(data);
      setLoading(false);
    }
    fetchDispo();
  }, [dispatch, date]);

  return [disponibilidades, loading];

};