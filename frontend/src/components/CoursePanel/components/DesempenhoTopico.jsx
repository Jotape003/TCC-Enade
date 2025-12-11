import React, { useMemo, useState } from 'react';
import { 
  Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Cell,
  ResponsiveContainer, Tooltip, Legend 
} from 'recharts';

const DesempenhoTopico = ({ componenteEspecificoData, formacaoGeralData }) => {
  const [activeDataView, setActiveDataView] = useState('ce');
  const [dataType, setDataType] = useState('objetivas');

  const [selectedTopicInfo, setSelectedTopicInfo] = useState(null);

  const [comparisonState, setComparisonState] = useState({
    ufc: false,
    brasil: false,
    regiao: false,
    ceara: false,
  });

  const comparisonOptions = {
    ufc: { label: "UFC (Área)", color: "#E70000", dataKeyObj: "percentual_objetivas_ufc", dataKeyDisc: "media_discursivas_ufc" },
    brasil: { label: "Brasil", color: "#FF7B00", dataKeyObj: "percentual_objetivas_br", dataKeyDisc: "media_discursivas_br" },
    regiao: { label: "Região", color: "#0A5C36", dataKeyObj: "percentual_objetivas_regiao", dataKeyDisc: "media_discursivas_regiao" },
    ceara: { label: "Ceará", color: "#FFE745", dataKeyObj: "percentual_objetivas_uf", dataKeyDisc: "media_discursivas_uf" }
  };

  const radarChartData = useMemo(() => {
    if (activeDataView === 'percepcao') return [];

    const activeData = activeDataView === 'ce' ? componenteEspecificoData : formacaoGeralData;
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
        fullMark: isObjetivas ? 100 : 100,
        "Curso": comp[cursoMetricKey],
        "UFC (Área)": (isObjetivas ? comp.percentual_objetivas_ufc : comp.media_discursivas_ufc) ?? 0,
        "Brasil": (isObjetivas ? comp.percentual_objetivas_br : comp.media_discursivas_br) ?? 0,
        "Região": (isObjetivas ? comp.percentual_objetivas_regiao : comp.media_discursivas_regiao) ?? 0,
        "Ceará": (isObjetivas ? comp.percentual_objetivas_uf : comp.media_discursivas_uf) ?? 0,
      }));
  }, [activeDataView, componenteEspecificoData, formacaoGeralData, dataType]);

  const perceptionData = useMemo(() => {
    if (activeDataView !== 'percepcao') return [];

    const processData = (data, type) => {
      if (!data) return [];
      return Object.entries(data).map(([topic, values]) => ({
        topico: topic,
        quantidade: values.quantidade_questoes_total || 0,
        objetivas: values.lista_questoes_objetivas || [],
        discursivas: values.lista_questoes_discursivas || [],
        tipo: type,
        lista_disciplinas: values.lista_disciplinas || [],
      }));
    };

    const ceData = processData(componenteEspecificoData, 'CE');
    const fgData = processData(formacaoGeralData, 'FG');

    return [...ceData, ...fgData].sort((a, b) => b.quantidade - a.quantidade);
  }, [activeDataView, componenteEspecificoData, formacaoGeralData]);

  const handleComparisonChange = (event) => {
    const { name, checked } = event.target;
    setComparisonState(prevState => ({ ...prevState, [name]: checked }));
  };

  const handleBarClick = (data) => {
    setSelectedTopicInfo(data);
  };

  const renderSelectors = () => (
    <div className="animate-in fade-in slide-in-from-top-4 duration-500">
      <div className="flex justify-center space-x-10 mb-6">
        <label className="flex items-center space-x-2 cursor-pointer group">
          <input type="radio" name="dataType" value="objetivas" checked={dataType === 'objetivas'} onChange={() => setDataType('objetivas')} className="form-radio h-5 w-5 text-indigo-600 focus:ring-indigo-500"/>
          <span className="text-gray-700 group-hover:text-indigo-600 transition-colors">Objetivas (Acerto %)</span>
        </label>
        <label className="flex items-center space-x-2 cursor-pointer group">
          <input type="radio" name="dataType" value="discursivas" checked={dataType === 'discursivas'} onChange={() => setDataType('discursivas')} className="form-radio h-5 w-5 text-indigo-600 focus:ring-indigo-500"/>
          <span className="text-gray-700 group-hover:text-indigo-600 transition-colors">Discursivas (Média 0-100)</span>
        </label>
      </div>

      <div className="flex justify-center items-center space-x-7">
        <h4 className="text-lg font-semibold text-gray-700">Comparar com:</h4>
        <div className="flex space-x-4">
          {Object.entries(comparisonOptions).map(([key, { label, color }]) => (
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
    </div>
  );

  const renderRadarChart = () => {
    if (radarChartData.length === 0) {
      return <div className="text-center py-20 text-gray-400 flex flex-col items-center">Dados insuficientes para este filtro.</div>;
    }
    
    return (
      <div className="w-full h-[450px] animate-in zoom-in-95 duration-500">
        <ResponsiveContainer>
          <RadarChart cx="50%" cy="50%" outerRadius="75%" data={radarChartData}>
            <PolarGrid stroke="#e5e7eb" />
            <PolarAngleAxis dataKey="topico" tick={{ fontSize: 14, fill: '#4b5563' }} />
            <PolarRadiusAxis angle={30} tick={false} axisLine={false} />
            
            <Radar 
              name="Curso"
              dataKey="Curso" 
              stroke="#4338ca"
              strokeWidth={2}
              fill="#4338ca" 
              fillOpacity={0.5}
            />
            
            {Object.entries(comparisonOptions).map(([key, { label, color }]) => (
              comparisonState[key] && (
                <Radar 
                  key={key}
                  name={label}
                  dataKey={label}
                  stroke={color}
                  strokeWidth={1.5}
                  fill={color}
                  fillOpacity={0.4}
                />
              )
            ))}

            <Tooltip 
              contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)' }}
              itemStyle={{ fontSize: '13px', fontWeight: 500 }}
            />
            <Legend wrapperStyle={{ paddingTop: '20px' }}/>
          </RadarChart>
        </ResponsiveContainer>
      </div>
    );
  };

  const renderPerceptionChart = () => {
    if (perceptionData.length === 0) return <p className="text-center text-gray-500 py-10">Sem dados de frequência.</p>;

    const chartHeight = Math.max(400, perceptionData.length * 50);

    return (
      <div className="flex flex-col lg:flex-row gap-6 animate-in fade-in slide-in-from-right-8 duration-500">
        <div className="flex-1 overflow-x-auto">
          <div style={{ height: chartHeight, minWidth: '100%' }}>
            <h3 className="text-center text-gray-600 mb-2 text-sm">Clique nas barras para ver as questões</h3>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart 
                layout="vertical" 
                data={perceptionData} 
                margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                onClick={(data) => {
                  if (data && data.activePayload && data.activePayload.length > 0) {
                    handleBarClick(data.activePayload[0].payload);
                  }
                }}
              >
                <CartesianGrid strokeDasharray="3 3" horizontal={false} />
                <XAxis type="number" hide />
                <YAxis 
                  dataKey="topico" 
                  type="category" 
                  width={180} 
                  tick={{ fontSize: 11, width: 170 }} 
                  interval={0}
                />
                <Tooltip cursor={{fill: '#f3f4f6'}} contentStyle={{ borderRadius: '8px', border: 'none' }}/>
                <Bar dataKey="quantidade" name="Qtd. Questões" radius={[0, 4, 4, 0]} barSize={20}>
                    {perceptionData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.tipo === 'CE' ? '#4338ca' : '#059669'} cursor="pointer" />
                    ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="lg:w-1/3 min-w-[250px]">
          {selectedTopicInfo ? (
            <div className="bg-white border border-indigo-100 rounded-xl shadow-lg p-6 sticky top-4 animate-in zoom-in-95 duration-300">
              <div className="flex items-start justify-between mb-4">
                <div>
                    <span className={`text-xs font-bold px-2 py-1 rounded-full ${selectedTopicInfo.tipo === 'CE' ? 'bg-indigo-100 text-indigo-700' : 'bg-emerald-100 text-emerald-700'}`}>
                        {selectedTopicInfo.tipo === 'CE' ? 'Componente Específico' : 'Formação Geral'}
                    </span>
                    <h3 className="text-lg font-bold text-gray-800 mt-2 leading-tight">{selectedTopicInfo.topico}</h3>
                </div>
              </div>
              
              <div className="space-y-4">
                <div className="bg-gray-50 p-3 rounded-lg">
                    <p className="text-sm text-gray-500 mb-1">Total de Itens</p>
                    <p className="text-2xl font-bold text-gray-800">{selectedTopicInfo.quantidade}</p>
                </div>

                <div>
                    <h5 className="text-sm font-semibold text-gray-700 flex items-center gap-2 mb-2">
                        Questões Objetivas
                    </h5>
                    <div className="flex flex-wrap gap-2">
                        {selectedTopicInfo.objetivas && selectedTopicInfo.objetivas.length > 0 ? (
                            selectedTopicInfo.objetivas.map(q => (
                                <span key={q} className="px-2 py-1 bg-white border border-gray-200 rounded text-xs font-mono text-gray-600 shadow-sm">
                                    {q.toUpperCase()}
                                </span>
                            ))
                        ) : (
                            <span className="text-xs text-gray-400 italic">Nenhuma</span>
                        )}
                    </div>
                </div>

                <div>
                    <h5 className="text-sm font-semibold text-gray-700 flex items-center gap-2 mb-2">
                        Questões Discursivas
                    </h5>
                    <div className="flex flex-wrap gap-2">
                        {selectedTopicInfo.discursivas && selectedTopicInfo.discursivas.length > 0 ? (
                            selectedTopicInfo.discursivas.map(q => (
                                <span key={q} className="px-2 py-1 bg-white border border-gray-200 rounded text-xs font-mono text-gray-600 shadow-sm">
                                    {q.toUpperCase()}
                                </span>
                            ))
                        ) : (
                            <span className="text-xs text-gray-400 italic">Nenhuma</span>
                        )}
                    </div>
                </div>

                {selectedTopicInfo.tipo === 'CE' && (
                  <div>
                        <h5 className="text-sm font-semibold text-gray-700 flex items-center gap-2 mb-2">
                          Lista de Disciplinas
                      </h5>
                      <div className="flex flex-wrap gap-2">
                          {selectedTopicInfo.lista_disciplinas && selectedTopicInfo.lista_disciplinas.length > 0 ? (
                              selectedTopicInfo.lista_disciplinas.map(q => (
                                  <span key={q} className="flex flex-col px-2 py-1 bg-white border border-gray-200 rounded text-xs font-mono text-gray-600 shadow-sm">
                                      {q.toUpperCase()}
                                  </span>
                              ))
                          ) : (
                              <span className="text-xs text-gray-400 italic">Nenhuma</span>
                          )}
                      </div>
                  </div>    
                )}
              </div>

              
              <div className="mt-6 pt-4 border-t border-gray-100">
                <p className="text-xs text-center text-gray-400">Dados extraídos do Relatório Enade</p>
              </div>
            </div>
          ) : (
            <div className="h-full flex flex-col items-center justify-center p-6 bg-gray-50 rounded-xl border border-dashed border-gray-300 text-center min-h-[300px]">
                <BarChart className="w-12 h-12 text-gray-300 mb-3" />
                <p className="text-gray-500 font-medium">Selecione um tópico no gráfico</p>
                <p className="text-sm text-gray-400 mt-1">Clique nas barras para ver quais questões (objetivas e discursivas) compõem o tópico.</p>
            </div>
          )}
        </div>
      </div>
    );
  };

  if (!componenteEspecificoData && !formacaoGeralData) {
    return (
        <div className="flex flex-col items-center justify-center py-12 bg-gray-50 rounded-lg">
            <p className="text-gray-500 font-medium">Sem dados disponíveis para visualização.</p>
        </div>
    );
  }

  return (
    <div className="bg-white">
      <nav className="flex justify-center bg-gray-50 p-4 space-x-4 rounded-lg" aria-label="Tabs">
        <button
          onClick={() => setActiveDataView('ce')}
          className={`px-4 py-2 rounded-md text-lg font-medium transition-all cursor-pointer ${
            activeDataView === 'ce'
              ? 'bg-white text-indigo-600 shadow-sm ring-1 ring-gray-200'
              : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          Componente Específico
        </button>
        <button
          onClick={() => setActiveDataView('fg')}
          className={`px-4 py-2 rounded-md text-lg font-medium transition-all cursor-pointer ${
            activeDataView === 'fg'
              ? 'bg-white text-indigo-600 shadow-sm ring-1 ring-gray-200'
              : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          Formação Geral
        </button>
        <button
          onClick={() => setActiveDataView('percepcao')}
          className={`px-4 py-2 rounded-md text-lg font-medium transition-all cursor-pointer ${
            activeDataView === 'percepcao'
              ? 'bg-white text-indigo-600 shadow-sm ring-1 ring-gray-200'
              : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          Percepção da Prova
        </button>
      </nav>

      <div className="p-4 sm:p-6">
        {activeDataView !== 'percepcao' && renderSelectors()}
        
        <div className="mt-4">
            {activeDataView === 'percepcao' ? renderPerceptionChart() : renderRadarChart()}
        </div>
      </div>
    </div>
  );
};

export default DesempenhoTopico;