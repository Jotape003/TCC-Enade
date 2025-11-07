import React, { useMemo, useState } from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Tooltip, Legend } from 'recharts';

const DesempenhoTopico = ({ desempenhoTopicoData }) => {
  const [comparison, setComparison] = useState('ufc');

  const chartData = useMemo(() => {
    if (!desempenhoTopicoData) return [];
    
    return desempenhoTopicoData.filter(comp => comp.percentual_objetivas_nacional != null) 
      .map(comp => ({
        topico: comp.competencia,
        "Curso": comp.percentual_objetivas_curso,
        "UFC (Área)": comp.percentual_objetivas_ufc ?? 0,
        "Brasil": comp.percentual_objetivas_nacional ?? 0,
        "Região": comp.percentual_objetivas_regiao ?? 0,
        "Ceará": comp.percentual_objetivas_uf ?? 0
    }));
  }, [desempenhoTopicoData]);

  // const charFGData = useMemo(() => {
  //   if (!desempenhoTopicoData) return [];

  //   return desempenhoTopicoData.filter()
  // })

  if (!desempenhoTopicoData || desempenhoTopicoData.length === 0) {
    return <p className="text-center text-gray-500 py-4">Dados de desempenho por tópico não disponíveis para este curso/ano.</p>;
  }
  const comparisonOptions = {
    ufc: {key: "UFC (Área)", color: "#E70000"},
    brasil: {key: "Brasil", color: "#FF7B00"},
    regiao: {key: "Região", color: "#0A5C36"},
    ceara: {key: "Ceará", color: "#FFE745"}
  }

  const {key: comparisonKey, color: comparisonColor} = comparisonOptions[comparison];

  return (
    <div className="space-y-4">
      {console.log(desempenhoTopicoData)}
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
        <label className="flex items-center space-x-2 cursor-pointer">
          <input
            type="radio"
            name="comparison"
            value="regiao"
            checked={comparison === 'regiao'}
            onChange={() => setComparison('regiao')}
            className="form-radio h-5 w-5 text-indigo-600"
          />
          <span className="text-gray-700">Comparar com Região</span>
        </label>
        <label className="flex items-center space-x-2 cursor-pointer">
          <input
            type="radio"
            name="comparison"
            value="ceara"
            checked={comparison === 'ceara'}
            onChange={() => setComparison('ceara')}
            className="form-radio h-5 w-5 text-indigo-600"
          />
          <span className="text-gray-700">Comparar com Ceará</span>
        </label>
      </div>

      <div style={{ width: '100%', height: 400 }}>
        <ResponsiveContainer>
          <RadarChart cx="50%" cy="50%" outerRadius="80%" data={chartData}>
            <PolarGrid />
            <PolarAngleAxis dataKey="topico" tick={{ fontSize: 14 }} />
            
            <Radar 
              name="Curso"
              dataKey="Curso" 
              stroke="#051650"
              fill="#051650" 
              fillOpacity={0.6}
            />
            
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