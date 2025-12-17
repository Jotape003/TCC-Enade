import React, { useState, useMemo, useEffect } from 'react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LabelList 
} from 'recharts';

const VisaoGeral = ({ historicalVisaoGData }) => {
  const availableYears = useMemo(() => {
    if (!historicalVisaoGData) return [];
    return Object.keys(historicalVisaoGData).sort((a, b) => b - a);
  }, [historicalVisaoGData]);

  const [selectedYear, setSelectedYear] = useState('');

  useEffect(() => {
    if (availableYears.length > 0 && !selectedYear) {
      setSelectedYear(availableYears[0]);
    }
  }, [availableYears, selectedYear]);

  const visaoGeralData = useMemo(() => {
    if (!historicalVisaoGData || !selectedYear) return null;
    return historicalVisaoGData[selectedYear];
  }, [historicalVisaoGData, selectedYear]);

  const [activeMetric, setActiveMetric] = useState('geral');

  const metricsConfig = {
    geral: {
      label: "Nota Geral",
      keys: {
        curso: "nota_geral",
        ufc: "media_ufc_geral",
        brasil: "media_nacional_geral",
        regiao: "media_regiao_geral",
        ceara: "media_uf_geral"
      }
    },
    fg: {
      label: "Formação Geral (FG)",
      keys: {
        curso: "nota_fg",
        ufc: "media_ufc_fg",
        brasil: "media_nacional_fg",
        regiao: "media_regiao_fg",
        ceara: "media_uf_fg"
      }
    },
    ce: {
      label: "Componente Específico (CE)",
      keys: {
        curso: "nota_ce",
        ufc: "media_ufc_ce",
        brasil: "media_nacional_ce",
        regiao: "media_regiao_ce",
        ceara: "media_uf_ce"
      }
    }
  };

  const chartData = useMemo(() => {
    if (!visaoGeralData) return [];

    const config = metricsConfig[activeMetric];
    const keys = config.keys;

    return [
      {
        name: config.label,
        'Curso': visaoGeralData[keys.curso] ?? 0,
        'UFC (Área)': visaoGeralData[keys.ufc] ?? 0,
        'Brasil': visaoGeralData[keys.brasil] ?? 0,
        'Região': visaoGeralData[keys.regiao] ?? 0,
        'Ceará': visaoGeralData[keys.ceara] ?? 0,
      }
    ];
  }, [visaoGeralData, activeMetric]);

  if (!historicalVisaoGData) {
     return <p className="text-gray-500 p-4">Carregando histórico...</p>;
  }

  if (!visaoGeralData) {
     return <p className="text-gray-500 p-4">Selecione um ano para visualizar.</p>;
  }

  return (
    <div className="space-y-8">
      
      <div className="flex justify-center items-center">
        <div className="flex items-center space-x-3 bg-gray-50 px-3 py-2 rounded-lg border border-gray-200">
            <span className="text-lg font-semibold text-gray-600">Ano da Edição:</span>
            <select 
                value={selectedYear}
                onChange={(e) => setSelectedYear(e.target.value)}
                className="bg-white border border-gray-300 text-gray-700 text-lg rounded focus:ring-indigo-500 focus:border-indigo-500 block p-1 font-bold cursor-pointer"
            >
                {availableYears.map(year => (
                    <option key={year} value={year}>{year}</option>
                ))}
            </select>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-center">
        <div 
          className={`p-4 rounded-lg shadow cursor-pointer transition-colors ${activeMetric === 'geral' ? 'bg-blue-200 ring-2 ring-blue-400' : 'bg-blue-100 hover:bg-blue-200'}`}
          onClick={() => setActiveMetric('geral')}
        >
          <p className="text-lg text-blue-700 font-semibold">Nota Média Geral</p>
          <p className="text-3xl font-bold text-blue-900">{visaoGeralData.nota_geral?.toFixed(1) ?? 'N/A'}</p>
        </div>
        <div 
          className={`p-4 rounded-lg shadow cursor-pointer transition-colors ${activeMetric === 'fg' ? 'bg-green-200 ring-2 ring-green-400' : 'bg-green-100 hover:bg-green-200'}`}
          onClick={() => setActiveMetric('fg')}
        >
          <p className="text-lg text-green-700 font-semibold">Nota Formação Geral</p>
          <p className="text-3xl font-bold text-green-900">{visaoGeralData.nota_fg?.toFixed(1) ?? 'N/A'}</p>
        </div>
        <div 
          className={`p-4 rounded-lg shadow cursor-pointer transition-colors ${activeMetric === 'ce' ? 'bg-yellow-200 ring-2 ring-yellow-400' : 'bg-yellow-100 hover:bg-yellow-200'}`}
          onClick={() => setActiveMetric('ce')}
        >
          <p className="text-lg text-yellow-700 font-semibold">Nota Comp. Específico</p>
          <p className="text-3xl font-bold text-yellow-900">{visaoGeralData.nota_ce?.toFixed(1) ?? 'N/A'}</p>
        </div>
        <div className="bg-gray-200 p-4 rounded-lg shadow">
          <p className="text-lg text-gray-700 font-semibold">Total de Participantes</p>
          <p className="text-3xl font-bold text-gray-900">{visaoGeralData.numero_participantes ?? 'N/A'}</p>
        </div>
      </div>

      <div className="flex justify-center bg-gray-50 p-4 space-x-4 rounded-lg">
        {['geral', 'fg', 'ce'].map((m) => (
          <button
            key={m}
            onClick={() => setActiveMetric(m)}
            className={`px-4 py-2 rounded-md text-lg font-medium transition-all cursor-pointer ${
              activeMetric === m
                ? 'bg-white text-indigo-600 shadow-sm ring-1 ring-gray-200'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            {metricsConfig[m].label}
          </button>
        ))}
      </div>

      <div className="bg-white rounded-lg mb-15">
        <div style={{ width: '100%', height: 400 }}>
          <h4 className="text-lg font-semibold text-gray-700 text-center mb-4">
            Comparativo - {metricsConfig[activeMetric].label}
          </h4>
          <ResponsiveContainer>
            <BarChart 
              data={chartData} 
              layout="vertical" 
              margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
              barSize={30}
            >
              <CartesianGrid strokeDasharray="3 3" horizontal={false} />
              <XAxis type="number" domain={[0, 100]} />
              <YAxis type="category" dataKey="name" hide />
              <Tooltip cursor={{fill: 'transparent'}} />
              <Legend />
              
              <Bar dataKey="Curso" fill="#051650" radius={[0, 4, 4, 0]}>
                <LabelList dataKey="Curso" position="right" formatter={(value) => value?.toFixed(1)} />
              </Bar>
              <Bar dataKey="UFC (Área)" fill="#E70000" radius={[0, 4, 4, 0]}>
                <LabelList dataKey="UFC (Área)" position="right" formatter={(value) => value?.toFixed(1)} />
              </Bar>
              <Bar dataKey="Brasil" fill="#FF7B00" radius={[0, 4, 4, 0]}>
                <LabelList dataKey="Brasil" position="right" formatter={(value) => value?.toFixed(1)} />
              </Bar>
              <Bar dataKey="Região" fill="#0A5C36" radius={[0, 4, 4, 0]}>
                <LabelList dataKey="Região" position="right" formatter={(value) => value?.toFixed(1)} />
              </Bar>
              <Bar dataKey="Ceará" fill="#FFE745" radius={[0, 4, 4, 0]}>
                <LabelList dataKey="Ceará" position="right" formatter={(value) => value?.toFixed(1)} />
              </Bar>

            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default VisaoGeral;