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

export const useClientes = () => {
  const [loading, setLoading] = useState(false);
  const clientes = useSelector((state) => get(state, 'clientes.list', []));
  const dispatch = useDispatch();

  useEffect(() => {
    if (clientes.length === 0) {
      setLoading(true)
      dispatch(clientesActions.get_all())
        .finally(() => {
          setLoading(false);
        });
    }
  }, [clientes, dispatch, setLoading]);

  return [clientes, loading];
};

export const useDominios = () => {
  const [loading, setLoading] = useState(false);
  const dominios = useSelector((state) => get(state, 'dominios.list', []));
  const dispatch = useDispatch();

  useEffect(() => {
    if (dominios.length === 0) {
      setLoading(true)
      dispatch(dominiosActions.get_all())
        .finally(() => {
          setLoading(false);
        });
    }
  }, [dominios, dispatch, setLoading]);

  return [dominios, loading];
};

export const useProveedores = () => {
  const [loading, setLoading] = useState(false);
  const proveedores = useSelector((state) => get(state, 'proveedores.list', []));
  const dispatch = useDispatch();

  useEffect(() => {
    if (proveedores.length === 0) {
      setLoading(true)
      dispatch(proveedoresActions.get_all())
        .finally(() => {
          setLoading(false);
        });
    }
  }, [proveedores, dispatch, setLoading]);

  return [proveedores, loading];
};


export const usePuntosDeVenta = () => {
  const puntos = useSelector((state) => get(state, 'puntos.list.results', []));
  const dispatch = useDispatch();

  useEffect(() => {
    if (puntos.length === 0) {
      dispatch(puntosActions.get_all());
    }
  }, [puntos, dispatch]);

  return puntos;
};

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

export const useTitulos = () => {
  const [loading, setLoading] = useState(false);
  const titulos = useSelector((state) => get(state, 'utils.titulos', []));
  const dispatch = useDispatch();

  useEffect(() => {
    if (titulos && (!Array.isArray(titulos) || titulos.length === 0)) {
      setLoading(true);

      dispatch(titulosActions.get())
        .finally(() => setLoading(false));
    }
  }, [titulos, dispatch]);

  return [titulos, loading];
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

export const useIngresos = () => {
  const [loading, setLoading] = useState(false);
  const dispatch = useDispatch();
  const ingresos = useSelector((state) => get(state, 'ingresos.list', []));

  useEffect(() => {
    setLoading(true);

    dispatch(ingresosActions.get_all())
      .finally(() => setLoading(false));

  }, [dispatch]);

  return [ingresos, loading];
};

export const useGastos = () => {
  const [loading, setLoading] = useState(false);
  const dispatch = useDispatch();
  const gastos = useSelector((state) => get(state, 'gastos.list', []));

  useEffect(() => {
    setLoading(true);

    dispatch(gastosActions.get_all())
      .finally(() => setLoading(false));

  }, [dispatch]);

  return [gastos, loading];
};

export const usePlataformas = () => {
  const [loading, setLoading] = useState(false);
  const dispatch = useDispatch();
  const plataforma = useSelector((state) => get(state, 'plataforma.list', []));

  useEffect(() => {
    setLoading(true);

    dispatch(plataformaActions.get_all())
      .finally(() => setLoading(false));
  }, [dispatch]);

  return [plataforma, loading];
};

export const useCajas = () => {
  const [loading, setLoading] = useState(false);
  const dispatch = useDispatch();
  const cajas = useSelector((state) => get(state, 'cajas.list', []));

  useEffect(() => {
    setLoading(true);

    dispatch(cajasActions.get_all())
      .finally(() => setLoading(false));
  }, [dispatch]);

  return [cajas, loading];
};

export const useRetenciones = () => {
  const [loading, setLoading] = useState(false);
  const dispatch = useDispatch();
  const retenciones = useSelector((state) => get(state, 'retenciones.list', []));

  useEffect(() => {
    setLoading(true);

    dispatch(retencionesActions.get_all())
      .finally(() => setLoading(false));
  }, [dispatch]);

  return [retenciones, loading];
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