import React, { useState, useMemo, useEffect, useRef } from 'react';
import { Bar, LabelList } from 'recharts';
import StatCard from './shared/StatCard';
import YearSelector from './shared/YearSelector';
import ComparisonSelector from './shared/ComparisonSelector';
import HorizontalBarChart from './shared/HorizontalBarChart';
import { exportToPNG, exportToCSV } from './shared/utils/exportGraph';
import DownloadButton from './shared/components/DownloadButton';

const VisaoGeral = ({ historicalVisaoGData }) => {
  const availableYears = useMemo(() => {
    if (!historicalVisaoGData) return [];
    return Object.keys(historicalVisaoGData).sort((a, b) => b - a);
  }, [historicalVisaoGData]);

  const chartRef = useRef(null);

  
  const [selectedYear, setSelectedYear] = useState('');
  
  const visaoGeralData = useMemo(() => {
    if (!historicalVisaoGData || !selectedYear) return null;
    return historicalVisaoGData[selectedYear];
  }, [historicalVisaoGData, selectedYear]);

  const handleDownloadCSV = () => {
    const dataForExport = [
      { 
        Indicador: 'Nota Geral', 
        Valor: visaoGeralData.nota_geral, 
        Media_BR: visaoGeralData.media_nacional_geral,
        Media_Regiao: visaoGeralData.media_regiao_geral,
        Media_UFC: visaoGeralData.media_ufc_geral
      },
      { 
        Indicador: 'Formação Geral', 
        Valor: visaoGeralData.nota_fg, 
        Media_BR: visaoGeralData.media_nacional_fg,
        Media_Regiao: visaoGeralData.media_regiao_fg,
        Media_UFC: visaoGeralData.media_ufc_fg
      },
      { 
        Indicador: 'Comp. Específico', 
        Valor: visaoGeralData.nota_ce, 
        Media_BR: visaoGeralData.media_nacional_ce,
        Media_Regiao: visaoGeralData.media_regiao_ce,
        Media_UFC: visaoGeralData.media_ufc_ce
      },
    ];
    exportToCSV(dataForExport, `Visao_Geral_${selectedYear}`);
  };

  useEffect(() => {
    if (availableYears.length > 0 && !selectedYear) {
      setSelectedYear(availableYears[0]);
    }
  }, [availableYears, selectedYear]);


  const [activeMetric, setActiveMetric] = useState('geral');

  const [comparisonState, setComparisonState] = useState({
    brasil: true,
    ufc: false,
    regiao: false,
    ceara: false,
  });

  const handleComparisonChange = (name, checked) => {
    setComparisonState(prevState => ({ ...prevState, [name]: checked }));
  };

  const comparisonConfig = {
    brasil: { label: 'Brasil', color: '#FF7B00' },
    regiao: { label: 'Região', color: '#0A5C36' },
    ceara: { label: 'Ceará', color: '#FFE745' },
    ufc: { label: 'UFC (Área)', color: '#E70000' },
  };

  const metricsConfig = {
    geral: {
      label: "Nota Geral",
      keys: { curso: "nota_geral", ufc: "media_ufc_geral", brasil: "media_nacional_geral", regiao: "media_regiao_geral", ceara: "media_uf_geral" }
    },
    fg: {
      label: "Formação Geral (FG)",
      keys: { curso: "nota_fg", ufc: "media_ufc_fg", brasil: "media_nacional_fg", regiao: "media_regiao_fg", ceara: "media_uf_fg" }
    },
    ce: {
      label: "Componente Específico (CE)",
      keys: { curso: "nota_ce", ufc: "media_ufc_ce", brasil: "media_nacional_ce", regiao: "media_regiao_ce", ceara: "media_uf_ce" }
    }
  };

  const chartData = useMemo(() => {
    if (!visaoGeralData) return [];
    const config = metricsConfig[activeMetric];
    const keys = config.keys;

    return [
      {
        name: config.label,
        'Curso': visaoGeralData[keys.curso],
        'Brasil': visaoGeralData[keys.brasil],
        'Região': visaoGeralData[keys.regiao],
        'Ceará': visaoGeralData[keys.ceara],
        'UFC (Área)': visaoGeralData[keys.ufc],
      }
    ];
  }, [visaoGeralData, activeMetric]);

  if (!historicalVisaoGData) return <div className="p-8 text-center text-gray-400">Carregando histórico...</div>;
  if (!visaoGeralData) return <div className="p-8 text-center text-gray-400">Selecione um ano para visualizar.</div>;

  return (
    <div className="space-y-8 animate-fade-in">
      
      <div className="flex flex-col sm:flex-row justify-between items-center gap-4 border-b border-gray-100 pb-6">
        <div>
           <h2 className="text-xl font-bold text-gray-800">Indicadores de Desempenho</h2>
           <p className="text-sm text-gray-500">Visão macro comparativa dos resultados.</p>
        </div>
        <YearSelector
          years={availableYears}
          selectedYear={selectedYear} 
          onChange={setSelectedYear} 
        />
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
        <StatCard label="Nota Geral" value={visaoGeralData.nota_geral?.toFixed(1)} color="blue" isActive={activeMetric === 'geral'} onClick={() => setActiveMetric('geral')} />
        <StatCard label="Formação Geral" value={visaoGeralData.nota_fg?.toFixed(1)} color="green" isActive={activeMetric === 'fg'} onClick={() => setActiveMetric('fg')} />
        <StatCard label="Comp. Específico" value={visaoGeralData.nota_ce?.toFixed(1)} color="yellow" isActive={activeMetric === 'ce'} onClick={() => setActiveMetric('ce')} />
        <StatCard label="Participantes" value={visaoGeralData.numero_participantes} color="gray" />
      </div>


      <div className="bg-white rounded-2xl p-6 sm:p-8 border border-gray-100 shadow-xl shadow-gray-200/40" ref={chartRef}>
        
        <div className="flex flex-col lg:flex-row items-center justify-between mb-6 gap-6">
            <h4 className="text-lg font-bold text-gray-700 whitespace-nowrap flex items-center gap-2">
                <div className="z-10">
                  <h4 className="text-lg font-bold text-gray-800 bg-white/80 backdrop-blur-sm px-4 py-1 rounded-full border border-gray-100 inline-block shadow-sm">
                    Comparativo - {metricsConfig[activeMetric].label}
                  </h4>
                </div>
            </h4>

            
            <div className="flex items-center gap-4">
              <div className="flex justify-end">
                <DownloadButton
                  onDownloadPNG={() => exportToPNG(chartRef, `Grafico_VisaoGeral_${selectedYear}`)}
                  onDownloadCSV={handleDownloadCSV}
                />
              </div>
              <ComparisonSelector 
                comparisonState={comparisonState} 
                onToggle={handleComparisonChange} 
              />
            </div>
        </div>

        <HorizontalBarChart 
          data={chartData} 
          dataKey="name"
          height={350}
          barGap={8}
        >
             <Bar 
                dataKey="Curso" 
                fill="#051650" 
                radius={[0, 4, 4, 0]} 
                barSize={32}
                animationDuration={1500}
             >
                <LabelList 
                    dataKey="Curso" 
                    position="right" 
                    formatter={(value) => value?.toFixed(1)} 
                    style={{ fontWeight: 'bold', fill: '#051650' }} 
                />
             </Bar>

             {Object.entries(comparisonConfig).map(([key, { label, color }]) => (
                comparisonState[key] && (
                  <Bar 
                    key={key} 
                    dataKey={label} 
                    fill={color} 
                    radius={[0, 4, 4, 0]}
                    barSize={24}
                    animationDuration={1500}
                  >
                    <LabelList 
                      dataKey={label} 
                      position="right" 
                      formatter={(value) => value?.toFixed(1)} 
                      style={{ fontWeight: 'bold', fill: color }} 
                    />
                  </Bar>
                )
             ))}
        </HorizontalBarChart>

      </div>
    </div>
  );
};

export default VisaoGeral;