import React from 'react';
import VisaoGeral from './components/VisaoGeral';
import EvolucaoHistorica from './components/EvolucaoHistorica';
import DesempenhoTopico from './components/DesempenhoTopico';
import AnalisePerfil from './components/AnalisePerfil';

const CoursePanel = ({
  courseId,
  courseData,
  currentYearData,
  activeTab,
  selectedYear,
  loadingLlm
}) => (
  <div className="mb-8">
    <h2 className="text-2xl font-bold text-indigo-700 mb-4">{courseData.nome} - Dados do ENADE {selectedYear}</h2>
    {activeTab === 'visao-geral' && <VisaoGeral currentYearData={currentYearData} />}
    {activeTab === 'evolucao-historica' && <EvolucaoHistorica historico={courseData.historico} />}
    {activeTab === 'desempenho-topico' && (
      <DesempenhoTopico
        desempenhoTopico={courseData.desempenhoTopico}
        currentYearData={currentYearData}
        loadingLlm={loadingLlm}
      />
    )}
    {activeTab === 'analise-perfil' && <AnalisePerfil perfilAluno={courseData.perfilAluno} />}
  </div>
);

export default CoursePanel;