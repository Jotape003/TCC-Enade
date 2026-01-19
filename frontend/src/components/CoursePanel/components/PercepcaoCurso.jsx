import React, { useState, useMemo, useEffect, useRef } from 'react';
import YearSelector from './shared/YearSelector';
import { exportToPNG, exportToCSV } from './shared/utils/exportGraph'; // Importação das funções
import DownloadButton from './shared/components/DownloadButton';

const PercepcaoCurso = ({ perfilData }) => {
  const chartRef = useRef(null); // Ref para o print da tela
  const [activeCategory, setActiveCategory] = useState('didatica');
  const [selectedYear, setSelectedYear] = useState('');

  const availableYears = useMemo(() => {
    if (!perfilData?.historico) return [];
    return Object.keys(perfilData.historico).sort((a, b) => b - a);
  }, [perfilData]);

  useEffect(() => {
    if (availableYears.length > 0) {
      setSelectedYear(availableYears[0]);
    }
  }, [availableYears]);

  const dadosAno = perfilData?.historico?.[selectedYear] || {};
  const questions = dadosAno[activeCategory] || [];

  // Função para baixar os dados da categoria atual
  const handleDownloadCSV = () => {
    if (!questions || questions.length === 0) return;
    const dataForExport = questions.map(q => ({
      Codigo: q.codigo,
      Pergunta: q.pergunta,
      Nota_Media_Likert: q.nota.toFixed(2),
      Percentual_Nao_Sei: `${q.nao_sei_perc}%`
    }));

    exportToCSV(dataForExport, `Percepcao_${activeCategory}_${selectedYear}`);
  };

  if (!perfilData || availableYears.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-20 bg-gray-50 rounded-2xl border border-dashed border-gray-200">
        <p className="text-gray-400 font-medium">Dados de percepção indisponíveis.</p>
      </div>
    );
  }

  // Adicionei ícones para dar um visual mais "App"
  const categories = [
    { 
      id: 'didatica', 
      label: 'Pedagógico', 
      icon: <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" /></svg> 
    },
    { 
      id: 'infra', 
      label: 'Infraestrutura', 
      icon: <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" /></svg> 
    },
    { 
      id: 'oportunidades', 
      label: 'Oportunidades', 
      icon: <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" /></svg> 
    },
    { 
      id: 'geral', 
      label: 'Geral', 
      icon: <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg> 
    }
  ];

  const getStatusColor = (perc) => {
    if (perc >= 50) return { border: 'border-orange-500', bg: 'bg-orange-50', text: 'text-orange-700', label: 'Alto índice de desconhecimento' };
    if (perc >= 20) return { border: 'border-amber-400', bg: 'bg-amber-50', text: 'text-amber-700', label: 'Índice moderado' };
    return { border: 'border-emerald-500', bg: 'bg-emerald-50', text: 'text-emerald-700', label: 'Dados confiáveis' };
  };

  const LikertBar = ({ value }) => {
    const widthPerc = (value / 6) * 100;
    return (
      <div className="mt-5 relative">
        <div className="flex justify-between items-end mb-2 text-xs font-bold uppercase tracking-wider text-gray-400">
          <span>Discordo (1)</span>
          <div className="flex items-baseline gap-1 text-indigo-600">
             <span className="text-2xl font-bold">{value.toFixed(2)}</span>
             <span className="text-[10px] opacity-70">/ 6.0</span>
          </div>
          <span>Concordo (6)</span>
        </div>
        
        <div className="w-full bg-gray-100 rounded-full h-2.5 relative overflow-hidden shadow-inner">
          {[1, 2, 3, 4, 5].map(i => (
             <div key={i} className="absolute top-0 bottom-0 w-0.5 bg-white z-10" style={{ left: `${(i/6)*100}%` }} />
          ))}
          
          <div 
            className="bg-indigo-600 h-full rounded-full transition-all duration-700 ease-out"
            style={{ width: `${widthPerc}%` }}
          ></div>
        </div>
      </div>
    );
  };

  return (
    <div className="space-y-8 animate-fade-in bg-white">      
      
      <div className="flex flex-col md:flex-row justify-between items-center gap-6 border-b border-gray-100 pb-6">
         <div className="text-center md:text-left">
            <h2 className="text-xl font-bold text-gray-800">Experiência Acadêmica</h2>
            <p className="text-sm text-gray-500 mt-1">Feedback qualitativo sobre as condições de ensino e aprendizagem.</p>
         </div>
         <YearSelector 
            years={availableYears} 
            selectedYear={selectedYear} 
            onChange={setSelectedYear} 
         />
      </div>

      <div className="flex justify-center md:justify-start items-center gap-4 pb-2">
      <div className="flex items-center gap-2 px-2 py-1.5 bg-gray-100/80 backdrop-blur-sm border border-gray-200 rounded-full shadow-inner">
          {categories.map((cat) => {
            const isActive = activeCategory === cat.id;
            return (
                <button
                key={cat.id}
                onClick={() => setActiveCategory(cat.id)}
                className={`
                    flex items-center gap-2 px-6 py-2 cursor-pointer rounded-full font-semibold transition-all duration-300
                    ${isActive
                    ? 'bg-indigo-600 text-white scale-105'
                    : 'bg-transparent text-gray-600 hover:bg-white hover:text-indigo-600 hover:shadow-sm'
                    }
                `}
                >
                {cat.icon}
                <span className="whitespace-nowrap">{cat.label}</span>
                </button>
            );
          })}

        </div>

        <div className="flex justify-end">
          <DownloadButton
            onDownloadPNG={() => exportToPNG(chartRef, `Grafico_PercepcaoCurso_${activeCategory}_${selectedYear}`)}
            onDownloadCSV={handleDownloadCSV}
          />
        </div>
      </div>

      <div ref={chartRef} className="grid grid-cols-1 md:grid-cols-2 gap-6 bg-white p-4">
        {questions.length > 0 ? (
          questions.map((q) => {
            const status = getStatusColor(q.nao_sei_perc);
            
            return (
              <div 
                key={q.codigo} 
                className={`
                    relative group ${status.border} bg-white p-6 rounded-xl shadow-sm border hover:shadow-lg transition-all duration-300
                    border-l-[6px]
                `}
              >
                <div className="flex justify-between items-start mb-4">
                  <div className="flex-1 pr-4">
                    <span className="inline-block text-[10px] font-bold text-gray-400 bg-gray-50 px-2 py-0.5 rounded border border-gray-100 mb-2">
                        QUESTÃO {q.codigo}
                    </span>
                    <h4 className="text-gray-700 font-medium text-sm leading-relaxed">
                        {q.pergunta}
                    </h4>
                  </div>
                  
                  {q.nao_sei_perc > 0 && (
                    <div className="relative group/tooltip">
                        <div className={`flex flex-col items-center justify-center min-w-[50px] px-2 py-1 rounded-lg border ${status.bg} ${status.text} border-transparent bg-opacity-50`}>
                            <span className="text-xs font-bold">{q.nao_sei_perc}%</span>
                            <span className="text-[8px] uppercase tracking-wide opacity-80">N/A</span>
                        </div>
                      
                        <div className="absolute right-0 top-full mt-2 w-60 p-4 bg-slate-800 text-white text-xs rounded-xl shadow-xl opacity-0 group-hover/tooltip:opacity-100 transition-opacity z-20 pointer-events-none transform origin-top-right">
                            <div className="font-bold text-slate-300 border-b border-slate-600 pb-2 mb-2 uppercase tracking-wider">
                                Respostas Inválidas
                            </div>
                            <div className="space-y-1">
                                <div className="flex justify-between">
                                    <span>Não sei / Não se aplica:</span>
                                    <span className="font-mono text-amber-400 font-bold">{q.nao_sei_qtd}</span>
                                </div>
                                <div className="flex justify-between">
                                    <span>Percentual do total:</span>
                                    <span className="font-mono text-amber-400 font-bold">{q.nao_sei_perc}%</span>
                                </div>
                            </div>
                            <div className="mt-3 text-slate-400 italic text-[10px] border-t border-slate-700 pt-2">
                                {status.label}
                            </div>
                        </div>
                    </div>
                  )}
                </div>

                <LikertBar value={q.nota} />
              </div>
            );
          })
        ) : (
          <div className="col-span-full flex flex-col items-center justify-center py-20 bg-gray-50 rounded-2xl border-2 border-dashed border-gray-200">
            <p className="text-gray-400 font-medium">Nenhuma pergunta encontrada para esta categoria em {selectedYear}.</p>
          </div>
        )}
      </div>

      {/* --- Legenda Minimalista --- */}
      <div className="flex flex-wrap justify-center gap-8 mt-6 pt-6 border-t border-gray-100 text-xs text-gray-500">
         <div className="flex items-center gap-2">
            <span className="w-1.5 h-1.5 bg-emerald-500 rounded-full"></span>
            <span className="w-8 h-1 bg-emerald-500 rounded-full"></span>
            <span>Dados sólidos (&lt;20% N/A)</span>
         </div>
         <div className="flex items-center gap-2">
            <span className="w-1.5 h-1.5 bg-amber-400 rounded-full"></span>
            <span className="w-8 h-1 bg-amber-400 rounded-full"></span>
            <span>Atenção (20-50% N/A)</span>
         </div>
         <div className="flex items-center gap-2">
            <span className="w-1.5 h-1.5 bg-orange-500 rounded-full"></span>
            <span className="w-8 h-1 bg-orange-500 rounded-full"></span>
            <span>Crítico (&gt;50% N/A)</span>
         </div>
      </div>
    </div>
  );
};

export default PercepcaoCurso;