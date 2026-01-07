import React, { useMemo } from 'react';
import VisaoGeral from './components/VisaoGeral';
import PercepcaoCurso from './components/PercepcaoCurso';
import EvolucaoHistorica from './components/EvolucaoHistorica';
import DesempenhoTopico from './components/DesempenhoTopico';

const CoursePanel = ({ selectedCourse, visaoGeralData, desempenhoTopicoData, activeTab, evolucaoHistorica, perfilConsolidadoData }) => {
  if (!visaoGeralData) {
    return (
      <div className="border-t pt-4 mt-4 first:mt-0 first:pt-0 first:border-0">
        <h3 className="text-xl font-semibold text-gray-600 mb-4">Carregando dados...</h3>
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
         return <DesempenhoTopico historicalDesempData={desempenhoTopicoData} idCourse={selectedCourse}/>;
        
      case 'percepcao-curso':
         return <PercepcaoCurso perfilData={perfilConsolidadoData} selectedYear={2021} />;

      default:
        return <div>Selecione uma aba válida</div>;
    }
  };

  return (
    <div className="space-y-6 py-6">
      <div className="bg-white border-l-4 border-indigo-600 rounded-r-xl shadow-sm p-6 flex items-center justify-between group hover:shadow-md transition-shadow">
        <div>
           <span className="text-2xs font-bold text-gray-400 uppercase tracking-wider">
             Curso Selecionado
           </span>
           <h3 className="text-2xl sm:text-3xl font-bold text-gray-800 mt-1 flex items-center gap-3">
             {courseName}
           </h3>
        </div>
        
        <div className="hidden sm:block p-3 bg-indigo-50 rounded-full text-indigo-600">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M4.26 10.147a60.438 60.438 0 0 0-.491 6.347A48.62 48.62 0 0 1 12 20.904a48.62 48.62 0 0 1 8.232-4.41 60.46 60.46 0 0 0-.491-6.347m-15.482 0a50.636 50.636 0 0 0-2.658-.813A59.906 59.906 0 0 1 12 3.493a59.903 59.903 0 0 1 10.399 5.84c-.896.248-1.783.52-2.658.814m-15.482 0A50.717 50.717 0 0 1 12 13.489a50.702 50.702 0 0 1 7.74-3.342M6.75 15a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm0 0v-3.675A55.378 55.378 0 0 1 12 8.443m-7.007 11.55A5.981 5.981 0 0 0 6.75 15.75v-1.5" />
        </svg>
        </div>
      </div>

      <div className="bg-white rounded-2xl p-1"> 
         {renderTabContent()}
      </div>
      
    </div>
  );
};

export default CoursePanel;