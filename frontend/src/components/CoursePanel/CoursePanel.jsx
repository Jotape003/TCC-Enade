import React, { useMemo } from 'react';
import VisaoGeral from './components/VisaoGeral';
import PercepcaoCurso from './components/PercepcaoCurso';
import EvolucaoHistorica from './components/EvolucaoHistorica';
import DesempenhoTopico from './components/DesempenhoTopico';

const CoursePanel = ({ visaoGeralData, desempenhoTopicoData, activeTab, evolucaoHistorica, perfilConsolidadoData }) => {
  if (!visaoGeralData) {
    return (
      <div className="border-t pt-4 mt-4 first:mt-0 first:pt-0 first:border-0">
        <h3 className="text-xl font-bold text-gray-600 mb-4">Carregando dados...</h3>
      </div>
    );
  }

  const courseName = useMemo(() => {
    if (!visaoGeralData) return '';
    const years = Object.keys(visaoGeralData);
    if (years.length > 0) {
      const lastYear = years[years.length - 1];
      return visaoGeralData[lastYear]?.NO_CURSO || 'Curso Sem Nome';
    }
    return 'Curso Não Identificado';
  }, [visaoGeralData]);


  const renderTabContent = () => {
    switch (activeTab) {
      case 'visao-geral':
        return <VisaoGeral historicalVisaoGData={visaoGeralData} />;

      case 'evolucao-historica':
        return (
          <EvolucaoHistorica historicoData={evolucaoHistorica} />
        );
      case 'desempenho-topico':
         return <DesempenhoTopico historicalDesempData={desempenhoTopicoData} />;
        
      case 'analise-perfil':
         return <PercepcaoCurso perfilData={perfilConsolidadoData} selectedYear={2021} />;

      default:
        return <div>Selecione uma aba válida</div>;
    }
  };

  return (
    <>
      <h3 className="flex text-3xl font-bold justify-center p-6 text-indigo-800">{courseName}</h3>
      {renderTabContent()}
    </>
  );
};

export default CoursePanel;