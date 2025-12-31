import React, { useMemo, useState, useEffect } from 'react';
import { 
  Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Cell,
  ResponsiveContainer, Tooltip, Legend 
} from 'recharts';

import MetricTabs from './shared/MetricTabs';
import ComparisonSelector from './shared/ComparisonSelector';
import { getFilterLinks } from '../../../services/enadeService';
import ExamViewerModal from './shared/ViewerModal';

const DesempenhoTopico = ({ idCourse, historicalDesempData }) => {
  const [activeDataView, setActiveDataView] = useState('ce');
  const [dataType, setDataType] = useState('objetivas');
  const [selectedTopicInfo, setSelectedTopicInfo] = useState(null);

  const viewOptions = [
    { value: 'ce', label: 'Componente Específico (CE)' },
    { value: 'fg', label: 'Formação Geral (FG)' },
    { value: 'percepcao', label: 'Percepção da Prova' }
  ];

  const availableYears = useMemo(() => {
    return Object.keys(historicalDesempData).sort();
  }, [historicalDesempData]);

  const [selectedYear, setSelectedYear] = useState('');

  const [examLinksMap, setExamLinksMap] = useState({});
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [viewingQuestion, setViewingQuestion] = useState(null);
  const [currentPdfUrl, setCurrentPdfUrl] = useState(null);

  // Efeito para carregar o JSON de links ao montar o componente
  useEffect(() => {
    const fetchLinks = async () => {
      const links = await getFilterLinks(idCourse);
      setExamLinksMap(links);
    };
    fetchLinks();
  }, []);

  useEffect(() => {
    if (availableYears.length > 0) {
      setSelectedYear(availableYears[availableYears.length - 1]);
    }
  }, [availableYears]);

  const handleQuestionClick = (questionLabel) => {
    const courseLinks = examLinksMap;
    console.log(courseLinks);
    const pdfUrl = courseLinks ? courseLinks[selectedYear] : null;
    console.log(pdfUrl);
    if (pdfUrl) {
      setCurrentPdfUrl(pdfUrl);
      setViewingQuestion(questionLabel);
      setIsModalOpen(true);
    } else {
      // Feedback melhorado para o usuário
      alert(`Prova de ${selectedYear} não encontrada no cadastro para este curso (Cód: ${idCourse}).`);
    }
  };

  const currentYearData = useMemo(() => {
    if (!historicalDesempData || !selectedYear) return null;
    return historicalDesempData[selectedYear];
  }, [historicalDesempData, selectedYear]);

  const componenteEspecificoData = currentYearData?.desempenho_CE;
  const formacaoGeralData = currentYearData?.desempenho_FG;

  const [comparisonState, setComparisonState] = useState({
    ufc: false,
    brasil: true,
    regiao: false,
    ceara: false,
  });

  const comparisonDataKeys = {
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

  const handleComparisonChange = (name, checked) => {
     setComparisonState(prevState => ({ ...prevState, [name]: checked }));
  };

  const handleBarClick = (data) => {
    setSelectedTopicInfo(data);
  };

  const renderSlider = () => {
    if (availableYears.length <= 1) return null;

    const currentIndex = availableYears.indexOf(selectedYear);

    return (
      <div className="flex flex-col items-center justify-center mb-6 animate-in fade-in slide-in-from-top-2">
        <div className="flex items-center justify-between w-full max-w-lg mb-2">
           <span className="text-lg font-semibold text-gray-600">Ano da Edição</span>
           <span className="text-2xl font-bold text-gray-700">{selectedYear}</span>
        </div>
        
        <input 
          type="range" 
          min="0" 
          max={availableYears.length - 1} 
          value={currentIndex === -1 ? 0 : currentIndex}
          onChange={(e) => setSelectedYear(availableYears[e.target.value])}
          className="w-full max-w-lg h-2 bg-gray-300 rounded-lg appearance-none cursor-pointer focus:outline-none focus:ring-2 focus:ring-indigo-500/50"
        />
        
        <div className="flex justify-between w-full max-w-lg mt-2 text-xs text-gray-400">
          <span>{availableYears[0]}</span>
          <span>{availableYears[availableYears.length - 1]}</span>
        </div>
      </div>
    );
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

      <ComparisonSelector 
        comparisonState={comparisonState} 
        onToggle={handleComparisonChange} 
      />
    </div>
  );

  const renderRadarChart = () => {
    if (radarChartData.length === 0) {
      return <div className="text-center py-20 text-gray-400 flex flex-col items-center">Dados insuficientes para este filtro em {selectedYear}.</div>;
    }
    return (
      <div className="w-full h-[450px] animate-in zoom-in-95 duration-500">
        <ResponsiveContainer>
          <RadarChart cx="50%" cy="50%" outerRadius="75%" data={radarChartData}>
             <PolarGrid stroke="#e5e7eb" />
            <PolarAngleAxis dataKey="topico" tick={{ fontSize: 14, fill: '#4b5563' }} />
            <PolarRadiusAxis angle={30} tick={false} axisLine={false} />
            <Radar name="Curso" dataKey="Curso" stroke="#4338ca" strokeWidth={2} fill="#4338ca" fillOpacity={0.5} />
            {Object.entries(comparisonDataKeys).map(([key, { label, color }]) => (
              comparisonState[key] && (
                <Radar key={key} name={label} dataKey={label} stroke={color} strokeWidth={1.5} fill={color} fillOpacity={0.4} />
              )
            ))}
            <Tooltip contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)' }} itemStyle={{ fontSize: '13px', fontWeight: 500 }} />
            <Legend wrapperStyle={{ paddingTop: '20px' }}/>
          </RadarChart>
        </ResponsiveContainer>
      </div>
    )
  };
  
  const renderFGDiscursiveBarChart = () => {
      const data = radarChartData;
       if (!data || data.length === 0) return <div className="text-center py-20 text-gray-400">Dados insuficientes.</div>;
       
       return (
        <div className="bg-white rounded-lg">
            <ResponsiveContainer>
            <BarChart data={data} margin={{ top: 10, right: 50, left: 50, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="topico" tick={{ fontSize: 14 }} />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="Curso" fill="#4338ca" name="Curso" barSize={30} radius={[4, 4, 0, 0]}/>
                {Object.entries(comparisonDataKeys).map(([key, { label, color }]) =>
                comparisonState[key] ? <Bar key={key} dataKey={label} fill={color} name={label} barSize={30} /> : null
                )}
            </BarChart>
            </ResponsiveContainer>
        </div>
       )
  };

  const renderPerceptionChart = () => {
      if (perceptionData.length === 0) return <p className="text-center text-gray-500 py-10">Sem dados de frequência para {selectedYear}.</p>;
      const chartHeight = Math.max(400, perceptionData.length * 50);

      return (
        <div className="flex flex-col lg:flex-row gap-6 animate-in fade-in slide-in-from-right-8 duration-500">
             <div className="flex-1 overflow-x-auto">
                <div style={{ height: chartHeight, minWidth: '100%' }}>
                    <ResponsiveContainer width="100%" height="100%">
                    <BarChart layout="vertical" data={perceptionData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }} onClick={(data) => { if (data && data.activePayload) handleBarClick(data.activePayload[0].payload); }}>
                        <CartesianGrid strokeDasharray="3 3" horizontal={false} />
                        <XAxis type="number" hide />
                        <YAxis dataKey="topico" type="category" width={180} tick={{ fontSize: 11, width: 170 }} interval={0} />
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
                                <h5 className="text-sm font-semibold text-gray-700 flex items-center gap-2 mb-2">Questões Objetivas</h5>
                                <div className="flex flex-wrap gap-2">
                                    {selectedTopicInfo.objetivas?.map(q => (
                                        <button 
                                          key={q} 
                                          // --- AQUI: Conectando a função ---
                                          onClick={() => handleQuestionClick(q)} 
                                          title="Clique para ver na prova"
                                          className="px-2 py-1 bg-white border border-gray-200 hover:border-indigo-500 hover:bg-indigo-50 hover:text-indigo-700 cursor-pointer transition-all rounded text-xs font-mono text-gray-600 shadow-sm"
                                        >
                                          {q.toUpperCase()}
                                        </button>
                                    ))}
                                </div>
                            </div>
                             <div>
                                <h5 className="text-sm font-semibold text-gray-700 flex items-center gap-2 mb-2">Questões Discursivas</h5>
                                <div className="flex flex-wrap gap-2">
                                    {selectedTopicInfo.discursivas?.map(q => (
                                        <span key={q} className="px-2 py-1 bg-white border border-gray-200 rounded text-xs font-mono text-gray-600 shadow-sm">{q.toUpperCase()}</span>
                                    ))}
                                </div>
                            </div>
                             {selectedTopicInfo.tipo === 'CE' && (
                                <div>
                                    <h5 className="text-sm font-semibold text-gray-700 flex items-center gap-2 mb-2">Disciplinas Relacionadas</h5>
                                    <div className="flex flex-col gap-2">
                                        {selectedTopicInfo.lista_disciplinas?.map(q => (
                                            <span key={q} className="w-fit px-2 py-1 bg-white border border-gray-200 rounded text-xs text-gray-700 shadow-sm">{q.toUpperCase()}</span>
                                        ))}
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>
                ) : (
                    <div className="h-full flex flex-col items-center justify-center p-6 bg-gray-50 rounded-xl border border-dashed border-gray-300 text-center min-h-[300px]">
                        <BarChart className="w-12 h-12 text-gray-300 mb-3" />
                        <p className="text-gray-500 font-medium">Selecione um tópico no gráfico</p>
                    </div>
                )}
            </div>
        </div>
      );
  };

  if (!historicalDesempData) {
     return <div className="p-10 text-center">Sem dados para mostrar</div>; 
  }

  return (
    <div className="bg-white">
      {renderSlider()}  

      <MetricTabs 
        activeTab={activeDataView} 
        onChange={setActiveDataView} 
        options={viewOptions} 
      />

      <div className="p-4 sm:p-6">
        {activeDataView !== 'percepcao' && renderSelectors()}
        
        <div className="mt-4">
          {activeDataView === 'percepcao' 
            ? renderPerceptionChart() 
            : (activeDataView === 'fg' && dataType === 'discursivas'
              ? renderFGDiscursiveBarChart()
              : renderRadarChart()
            )
          }
        </div>
      </div>
      
      <ExamViewerModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        pdfUrl={currentPdfUrl}
        questionLabel={viewingQuestion}
        year={selectedYear}
      />

    </div>
  );
};

export default DesempenhoTopico;