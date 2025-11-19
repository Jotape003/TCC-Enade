// src/components/CoursePanel/EvolucaoHistorica.js
import React, { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const EvolucaoHistorica = ({ historicoData }) => {
  const [metric, setMetric] = useState('geral');
  console.log(historicoData); 

  if (!historicoData || historicoData.length === 0) {
    return <p className="text-center text-gray-500 py-10">Histórico não disponível para este curso.</p>;
  }

  // Configuração dinâmica baseada na métrica escolhida
  const config = {
    geral: { 
      title: "Evolução da Nota Geral", 
      dataKeyCurso: "nota_geral", 
      dataKeyUfc: "ufc_geral", 
      dataKeyBr: "nacional_geral",
      datakeyRegiao: "regiao_geral",
      dataKeyUf: "uf_geral" 
    },
    fg: { 
      title: "Evolução da Formação Geral (FG)", 
      dataKeyCurso: "nota_fg", 
      dataKeyUfc: "ufc_fg", 
      dataKeyBr: "nacional_fg",
      datakeyRegiao: "regiao_fg",
      datakeyUf: "uf_fg"
    },
    ce: { 
      title: "Evolução do Componente Específico (CE)", 
      dataKeyCurso: "nota_ce", 
      dataKeyUfc: "ufc_ce", 
      dataKeyBr: "nacional_ce" ,
      datakeyRegiao: "regiao_ce",
      datakeyUf: "uf_ce"
    }
  };

  const currentConfig = config[metric];

  return (
    <div className="space-y-6">
      
      {/* Seletor de Métrica (Abas internas ou botões) */}
      <div className="flex justify-center space-x-4 bg-gray-50 p-2 rounded-lg">
        {['geral', 'fg', 'ce'].map((m) => (
          <button
            key={m}
            onClick={() => setMetric(m)}
            className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
              metric === m
                ? 'bg-white text-indigo-600 shadow-sm ring-1 ring-gray-200'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            {m === 'geral' ? 'Nota Geral' : m.toUpperCase()}
          </button>
        ))}
      </div>

      {/* Gráfico de Linha */}
      <div style={{ width: '100%', height: 400 }}>
        <h4 className="text-lg font-semibold text-gray-700 mb-4 text-center">{currentConfig.title}</h4>
        <ResponsiveContainer>
          <LineChart data={historicoData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid />
            <XAxis dataKey="ano" />
            <YAxis domain={[0, 100]} />
            <Tooltip />
            <Legend />
            
            {/* Linha do Curso */}
            <Line 
              type="monotone" 
              dataKey={currentConfig.dataKeyCurso} 
              name="Curso" 
              stroke="#051650" 
              strokeWidth={3} 
            />
            
            {/* Linha da UFC */}
            <Line 
              type="monotone" 
              dataKey={currentConfig.dataKeyUfc} 
              name="Média UFC (Área)" 
              stroke="#E70000" 
              strokeWidth={2}
            />
            
            {/* Linha Nacional */}
            <Line 
              type="monotone" 
              dataKey={currentConfig.dataKeyBr} 
              name="Média Brasil" 
              stroke="#FF7B00" 
              strokeWidth={2}
            />

            {/* Linha Região */}
            <Line 
              type="monotone" 
              dataKey={currentConfig.datakeyRegiao} 
              name="Média Região" 
              stroke="#0A5C36" 
              strokeWidth={2}
            />

            {/* Linha UF */}
            <Line 
              type="monotone" 
              dataKey={currentConfig.dataKeyUf} 
              name="Média Ceará" 
              stroke="#FFE745" 
              strokeWidth={2}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default EvolucaoHistorica;