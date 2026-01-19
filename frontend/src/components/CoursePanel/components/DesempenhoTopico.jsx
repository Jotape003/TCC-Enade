import React, { useMemo, useState, useEffect, useRef } from 'react';
import { 
  Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Bar, Cell,
  ResponsiveContainer, Tooltip, Legend, 
  LabelList
} from 'recharts';

import MetricTabs from './shared/MetricTabs';
import ComparisonSelector from './shared/ComparisonSelector';
import ExamViewerModal from './shared/ViewerModal';
import QuestionTypeSelector from './shared/QuestionTypeSelector';
import HorizontalBarChart from './shared/HorizontalBarChart';
import { truncateName } from './shared/utils/truncateName';
import { exportToPNG, exportToCSV } from './shared/utils/exportGraph'; 
import DownloadButton from './shared/components/DownloadButton';

const DesempenhoTopico = ({ idCourse, historicalDesempData }) => {
  const chartRef = useRef(null); // Ref para o print da tela
  const [activeDataView, setActiveDataView] = useState('ce');
  const [dataType, setDataType] = useState('objetivas');
  const [selectedTopicInfo, setSelectedTopicInfo] = useState(null);

  const viewOptions = [
    { value: 'ce', label: 'Componente Específico (CE)' },
    { value: 'fg', label: 'Formação Geral (FG)' },
    { value: 'percepcao', label: 'Distribuição das Questões' }
  ];

  const availableYears = useMemo(() => {
    return Object.keys(historicalDesempData).sort();
  }, [historicalDesempData]);

  const [selectedYear, setSelectedYear] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [viewingQuestion, setViewingQuestion] = useState(null);
  const [modalQuestionType, setModalQuestionType] = useState('objetivas');

  useEffect(() => {
    if (availableYears.length > 0) {
      setSelectedYear(availableYears[availableYears.length - 1]);
    }
  }, [availableYears]);

  const handleDownloadCSV = () => {
    let dataForExport = [];
    let fileName = `Desempenho_${activeDataView}_${selectedYear}`;

    if (activeDataView === 'percepcao') {
      if (!perceptionData.length) return;
      dataForExport = perceptionData.map(item => ({
        Topico: item.topico,
        Quantidade_Total: item.quantidade,
        Tipo: item.tipo, // CE ou FG
        Questoes_Objetivas: item.objetivas.join('; '),
        Questoes_Discursivas: item.discursivas.join('; ')
      }));
      fileName = `Distribuicao_Questoes_${selectedYear}`;

    } else {
      if (!radarChartData.length) return;
      dataForExport = radarChartData.map(item => ({
        Topico: item.topico,
        [`Nota_Curso_${dataType}`]: item.Curso,
        Media_Brasil: item.Brasil,
        Media_Regiao: item.Região,
        Media_UFC: item["UFC (Área)"],
        Media_Ceara: item.Ceará
      }));
      fileName = `Desempenho_${activeDataView}_${dataType}_${selectedYear}`;
    }

    exportToCSV(dataForExport, fileName);
  };

  const handleQuestionClick = (questionLabel, forcedType = null) => {
    if (selectedTopicInfo?.tipo !== 'CE') return;

    setViewingQuestion(questionLabel);
    setModalQuestionType(forcedType || dataType);
    setIsModalOpen(true);
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
    brasil: { label: "Brasil", color: "#FF7B00", dataKeyObj: "percentual_objetivas_br", dataKeyDisc: "media_discursivas_br" },
    regiao: { label: "Região", color: "#0A5C36", dataKeyObj: "percentual_objetivas_regiao", dataKeyDisc: "media_discursivas_regiao" },
    ceara: { label: "Ceará", color: "#FFE745", dataKeyObj: "percentual_objetivas_uf", dataKeyDisc: "media_discursivas_uf" },
    ufc: { label: "UFC (Área)", color: "#E70000", dataKeyObj: "percentual_objetivas_ufc", dataKeyDisc: "media_discursivas_ufc" }
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

  const CustomRadarTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-slate-800/95 backdrop-blur-md p-4 rounded-xl shadow-2xl border border-slate-700 text-white min-w-[200px] z-50">
          <h4 className="text-sm font-bold text-slate-300 mb-3 border-b border-slate-600 pb-2 uppercase tracking-wide">
            {label}
          </h4>
          <div className="space-y-2">
            {payload.map((entry, index) => (
              <div key={index} className="flex items-center justify-between gap-4 text-sm">
                <div className="flex items-center gap-2">
                  <span 
                    className="w-2.5 h-2.5 rounded-full shadow-sm" 
                    style={{ backgroundColor: entry.color }} // Usa a cor da linha
                  />
                  <span className={entry.name === 'Curso' ? 'font-bold text-white' : 'text-slate-400 font-medium'}>
                    {entry.name}
                  </span>
                </div>
                <span className="font-mono font-bold">
                  {Number(entry.value).toFixed(1)}
                </span>
              </div>
            ))}
          </div>
        </div>
      );
    }
    return null;
  };

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
      <div className="w-lg flex flex-col items-center animate-in fade-in slide-in-from-top-2">
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
          className="w-full max-w-lg h-2 bg-gray-300 rounded-full appearance-none cursor-pointer focus:ring-2 focus:ring-gray-400"
        />
        
        <div className="flex justify-between w-full max-w-lg mt-2 text-xs text-gray-400">
          <span>{availableYears[0]}</span>
          <span>{availableYears[availableYears.length - 1]}</span>
        </div>
      </div>
    );
  };

  const renderSelectors = () => (
    <div className="flex flex-col lg:flex-row justify-center items-center gap-8 mb-8 p-4 rounded-2xl animate-in fade-in slide-in-from-top-4 duration-500">

      <div className="flex-shrink-0 scale-90 lg:scale-100 origin-center">
        <MetricTabs 
          activeTab={activeDataView} 
          onChange={setActiveDataView} 
          options={viewOptions} 
        />
      </div>

      {activeDataView !== 'percepcao' && (
        <>
          <div className="hidden lg:block w-px h-12 bg-gray-300/100"></div>
          
          <div className="flex-shrink-0">
            <QuestionTypeSelector
              value={dataType} 
              onChange={setDataType} 
            />
          </div>
        </>
      )}
      

    </div>
  );

  const renderRadarChart = () => {
    if (radarChartData.length === 0) {
      return (
        <div className="flex flex-col items-center justify-center py-20 bg-gray-50/50 rounded-3xl border border-dashed border-gray-200">
          <p className="text-gray-400 font-medium">Dados insuficientes para este filtro em {selectedYear}.</p>
        </div>
      );
    }

    const sortedData = [...radarChartData].sort((a, b) => b["Curso"] - a["Curso"]);
    const bestTopic = sortedData[0];
    const worstTopic = sortedData[sortedData.length - 1];

    return (
      <div className="flex flex-col gap-10 lg:flex-row items-center justify-center animate-in zoom-in-90 duration-700">
        
        <div className="w-full lg:flex-1 h-126">
          <ResponsiveContainer>
            <RadarChart cx="50%" cy="50%" outerRadius="80%" data={radarChartData}>
              <PolarGrid 
                gridType="circle" 
                stroke="#cbd5e1" 
                strokeWidth={0.5}  
              />
              
              <PolarAngleAxis 
                dataKey="topico" 
                tick={({ payload, x, y, cx, cy, textAnchor }) => {
                const dx = x - cx;
                const dy = y - cy;
                const factor = 1.10;

                return (
                  <text
                    x={cx + dx * factor}
                    y={cy + dy * factor}
                    textAnchor={textAnchor}
                    fill="#4b5563"
                    fontSize={12}
                    fontWeight={500}
                  >
                    <title>{payload.value}</title>
                    {truncateName(payload.value, 30)}
                  </text>
                );
              }}
              />
              
              <PolarRadiusAxis 
                angle={90} 
                domain={[0, 100]} 
                tick={{ fill: '#9ca3af', fontSize: 10 }} 
                axisLine={false} 
                orientation="middle"
              />

              <Radar
                name="Curso"
                dataKey="Curso"
                stroke="#4338ca"
                strokeWidth={3}
                fill="#4338ca"
                fillOpacity={0.4}
                isAnimationActive={true}
              />

              {Object.entries(comparisonDataKeys).map(([key, { label, color }]) => (
                comparisonState[key] && (
                  <Radar
                    key={key}
                    name={label}
                    dataKey={label}
                    stroke={color}
                    strokeWidth={2}
                    fill={color}
                    fillOpacity={0.3}
                    strokeDasharray="0"
                  />
                )
              ))}

              <Tooltip content={<CustomRadarTooltip />} cursor={{ stroke: '#94a3b8', strokeWidth: 1 }} />
              <Legend wrapperStyle={{ paddingTop: '10px', fontSize: '14px' }} iconType="circle"/>
              
            </RadarChart>
          </ResponsiveContainer>
        </div>

        <div className="lg:w-1/3 flex flex-col gap-4 self-center lg:self-start lg:mt-10">
            
            <div className="mb-2 px-1">
                <h4 className="text-2xs font-bold text-gray-500 uppercase tracking-wider">
                    Resumo do Desempenho
                </h4>
            </div>

            <div className="p-5 flex flex-col gap-2 rounded-2xl border border-emerald-200 bg-gradient-to-br from-emerald-50 to-emerald-100/50 transition-all hover:shadow-md">
                <div className='flex gap-2 items-center'>
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M6.633 10.25c.806 0 1.533-.446 2.031-1.08a9.041 9.041 0 0 1 2.861-2.4c.723-.384 1.35-.956 1.653-1.715a4.498 4.498 0 0 0 .322-1.672V2.75a.75.75 0 0 1 .75-.75 2.25 2.25 0 0 1 2.25 2.25c0 1.152-.26 2.243-.723 3.218-.266.558.107 1.282.725 1.282m0 0h3.126c1.026 0 1.945.694 2.054 1.715.045.422.068.85.068 1.285a11.95 11.95 0 0 1-2.649 7.521c-.388.482-.987.729-1.605.729H13.48c-.483 0-.964-.078-1.423-.23l-3.114-1.04a4.501 4.501 0 0 0-1.423-.23H5.904m10.598-9.75H14.25M5.904 18.5c.083.205.173.405.27.602.197.4-.078.898-.523.898h-.908c-.889 0-1.713-.518-1.972-1.368a12 12 0 0 1-.521-3.507c0-1.553.295-3.036.831-4.398C3.387 9.953 4.167 9.5 5 9.5h1.053c.472 0 .745.556.5.96a8.958 8.958 0 0 0-1.302 4.665c0 1.194.232 2.333.654 3.375Z" />
                    </svg>

                    <p className="text-xs font-bold text-emerald-600 uppercase tracking-wider">
                        Maior Nota
                    </p>
                </div>
                <div className="flex flex-col gap-1">
                      <span className="text-4xl font-extrabold text-emerald-900">
                        {bestTopic ? bestTopic["Curso"]?.toFixed(1) : '-'}
                      </span>
                      <p className="text-sm font-medium text-emerald-800/80 leading-snug line-clamp-3">
                        {bestTopic?.topico}
                      </p>
                </div>
            </div>

            <div className="p-5 flex flex-col gap-2 rounded-2xl border border-rose-200 bg-gradient-to-br from-rose-50 to-rose-100/50 transition-all hover:shadow-md">
                <div className='flex gap-2 items-center'>
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M7.498 15.25H4.372c-1.026 0-1.945-.694-2.054-1.715a12.137 12.137 0 0 1-.068-1.285c0-2.848.992-5.464 2.649-7.521C5.287 4.247 5.886 4 6.504 4h4.016a4.5 4.5 0 0 1 1.423.23l3.114 1.04a4.5 4.5 0 0 0 1.423.23h1.294M7.498 15.25c.618 0 .991.724.725 1.282A7.471 7.471 0 0 0 7.5 19.75 2.25 2.25 0 0 0 9.75 22a.75.75 0 0 0 .75-.75v-.633c0-.573.11-1.14.322-1.672.304-.76.93-1.33 1.653-1.715a9.04 9.04 0 0 0 2.86-2.4c.498-.634 1.226-1.08 2.032-1.08h.384m-10.253 1.5H9.7m8.075-9.75c.01.05.027.1.05.148.593 1.2.925 2.55.925 3.977 0 1.487-.36 2.89-.999 4.125m.023-8.25c-.076-.365.183-.75.575-.75h.908c.889 0 1.713.518 1.972 1.368.339 1.11.521 2.287.521 3.507 0 1.553-.295 3.036-.831 4.398-.306.774-1.086 1.227-1.918 1.227h-1.053c-.472 0-.745-.556-.5-.96a8.95 8.95 0 0 0 .303-.54" />
                </svg>

                  <p className="text-xs font-bold text-rose-600 uppercase tracking-wider">
                      Menor Nota
                  </p>
                </div>
                <div className="flex flex-col gap-1">
                      <span className="text-4xl font-extrabold text-rose-900">
                        {worstTopic ? worstTopic["Curso"]?.toFixed(1) : '-'}
                      </span>
                      <p className="text-sm font-medium text-rose-800/80 leading-snug line-clamp-3">
                        {worstTopic?.topico}
                      </p>
                </div>
            </div>

        </div>
      </div>
    );
  };
  
  const renderFGDiscursiveBarChart = () => {
    const data = radarChartData;
    if (!data || data.length === 0) return <div className="text-center py-20 text-gray-400">Dados insuficientes.</div>;
    
    const activeBars = [];
    
    activeBars.push({ 
      key: 'Curso', 
      color: '#4338ca', 
      size: 24, 
      label: 'Curso' 
    });

    Object.entries(comparisonDataKeys).forEach(([key, { label, color }]) => {
      if (comparisonState[key]) {
        activeBars.push({ 
          key: label, 
          color: color, 
          size: 14, 
          label: label,
          opacity: 0.8 
        });
      }
    });

    return (
      <div className="bg-white rounded-3xl p-6 sm:p-8 border border-gray-100 shadow-xl shadow-gray-200/40 animate-in fade-in slide-in-from-bottom-4 duration-700">
          <div className="flex items-center justify-between mb-6">
              <h4 className="text-lg font-bold text-gray-800 flex items-center gap-2">Comparativo de Desempenho</h4>
              <span className="text-xs font-medium text-indigo-600 bg-indigo-50 px-3 py-1 rounded-full border border-indigo-100 uppercase tracking-wide">
                  {dataType === 'objetivas' ? 'Nota Média' : 'Nota Discursiva'}
              </span>
          </div>

          <HorizontalBarChart
            data={data}
            dataKey="topico"
            barsConfig={activeBars}
            height={500}
            yAxisWidth={250}
          />
      </div>
    );
  };

  const renderPerceptionChart = () => {
      if (perceptionData.length === 0) return <p className="text-center text-gray-500 py-10">Sem dados de frequência para {selectedYear}.</p>;

      const maxQuantity = Math.max(...perceptionData.map(d => d.quantidade));

      
      const chartData = perceptionData.map(item => ({
        ...item,
        shortName: truncateName(item.topico, 30)
      }));

      const CE_COLOR = '#4338ca'; 
      const FG_COLOR = '#059669'; 

      return (
        <div className="flex flex-col lg:flex-row gap-8 animate-in fade-in slide-in-from-right-8 duration-500">
             
             <div className="flex-1 bg-white rounded-3xl p-6 border border-gray-100 shadow-xl shadow-gray-200/40">
                <div className="mb-4 flex justify-between items-end">
                    <div>
                        <h4 className="text-lg font-bold text-gray-800">Distribuição de Questões</h4>
                        <p className="text-sm text-gray-500">Quantidade de itens por tópico na prova.</p>
                    </div>
                    <div className="flex gap-3 text-xs font-bold">
                        <div className="flex justify-end">
                          <DownloadButton
                            onDownloadPNG={() => exportToPNG(chartRef, `Grafico_DesempenhoTopico_${selectedYear}`)}
                            onDownloadCSV={handleDownloadCSV}
                          />
                        </div>
                        <span className="flex items-center gap-1 text-indigo-700"><span className="w-2 h-2 rounded-full bg-indigo-700"></span> Específico</span>
                        <span className="flex items-center gap-1 text-emerald-600"><span className="w-2 h-2 rounded-full bg-emerald-600"></span> Geral</span>
                    </div>
                </div>
                
                <HorizontalBarChart 
                    data={chartData}
                    dataKey="shortName"
                    height={1200}
                    barSize={28}
                    yAxisWidth={280}
                    maxValue={maxQuantity}
                >
                    <Bar 
                        dataKey="quantidade" 
                        name="Qtd. Questões" 
                        radius={[0, 4, 4, 0]} 
                        onClick={(data) => {
                            if (data && data.payload) handleBarClick(data.payload); 
                        }}
                        cursor="pointer"
                    >
                        <LabelList 
                            dataKey="quantidade" 
                            position="right" 
                            style={{ fill: '#000', fontSize: '12px', fontWeight: 'bold' }}
                        />

                        {chartData.map((entry, index) => (
                            <Cell 
                                key={`cell-${index}`} 
                                fill={entry.tipo === 'CE' ? CE_COLOR : FG_COLOR} 
                                fillOpacity={selectedTopicInfo?.topico === entry.topico ? 1 : 0.6}
                            />
                        ))}
                    </Bar>
                </HorizontalBarChart>
            </div>
            
            <div className="lg:w-1/3 min-w-[300px]">
                {selectedTopicInfo ? (
                    <div className={`
                        sticky top-4 p-6 rounded-2xl shadow-lg border-2 animate-in zoom-in-95 duration-300 bg-white
                        ${selectedTopicInfo.tipo === 'CE' ? 'border-indigo-100' : 'border-emerald-100'}
                    `}>
                          <div className="mb-6 border-b border-gray-100 pb-4">
                            <span className={`
                                inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-wide mb-3
                                ${selectedTopicInfo.tipo === 'CE' ? 'bg-indigo-50 text-indigo-700' : 'bg-emerald-50 text-emerald-700'}
                            `}>
                                <span className={`w-1.5 h-1.5 rounded-full ${selectedTopicInfo.tipo === 'CE' ? 'bg-indigo-600' : 'bg-emerald-600'}`}></span>
                                {selectedTopicInfo.tipo === 'CE' ? 'Componente Específico' : 'Formação Geral'}
                            </span>
                            <h3 className="text-xl font-bold text-gray-800 leading-tight">{selectedTopicInfo.topico}</h3>
                          </div>

                          <div className="space-y-6">
                             <div className="flex items-center justify-between bg-gray-50 p-4 rounded-xl border border-gray-100">
                                <span className="text-sm font-bold text-gray-400 uppercase tracking-wider">Total de Itens</span>
                                <span className="text-3xl font-extrabold text-gray-800">{selectedTopicInfo.quantidade}</span>
                             </div>

                             <div>
                                 <h5 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3 flex items-center gap-2">
                                     <svg className="w-4 h-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" /></svg>
                                     Questões Objetivas
                                 </h5>
                                 <div className="flex flex-wrap gap-2">
                                     {selectedTopicInfo.objetivas?.length > 0 ? selectedTopicInfo.objetivas.map(q => (
                                          <button 
                                          key={q} 
                                          onClick={() => handleQuestionClick(q, 'objetivas')} 
                                          title="Visualizar questão"
                                          className="px-3 py-1.5 cursor-pointer bg-white border border-gray-200 hover:border-indigo-500 hover:bg-indigo-50 hover:text-indigo-700 text-gray-600 font-mono text-xs font-bold rounded-lg transition-all shadow-sm active:scale-95"
                                          >
                                             {q.toUpperCase()}
                                          </button>
                                     )) : <span className="text-xs text-gray-400 italic pl-1">Nenhuma registrada</span>}
                                 </div>
                             </div>

                             <div>
                                 <h5 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3 flex items-center gap-2">
                                     <svg className="w-4 h-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
                                     Questões Discursivas
                                 </h5>
                                 <div className="flex flex-wrap gap-2">
                                     {selectedTopicInfo.discursivas?.length > 0 ? selectedTopicInfo.discursivas.map(q => (
                                          <button 
                                           key={q} 
                                           onClick={() => handleQuestionClick(q, 'discursivas')}
                                           className="px-3 cursor-pointer py-1.5 bg-gray-50 border border-gray-200 hover:border-emerald-500 hover:bg-emerald-50 hover:text-emerald-700 text-gray-500 font-mono text-xs font-bold rounded-lg transition-all shadow-sm active:scale-95"
                                          >
                                             {q.toUpperCase()}
                                          </button>
                                     )) : <span className="text-xs text-gray-400 italic pl-1">Nenhuma registrada</span>}
                                 </div>
                             </div>

                             {selectedTopicInfo.tipo === 'CE' && selectedTopicInfo.lista_disciplinas?.length > 0 && (
                                 <div className="pt-4 border-t border-gray-100">
                                     <h5 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3 flex items-center gap-2">
                                        <svg className="w-4 h-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" /></svg>
                                         Disciplinas Relacionadas
                                     </h5>
                                     <div className="flex flex-wrap gap-2">
                                         {selectedTopicInfo.lista_disciplinas.map((disc, idx) => (
                                             <span key={idx} className="px-2 py-1 bg-indigo-50 text-indigo-700 text-[10px] uppercase font-bold rounded border border-indigo-100">
                                                 {disc}
                                             </span>
                                         ))}
                                     </div>
                                 </div>
                             )}
                          </div>
                    </div>
                ) : (
                    <div className="h-full min-h-[400px] flex flex-col items-center justify-center p-8 bg-gray-50/50 rounded-3xl border-2 border-dashed border-gray-200 text-center animate-in fade-in duration-500">
                        <div className="w-16 h-16 bg-white rounded-full shadow-sm flex items-center justify-center mb-4">
                            <svg className="w-8 h-8 text-indigo-300" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                        </div>
                        <h4 className="text-gray-800 font-bold mb-2">Detalhes do Tópico</h4>
                        <p className="text-sm text-gray-500 max-w-[200px]">Clique em uma barra do gráfico para ver as questões e disciplinas associadas.</p>
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
      <div className="flex flex-col sm:flex-row justify-between items-center border-b border-gray-100 pb-6">
        <div>
           <h2 className="text-xl font-bold text-gray-800">Diagnóstico de Conteúdos</h2>
           <p className="text-sm text-gray-500">Identificação de forças e fraquezas por área de conhecimento.</p>
        </div>
        {renderSlider()}  
      </div>

      <div className="sm:py-6" ref={chartRef}>
        {renderSelectors()}
        {activeDataView !== 'percepcao' && (
          <div className="flex items-center justify-center gap-4">
            <div className='flex items-center justify-center'>
              <ComparisonSelector 
                comparisonState={comparisonState} 
                onToggle={handleComparisonChange} 
              />
            </div>
            
            <div className="flex justify-end">
              <DownloadButton
                onDownloadPNG={() => exportToPNG(chartRef, `Grafico_DesempenhoTopico_${selectedYear}`)}
                onDownloadCSV={handleDownloadCSV}
              />
            </div>
          </div>
        )}
        
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
        courseID={idCourse}
        year={selectedYear}
        questionLabel={viewingQuestion}
        type={modalQuestionType}
      />

    </div>
  );
};

export default DesempenhoTopico;