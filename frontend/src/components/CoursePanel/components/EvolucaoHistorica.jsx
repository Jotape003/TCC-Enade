import React, { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const EvolucaoHistorica = ({ historicoData }) => {
  const [metric, setMetric] = useState('geral');
  
  const [comparisonState, setComparisonState] = useState({
    ufc: false,
    brasil: false,
    regiao: false,
    ceara: false,
  });

  const comparisonOptions = {
    ufc: { label: "UFC (Área)", color: "#E70000" },
    brasil: { label: "Brasil", color: "#FF7B00" },
    regiao: { label: "Região", color: "#0A5C36" },
    ceara: { label: "Ceará", color: "#FFE745" }
  };

  if (!historicoData || historicoData.length === 0) {
    return <p className="text-center text-gray-500 py-10">Histórico não disponível para este curso.</p>;
  }

  const handleComparisonChange = (event) => {
    const { name, checked } = event.target;
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

  const currentConfig = config[metric];

  return (
    <div className="space-y-6">
      
      <div className="flex justify-center bg-gray-50 p-4 space-x-4 rounded-lg">
        {['geral', 'fg', 'ce'].map((m) => (
          <button
            key={m}
            onClick={() => setMetric(m)}
            className={`px-4 py-2 rounded-md text-lg font-medium transition-all cursor-pointer ${
              metric === m
                ? 'bg-white text-indigo-600 shadow-sm ring-1 ring-gray-200'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            {m === 'geral' ? 'Nota Geral' : m.toUpperCase()}
          </button>
        ))}
      </div>

      <div className="flex justify-center items-center space-x-7">
        <h4 className="text-lg font-semibold text-gray-700">Comparar com:</h4>
        <div className="flex space-x-4">
          {Object.entries(comparisonOptions).map(([key, { label }]) => (
            <label key={key} className="flex items-center space-x-2 cursor-pointer">
              <input
                type="checkbox"
                name={key}
                checked={comparisonState[key]}
                onChange={handleComparisonChange}
                className="form-checkbox h-5 w-5 text-indigo-600 rounded cursor-pointer"
              />
              <span className="text-gray-700 text-2sm font-medium">{label}</span>
            </label>
          ))}
        </div>
      </div>

      <div style={{ width: '100%', height: 400 }} className="bg-white rounded-lg mb-10 flex flex-col justify-center items-center">
        <h4 className="text-lg font-semibold text-gray-700 p-4 text-center">{currentConfig.title}</h4>
        <ResponsiveContainer>
          <LineChart data={historicoData} margin={{ top: 5, right: 30, left: -5, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="ano" />
            <YAxis domain={[0, 100]} />
            <Tooltip />
            <Legend />
            
            <Line 
              type="monotone" 
              dataKey={currentConfig.curso}
              name="Curso" 
              stroke="#051650" 
              strokeWidth={3} 
              activeDot={{ r: 8 }}
            />
            
            {Object.entries(comparisonOptions).map(([key, { label, color }]) => {
              if (!comparisonState[key]) return null;

              const dataKey = currentConfig[key]; 

              return (
                <Line
                  key={key}
                  type="monotone"
                  dataKey={dataKey}
                  name={label}
                  stroke={color}
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