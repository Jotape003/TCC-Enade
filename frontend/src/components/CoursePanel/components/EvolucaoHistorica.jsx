import React, { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import MetricTabs from './shared/MetricTabs';
import ComparisonSelector from './shared/ComparisonSelector';


const EvolucaoHistorica = ({ historicoData }) => {
  const [metric, setMetric] = useState('geral');
  
  const [comparisonState, setComparisonState] = useState({
    ufc: false,
    brasil: true,
    regiao: false,
    ceara: false,
  });

  // Configuração das Abas
  const tabOptions = [
    { value: 'geral', label: 'Nota Geral' },
    { value: 'fg', label: 'Formação Geral (FG)' },
    { value: 'ce', label: 'Comp. Específico (CE)' }
  ];

  // Mapeamento de Cores para o Gráfico (Consistente com o componente ComparisonSelector)
  const comparisonColors = {
    ufc: "#E70000",
    brasil: "#FF7B00",
    regiao: "#0A5C36",
    ceara: "#FFE745"
  };

  const handleComparisonChange = (name, checked) => {
    setComparisonState(prevState => ({
      ...prevState,
      [name]: checked,
    }));
  };

  const config = {
    geral: { 
      title: "Evolução da Nota Geral", 
      curso: "nota_geral", 
      ufc: "ufc_geral", 
      brasil: "nacional_geral",
      regiao: "regiao_geral",
      ceara: "uf_geral" 
    },
    fg: { 
      title: "Evolução da Formação Geral (FG)", 
      curso: "nota_fg", 
      ufc: "ufc_fg", 
      brasil: "nacional_fg",
      regiao: "regiao_fg",
      ceara: "uf_fg"
    },
    ce: { 
      title: "Evolução do Componente Específico (CE)", 
      curso: "nota_ce", 
      ufc: "ufc_ce", 
      brasil: "nacional_ce" ,
      regiao: "regiao_ce",
      ceara: "uf_ce"
    }
  };

  if (!historicoData || historicoData.length === 0) {
    return <p className="text-center text-gray-500 py-10">Histórico não disponível para este curso.</p>;
  }

  const currentConfig = config[metric];

  return (
    <div className="space-y-2">
      <MetricTabs
        activeTab={metric} 
        onChange={setMetric} 
        options={tabOptions} 
      />

      <ComparisonSelector 
        comparisonState={comparisonState} 
        onToggle={handleComparisonChange} 
      />

      <div style={{ width: '100%', height: 400 }} className="bg-white rounded-lg mb-10 flex flex-col justify-center items-center pt-4">
        <h4 className="text-lg font-semibold text-gray-700 mb-4 text-center">{currentConfig.title}</h4>
        <ResponsiveContainer>
          <LineChart data={historicoData} margin={{ top: 5, right: 30, left: -5, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="ano" />
            <YAxis domain={[0, 100]} />
            <Tooltip contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)' }} />
            <Legend />
            
            <Line 
              type="monotone" 
              dataKey={currentConfig.curso}
              name="Curso" 
              stroke="#051650" 
              strokeWidth={3} 
              activeDot={{ r: 8 }}
            />
            
            {Object.keys(comparisonColors).map((key) => {
              if (!comparisonState[key]) return null;

              const labels = {
                ufc: "UFC (Área)", brasil: "Brasil", regiao: "Região", ceara: "Ceará"
              };

              return (
                <Line
                  key={key}
                  type="monotone"
                  dataKey={currentConfig[key]}
                  name={labels[key]}
                  stroke={comparisonColors[key]}
                  strokeWidth={2}
                  dot={false}
                />
              );
            })}
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default EvolucaoHistorica;