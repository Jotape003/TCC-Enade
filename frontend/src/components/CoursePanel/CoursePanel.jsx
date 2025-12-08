import React from 'react';
import VisaoGeral from './components/VisaoGeral';
import AnalisePerfil from './components/AnalisePerfil';
import EvolucaoHistorica from './components/EvolucaoHistorica';
import DesempenhoTopico from './components/DesempenhoTopico';

const CoursePanel = ({ courseId, visaoGeralData, componenteEspecificoData, formacaoGeralData, activeTab, selectedYear, evolucaoHistorica }) => {
  if (!visaoGeralData) {
    return (
      <div className="border-t pt-4 mt-4 first:mt-0 first:pt-0 first:border-0">
        <h3 className="text-xl font-bold text-gray-600 mb-4">Carregando dados ({selectedYear})...</h3>
      </div>
    );
  }

  const renderTabContent = () => {
    switch (activeTab) {
      case 'visao-geral':
        return <VisaoGeral visaoGeralData={visaoGeralData} />;

      case 'evolucao-historica':
        return (
          <EvolucaoHistorica historicoData={evolucaoHistorica} />
        );
      case 'desempenho-topico':
         return <DesempenhoTopico componenteEspecificoData={componenteEspecificoData} formacaoGeralData={formacaoGeralData} />;
        
      case 'analise-perfil':
         return (
          <div className="text-center py-10 text-gray-500">
            <p className="text-lg">Análise de Perfil - Em construção.</p>
          </div>
        );
      default:
        return <div>Selecione uma aba válida</div>;
    }
  };

  return (
    <>
      <h3 className="flex text-3xl font-bold justify-center p-6 text-indigo-800">{visaoGeralData.NO_CURSO} ({selectedYear})</h3>
      {renderTabContent()}
    </>
  );
};

export default CoursePanel;