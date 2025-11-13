import React, { act, useMemo, useState } from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Tooltip, Legend } from 'recharts';

const DesempenhoTopico = ({ componenteEspecificoData, formacaoGeralData }) => {
  const [activeDataView, setActiveDataView] = useState('ce');
  const [dataType, setDataType] = useState('objetivas');

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

  const activeData = useMemo(() => {
    return activeDataView === 'ce' ? componenteEspecificoData : formacaoGeralData;
  }, [activeDataView, componenteEspecificoData, formacaoGeralData]);

  const chartData = useMemo(() => {
    if (!activeData) return [];

    
    const dataArray = Object.entries(activeData).map(([competencia, dados]) => ({
      competencia,
      ...dados
    }));
    
    const isObjetivas = dataType === 'objetivas';
    const cursoMetricKey = isObjetivas ? 'percentual_objetivas_curso' : 'media_discursivas_curso';

    return dataArray
      .filter(comp => comp[cursoMetricKey] != null)
      .map(comp => ({
        topico: comp.competencia,
        "Curso": comp[cursoMetricKey],
        "UFC (Área)": (isObjetivas ? comp.percentual_objetivas_ufc : comp.media_discursivas_ufc) ?? 0,
        "Brasil": (isObjetivas ? comp.percentual_objetivas_br : comp.media_discursivas_br) ?? 0,
        "Região": (isObjetivas ? comp.percentual_objetivas_regiao : comp.media_discursivas_regiao) ?? 0,
        "Ceará": (isObjetivas ? comp.percentual_objetivas_uf : comp.media_discursivas_uf) ?? 0,
      }));
  }, [activeData, dataType]);

  const handleComparisonChange = (event) => {
    const { name, checked } = event.target;
    setComparisonState(prevState => ({
      ...prevState,
      [name]: checked,
    }));
  };

  if (!componenteEspecificoData && !formacaoGeralData) {
    return <p className="text-center text-gray-500 py-4">Sem Dados</p>;
  }

  const renderSelectors = () => (
    <>
      <div className="flex justify-center space-x-10">
        <label className="flex items-center space-x-2 cursor-pointer">
          <input type="radio" name="dataType" value="objetivas" checked={dataType === 'objetivas'} onChange={() => setDataType('objetivas')} className="form-radio h-5 w-5 text-indigo-600"/>
          <span className="text-gray-700">Objetivas (Acerto %)</span>
        </label>
        <label className="flex items-center space-x-2 cursor-pointer">
          <input type="radio" name="dataType" value="discursivas" checked={dataType === 'discursivas'} onChange={() => setDataType('discursivas')} className="form-radio h-5 w-5 text-indigo-600"/>
          <span className="text-gray-700">Discursivas (Média 0-100)</span>
        </label>
      </div>

      <div className="flex justify-center items-center space-x-7 pt-4">
        <h4 className="text-lg font-semibold text-gray-700">Comparar com:</h4>
        <div className="flex space-x-4">
          {Object.entries(comparisonOptions).map(([key, { label }]) => (
            <label key={key} className="flex items-center space-x-2 cursor-pointer">
              <input
                type="checkbox"
                name={key}
                checked={comparisonState[key]}
                onChange={handleComparisonChange}
                className="form-checkbox h-5 w-5 text-indigo-600 rounded"
              />
              <span className="text-gray-700">{label}</span>
            </label>
          ))}
        </div>
      </div>
    </>
  );

  const renderChart = () => {
    if (chartData.length === 0) {
      return <p className="text-center text-gray-500 py-10">Dados não disponíveis para o tipo de nota selecionado ({dataType}).</p>;
    }
    
    return (
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
            
            {Object.entries(comparisonOptions).map(([key, { label, color }]) => (
              comparisonState[key] && (
                <Radar 
                  key={key}
                  name={label}
                  dataKey={label}
                  stroke={color}
                  fill={color}
                  fillOpacity={0.4}
                />
              )
            ))}

            <Tooltip />
            <Legend />
          </RadarChart>
        </ResponsiveContainer>
      </div>
    );
  };

  return (
    <div className="space-y-4">
      <div className="border-b border-gray-200">
        <nav className="flex justify-around" aria-label="Tabs">
          <button
            onClick={() => setActiveDataView('ce')}
            className={`whitespace-nowrap py-3 px-1 border-b-2 font-medium text-lg cursor-pointer ${
              activeDataView === 'ce'
                ? 'border-indigo-500 text-indigo-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Componente Específico (CE)
          </button>
          <button
            onClick={() => setActiveDataView('fg')}
            className={`whitespace-nowrap py-3 px-1 border-b-2 font-medium text-lg cursor-pointer ${
              activeDataView === 'fg'
                ? 'border-indigo-500 text-indigo-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Formação Geral (FG)
          </button>
        </nav>
      </div>

      {renderSelectors()}
      {renderChart()}

    </div>
  );
};

export default DesempenhoTopico;