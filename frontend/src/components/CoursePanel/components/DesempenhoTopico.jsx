// src/components/CoursePanel/DesempenhoTopico.js
import React, { useMemo } from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Tooltip, Legend } from 'recharts';

const DesempenhoTopico = ({ competenciaData }) => {
  const chartData = useMemo(() => {
    if (!competenciaData) return [];
    
    return competenciaData.map(comp => ({
      topico: comp.competencia,
      "Desempenho (Obj. %)": comp.percentual_objetivas ?? 0,
    }));
  }, [competenciaData]);

  if (!competenciaData || competenciaData.length === 0) {
    return <p className="text-center text-gray-500 py-4">Dados de desempenho por tópico não disponíveis para este curso/ano.</p>;
  }

  return (
    <div style={{ width: '100%', height: 400 }}>
      <h4 className="text-md font-semibold text-gray-700 mb-2 text-center">Desempenho por Tópico (Objetivas)</h4>
      <ResponsiveContainer>
        <RadarChart cx="50%" cy="50%" outerRadius="100%" data={chartData}>
          <PolarGrid /> // Grade
          <PolarAngleAxis dataKey="topico" tick={{ fontSize: 12 }} /> // Competências
          <PolarRadiusAxis angle={30} domain={[0, 100]} /> // Desempenho por Competências
          
          <Radar 
            name="Desempenho do Curso" 
            dataKey="Desempenho (Obj. %)" 
            stroke="#4F46E5" 
            fill="#4F46E5" 
            fillOpacity={0.5} 
          />
          
          <Tooltip />
          <Legend />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default DesempenhoTopico;