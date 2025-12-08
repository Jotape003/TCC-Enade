import React, { useState, useMemo } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LabelList } from 'recharts';

const VisaoGeral = ({ visaoGeralData }) => {
  // Estado para controlar qual métrica está sendo visualizada no gráfico
  const [activeMetric, setActiveMetric] = useState('geral'); // 'geral', 'fg', 'ce'

  // Configuração para mapear as chaves do JSON para cada tipo de métrica
  // Isso resolve a inconsistência de nomes (ex: nota_geral_media_curso vs media_ufc_geral)
  const metricsConfig = {
    geral: {
      label: "Nota Geral",
      keys: {
        curso: "nota_geral_media_curso",
        ufc: "media_ufc_geral",
        brasil: "media_nacional_geral",
        regiao: "media_regiao_geral",
        ceara: "media_uf_geral"
      }
    },
    fg: {
      label: "Formação Geral (FG)",
      keys: {
        curso: "nota_fg_media_curso",
        ufc: "media_ufc_fg",
        brasil: "media_nacional_fg",
        regiao: "media_regiao_fg",
        ceara: "media_uf_fg"
      }
    },
    ce: {
      label: "Componente Específico (CE)",
      keys: {
        curso: "nota_ce_media_curso",
        ufc: "media_ufc_ce",
        brasil: "media_nacional_ce",
        regiao: "media_regiao_ce",
        ceara: "media_uf_ce"
      }
    }
  };

  // Prepara os dados do gráfico dinamicamente com base na métrica ativa
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

  if (!visaoGeralData) {
     return <p className="text-gray-500">Dados não disponíveis.</p>;
  }

  return (
    <div className="space-y-8">
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-center">
        <div 
          className={`p-4 rounded-lg shadow cursor-pointer transition-colors ${activeMetric === 'geral' ? 'bg-blue-200 ring-2 ring-blue-400' : 'bg-blue-100 hover:bg-blue-200'}`}
          onClick={() => setActiveMetric('geral')}
        >
          <p className="text-lg text-blue-700 font-semibold">Nota Média Geral</p>
          <p className="text-3xl font-bold text-blue-900">{visaoGeralData.nota_geral_media_curso ?? 'N/A'}</p>
        </div>
        <div 
          className={`p-4 rounded-lg shadow cursor-pointer transition-colors ${activeMetric === 'fg' ? 'bg-green-200 ring-2 ring-green-400' : 'bg-green-100 hover:bg-green-200'}`}
          onClick={() => setActiveMetric('fg')}
        >
          <p className="text-lg text-green-700 font-semibold">Nota Formação Geral</p>
          <p className="text-3xl font-bold text-green-900">{visaoGeralData.nota_fg_media_curso ?? 'N/A'}</p>
        </div>
        <div 
          className={`p-4 rounded-lg shadow cursor-pointer transition-colors ${activeMetric === 'ce' ? 'bg-yellow-200 ring-2 ring-yellow-400' : 'bg-yellow-100 hover:bg-yellow-200'}`}
          onClick={() => setActiveMetric('ce')}
        >
          <p className="text-lg text-yellow-700 font-semibold">Nota Comp. Específico</p>
          <p className="text-3xl font-bold text-yellow-900">{visaoGeralData.nota_ce_media_curso ?? 'N/A'}</p>
        </div>
        <div className="bg-gray-200 p-4 rounded-lg shadow">
          <p className="text-lg text-gray-700 font-semibold">Total de Participantes</p>
          <p className="text-3xl font-bold text-gray-900">{visaoGeralData.total_participantes ?? 'N/A'}</p>
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

      <div className="bg-white rounded-lg mb-10">
        <div style={{ width: '100%', height: 400 }}>
          <h4 className="text-lg font-semibold text-gray-700 text-center">
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