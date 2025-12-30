import { useState, useEffect } from 'react';
import { 
  getVisaoGeralData, 
  getDesempenhoTopicoData, 
  getEvolucaoHistorica,
  getPerfilConsolidado 
} from '../services/enadeService';

export const useEnadeData = (campus, course) => {
  const [data, setData] = useState({
    visaoGeral: null,
    desempenhoTopico: null,
    evolucaoHistorica: null,
    perfilConsolidado: null
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!campus || !course) {
      setData({ visaoGeral: null, desempenhoTopico: null, evolucaoHistorica: null, perfilConsolidado: null });
      return;
    }

    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        const results = await Promise.allSettled([
          getVisaoGeralData(campus, course),
          getDesempenhoTopicoData(campus, course),
          getEvolucaoHistorica(campus, course),
          getPerfilConsolidado(campus, course)
        ]);

        const getValue = (res) => (res.status === 'fulfilled' ? res.value : null);

        setData({
          visaoGeral: getValue(results[0]),
          desempenhoTopico: getValue(results[1]),
          evolucaoHistorica: getValue(results[2]),
          perfilConsolidado: getValue(results[3]),
        });

      } catch (err) {
        setError("Erro crítico ao carregar dados.");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [campus, course]);

  return { ...data, loading, error };
};