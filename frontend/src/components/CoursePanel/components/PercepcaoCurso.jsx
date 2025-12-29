import React, { useState, useMemo, useEffect } from 'react';

const PercepcaoCurso = ({ perfilData }) => {
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

  if (!perfilData || availableYears.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-64 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300 p-6">
        <p className="text-gray-500 text-lg font-medium">Dados de perfil não disponíveis.</p>
        <span className="text-sm text-gray-400 mt-2 text-center">
          Verifique se este curso possui histórico de questionários processados.
        </span>
      </div>
    );
  }

  const dadosAno = perfilData.historico[selectedYear] || {};
  const questions = dadosAno[activeCategory] || [];

  const categories = [
    { id: 'didatica', label: 'Org. Didático-Pedagógica' },
    { id: 'infra', label: 'Infraestrutura' },
    { id: 'oportunidades', label: 'Oportunidades' },
    { id: 'geral', label: 'Avaliação Geral' }
  ];

  const getStatusColor = (perc) => {
    if (perc >= 50) return { border: 'border-orange-500', bg: 'bg-orange-100', text: 'text-orange-700', label: 'Alto índice de desconhecimento' };
    if (perc >= 20) return { border: 'border-yellow-400', bg: 'bg-yellow-100', text: 'text-yellow-700', label: 'Índice moderado' };
    return { border: 'border-green-500', bg: 'bg-green-50', text: 'text-green-700', label: 'Dados confiáveis' };
  };

  const LikertBar = ({ value }) => {
    const widthPerc = (value / 6) * 100;
    return (
      <div className="mt-4 relative">
        <div className="flex justify-between text-xs text-gray-500 mb-1 font-medium">
          <span>Discordo (1)</span>
          <span className="text-indigo-700 font-bold text-sm">{value.toFixed(2)}</span>
          <span>Concordo (6)</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-3 relative overflow-hidden">
          {[1, 2, 3, 4, 5].map(i => (
             <div key={i} className="absolute top-0 bottom-0 border-r border-white/50 z-10" style={{ left: `${(i/6)*100}%` }} />
          ))}
          <div 
            className="bg-indigo-600 h-full rounded-full transition-all duration-500 ease-out shadow-sm"
            style={{ width: `${widthPerc}%` }}
          ></div>
        </div>
      </div>
    );
  };

  return (
    <div className="space-y-6 animate-fadeIn">
      
      <div className="flex flex-col md:flex-row justify-between items-center gap-4 pb-4 border-b border-gray-200">
        
        <div className="flex items-center space-x-2 bg-gray-100 p-2 rounded-lg">
          <span className="text-sm font-semibold text-gray-600 pl-2">Ano:</span>
          <select 
            value={selectedYear}
            onChange={(e) => setSelectedYear(e.target.value)}
            className="bg-white border-gray-300 text-gray-700 text-sm rounded-md focus:ring-indigo-500 focus:border-indigo-500 block p-2 cursor-pointer shadow-sm"
          >
            {availableYears.map(year => (
              <option key={year} value={year}>{year}</option>
            ))}
          </select>
        </div>

        <div className="flex flex-wrap justify-center gap-2">
          {categories.map((cat) => (
            <button
              key={cat.id}
              onClick={() => setActiveCategory(cat.id)}
              className={`px-4 py-2 rounded-full text-xs font-bold uppercase tracking-wider transition-all duration-200 ${
                activeCategory === cat.id
                  ? 'bg-indigo-600 text-white shadow-md'
                  : 'bg-white text-gray-500 border border-gray-200 hover:bg-gray-50 hover:text-indigo-600'
              }`}
            >
              {cat.label}
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {questions.length > 0 ? (
          questions.map((q) => {
            const status = getStatusColor(q.nao_sei_perc);
            
            return (
              <div 
                key={q.codigo} 
                className={`relative group bg-white p-6 rounded-xl border-l-4 shadow-sm hover:shadow-md transition-all duration-300 ${status.border}`}
              >
                <div className="flex justify-between items-start mb-3">
                  <div className="flex-1 pr-2">
                    <span className="text-[10px] font-mono font-bold text-gray-400 uppercase tracking-wider mb-1 block">{q.codigo}</span>
                    <h4 className="text-gray-800 font-medium text-base leading-snug">{q.pergunta}</h4>
                  </div>
                  
                  {q.nao_sei_perc > 0 && (
                    <div className="relative group/tooltip">
                       <div className={`px-2 py-1 rounded-md text-[10px] font-bold uppercase tracking-wide cursor-help ${status.bg} ${status.text}`}>
                        {q.nao_sei_perc}% N/A
                      </div>
                      
                      <div className="absolute right-0 top-full mt-2 w-64 p-3 bg-gray-900 text-white text-xs rounded-lg shadow-xl opacity-0 group-hover/tooltip:opacity-100 transition-opacity z-20 pointer-events-none transform origin-top-right">
                        <div className="font-semibold mb-1 pb-1 border-b border-gray-700">Dados de Participação</div>
                        <div className="flex justify-between py-1">
                          <span>"Não sei/Não aplica":</span>
                          <span className="font-mono text-yellow-400">{q.nao_sei_qtd}</span>
                        </div>
                        <div className="flex justify-between py-1">
                          <span>Percentual:</span>
                          <span className="font-mono text-yellow-400">{q.nao_sei_perc}%</span>
                        </div>
                        <div className="mt-2 text-gray-400 italic text-[10px]">
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
          <div className="col-span-full text-center py-16 bg-gray-50 rounded-xl border border-dashed border-gray-200">
            <p className="text-gray-400 font-medium">Nenhuma pergunta encontrada para esta categoria em {selectedYear}.</p>
          </div>
        )}
      </div>

      <div className="mt-8 bg-blue-50 p-4 rounded-lg border border-blue-100 text-sm text-blue-800 flex flex-col sm:flex-row gap-4 items-start sm:items-center">
        <div className="flex items-center font-bold shrink-0">
           <span className="bg-blue-200 p-1 rounded mr-2">ℹ️</span> Como ler:
        </div>
        <ul className="flex-1 grid sm:grid-cols-2 gap-x-4 gap-y-1 list-disc pl-4 sm:pl-0 sm:list-none text-blue-900/80 text-xs">
          <li><strong>Nota:</strong> Média das respostas válidas (1 a 6).</li>
          <li className="flex items-center"><span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span> Borda Verde: &lt;20% "Não sei"</li>
          <li className="flex items-center"><span className="w-2 h-2 bg-yellow-400 rounded-full mr-2"></span> Borda Amarela: 20-50% "Não sei"</li>
          <li className="flex items-center"><span className="w-2 h-2 bg-orange-500 rounded-full mr-2"></span> Borda Laranja: &gt;50% "Não sei"</li>
        </ul>
      </div>
    </div>
  );
};

export default PercepcaoCurso;