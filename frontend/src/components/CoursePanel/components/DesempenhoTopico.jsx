// src/components/CoursePanel/DesempenhoTopico.js
import React, { useMemo } from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Tooltip, Legend } from 'recharts';

const DesempenhoTopico = ({ competenciaData }) => {

  const chartData = useMemo(() => {
    if (!competenciaData) return [];
    
    return competenciaData.map(comp => ({
      topico: comp.competencia,
      // Renomeia as chaves para a legenda do gráfico
      "Curso": comp.percentual_objetivas_curso ?? 0,
      "UFC (Área)": comp.percentual_objetivas_ufc ?? 0,
      
    }));
  }, [competenciaData]);

  if (!competenciaData || competenciaData.length === 0) {
    return <p className="text-center text-gray-500 py-4">Dados de desempenho por tópico não disponíveis para este curso/ano.</p>;
  }

  return (
    <div style={{ width: '100%', height: 400 }}>
      <h4 className="text-md font-semibold text-gray-700 mb-2 text-center">Desempenho por Tópico (Objetivas)</h4>
      <ResponsiveContainer>
        <RadarChart cx="50%" cy="50%" outerRadius="80%" data={chartData}>
          <PolarGrid />
          <PolarAngleAxis dataKey="topico" tick={{ fontSize: 12 }} />
          <PolarRadiusAxis angle={30} domain={[0, 100]} />
          
          {/* Radar 1: Desempenho do Curso */}
          <Radar 
            name="Curso" // Corresponde à chave em chartData
            dataKey="Curso" 
            stroke="#4F46E5" // Indigo
            fill="#4F46E5" 
            fillOpacity={0.6} 
          />
          
          {/* Radar 2: Média da UFC (Área) */}
          <Radar 
            name="UFC (Área)" // Corresponde à chave em chartData
            dataKey="UFC (Área)"
            stroke="#10B981" // Verde
            fill="#10B981"
            fillOpacity={0.4} // Opacidade menor para ver sobreposição
          />
          
          <Tooltip />
          <Legend />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default DesempenhoTopico;