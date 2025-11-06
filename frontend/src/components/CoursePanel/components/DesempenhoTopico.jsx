import React, { useMemo, useState } from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Tooltip, Legend } from 'recharts';

const DesempenhoTopico = ({ competenciaData }) => {
  const [comparison, setComparison] = useState('ufc');

  const chartData = useMemo(() => {
    if (!competenciaData) return [];
    
    return competenciaData.map(comp => ({
      topico: comp.competencia,
      "Curso": comp.percentual_objetivas_curso ?? 0,
      "UFC (Área)": comp.percentual_objetivas_ufc ?? 0,
      "Brasil": comp.percentual_objetivas_nacional ?? 0,
    }));
  }, [competenciaData]);

  if (!competenciaData || competenciaData.length === 0) {
    return <p className="text-center text-gray-500 py-4">Dados de desempenho por tópico não disponíveis para este curso/ano.</p>;
  }

  const comparisonKey = comparison === 'ufc' ? "UFC (Área)" : "Brasil";
  const comparisonColor = comparison === 'ufc' ? "#10B981" : "#FBBF24";

  return (
    <div className="space-y-4">
      <h4 className="text-md font-semibold text-gray-700 mb-2 text-center">Desempenho por Tópico (Objetivas)</h4>
      <div className="flex justify-center space-x-4">
        <label className="flex items-center space-x-2 cursor-pointer">
          <input
            type="radio"
            name="comparison"
            value="ufc"
            checked={comparison === 'ufc'}
            onChange={() => setComparison('ufc')}
            className="form-radio h-5 w-5 text-indigo-600"
          />
          <span className="text-gray-700">Comparar com UFC (Área)</span>
        </label>
        <label className="flex items-center space-x-2 cursor-pointer">
          <input
            type="radio"
            name="comparison"
            value="brasil"
            checked={comparison === 'brasil'}
            onChange={() => setComparison('brasil')}
            className="form-radio h-5 w-5 text-indigo-600"
          />
          <span className="text-gray-700">Comparar com Brasil</span>
        </label>
      </div>

      {/* --- Gráfico de Radar --- */}
      <div style={{ width: '100%', height: 400 }}>
        <ResponsiveContainer>
          <RadarChart cx="50%" cy="50%" outerRadius="80%" data={chartData}>
            <PolarGrid />
            <PolarAngleAxis dataKey="topico" tick={{ fontSize: 14 }} />
            
            <Radar 
              name="Curso"
              dataKey="Curso" 
              stroke="#4F46E5"
              fill="#4F46E5" 
              fillOpacity={0.6}
            />
            
            {/* Radar 2: Comparativo (Dinâmico) */}
            <Radar 
              name={comparisonKey}
              dataKey={comparisonKey}
              stroke={comparisonColor}
              fill={comparisonColor}
              fillOpacity={0.4}
            />
            
            <Tooltip />
            <Legend />
          </RadarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default DesempenhoTopico;