import React, { useState } from 'react';
import { 
  ComposedChart, Line, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer
} from 'recharts';
import MetricTabs from './shared/MetricTabs';
import ComparisonSelector from './shared/ComparisonSelector';
import CustomTooltip from './shared/CustomTooltip';


const EvolucaoHistorica = ({ historicoData }) => {
  const [metric, setMetric] = useState('geral');
  
  const [comparisonState, setComparisonState] = useState({
    brasil: true,
    regiao: false,
    ceara: false,
    ufc: false,
  });

  const tabOptions = [
    { value: 'geral', label: 'Nota Geral' },
    { value: 'fg', label: 'Formação Geral (FG)' },
    { value: 'ce', label: 'Comp. Específico (CE)' }
  ];


  const comparisonColors = {
    brasil: "#FF7B00",
    regiao: "#0A5C36",
    ceara: "#FFE745",
    ufc: "#E70000",
  };

  const handleComparisonChange = (name, checked) => {
    setComparisonState(prevState => ({
      ...prevState,
      [name]: checked,
    }));
  };

  const config = {
    geral: { 
      title: "Trajetória da Nota Geral", 
      curso: "nota_geral", 
      brasil: "nacional_geral", ufc: "ufc_geral", regiao: "regiao_geral", ceara: "uf_geral" 
    },
    fg: { 
      title: "Trajetória na Formação Geral", 
      curso: "nota_fg", 
      brasil: "nacional_fg", ufc: "ufc_fg", regiao: "regiao_fg", ceara: "uf_fg"
    },
    ce: { 
      title: "Trajetória no Componente Específico", 
      curso: "nota_ce", 
      brasil: "nacional_ce" , ufc: "ufc_ce", regiao: "regiao_ce", ceara: "uf_ce"
    }
  };

  if (!historicoData || historicoData.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-20 bg-gray-50/50 rounded-3xl border-2 border-dashed border-gray-200">
        <p className="text-gray-400 font-medium">Histórico indisponível</p>
      </div>
    );
  }

  const currentConfig = config[metric];

  return (
    <div className="space-y-8 animate-fade-in">
      <div className="flex sm:flex-row justify-between items-center border-b border-gray-100 pb-6">
        <div>
           <h2 className="text-xl font-bold text-gray-800">Análise Temporal</h2>
           <p className="text-sm text-gray-500">Evolução das médias e tendências ao longo dos anos.</p>
        </div>
        <MetricTabs activeTab={metric} onChange={setMetric} options={tabOptions} />
      </div>

      <div className="bg-white rounded-3xl p-6 sm:p-10 border border-gray-100 shadow-2xl shadow-gray-200/50 relative overflow-hidden">
        
        {/* Título interno elegante */}
        <div className='flex justify-between'>
          <div className="z-10">
            <h4 className="text-lg font-bold text-gray-800 bg-white/80 backdrop-blur-sm px-4 py-1 rounded-full border border-gray-100 inline-block shadow-sm">
              {currentConfig.title}
            </h4>
          </div>

          <div className="origin-center lg:origin-right">
            <ComparisonSelector 
              comparisonState={comparisonState} 
              onToggle={handleComparisonChange} 
            />
          </div>
        </div>

        <div style={{ width: '100%', height: 420 }}>
          <ResponsiveContainer>
            <ComposedChart 
              data={historicoData} 
              margin={{ top: 60, right: 30, left: 0, bottom: 10 }}
            >
              <defs>
                <linearGradient id="colorCurso" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#4f46e5" stopOpacity={0.2}/>
                  <stop offset="95%" stopColor="#4f46e5" stopOpacity={0}/>
                </linearGradient>
              </defs>

              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
              
              <XAxis 
                dataKey="ano" 
                tick={{ fill: '#94a3b8', fontSize: 12, fontWeight: 600 }} 
                axisLine={false}
                tickLine={false}
                dy={15}
              />
              
              <YAxis 
                domain={[0, 100]} 
                tick={{ fill: '#94a3b8', fontSize: 12 }} 
                axisLine={false}
                tickLine={false}
                dx={-10}
              />
              
              <Tooltip content={<CustomTooltip />} cursor={{ stroke: '#64748b', strokeWidth: 1, strokeDasharray: '4 4' }} />
              
              <Area 
                type="monotone" 
                dataKey={currentConfig.curso}
                name="Curso" 
                stroke="#4f46e5"
                strokeWidth={4}
                fillOpacity={1} 
                fill="url(#colorCurso)"
                dot={{ r: 6, fill: "#fff", stroke: "#4f46e5", strokeWidth: 3 }}
                activeDot={{ r: 8, strokeWidth: 0, fill: "#4f46e5" }}
              />
              
              {Object.keys(comparisonColors).map((key) => {
                if (!comparisonState[key]) return null;

                const labels = {
                  ufc: "UFC (Área)", brasil: "Brasil", regiao: "Região", ceara: "Ceará"
                };

                return (
                  <Line
                    key={key}
                    type="monotone"
                    dataKey={currentConfig[key]}
                    name={labels[key]}
                    stroke={comparisonColors[key]}
                    strokeWidth={2.5}
                    strokeDasharray="0" 
                    dot={{ r: 4, fill: "#fff", stroke: comparisonColors[key], strokeWidth: 2 }}
                    activeDot={{ r: 6 }}
                  />
                );
              })}
            </ComposedChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default EvolucaoHistorica;