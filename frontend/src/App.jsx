import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import Tabs from './components/Tabs';
import CoursePanel from './components/CoursePanel/CoursePanel';

const mockData = {
  'CC': {
    nome: 'Ciência da Computação',
    historico: [
      { ano: 2014, mediaFG: 50, mediaCE: 60, taxaParticipacao: 80 },
      { ano: 2017, mediaFG: 55, mediaCE: 68, taxaParticipacao: 85 },
      { ano: 2021, mediaFG: 62, mediaCE: 75, taxaParticipacao: 92 },
    ],
    comparativoAtual: {
      ano: 2021,
      mediaFG: 62,
      mediaCE: 75,
      mediaNacionalFG: 58,
      mediaNacionalCE: 70,
      mediaUFCQuixadaFG: 60,
      mediaUFCQuixadaCE: 72,
    },
    desempenhoTopico: [
      { topico: 'Estruturas de Dados', curso: 60, nacional: 75, fullMark: 100 },
      { topico: 'Algoritmos', curso: 85, nacional: 80, fullMark: 100 },
      { topico: 'Engenharia de Software', curso: 70, nacional: 70, fullMark: 100 },
      { topico: 'Redes de Computadores', curso: 55, nacional: 65, fullMark: 100 },
      { topico: 'Banco de Dados', curso: 78, nacional: 72, fullMark: 100 },
      { topico: 'Ética e Sociedade', curso: 50, nacional: 60, fullMark: 100 },
      { topico: 'Sistemas Operacionais', curso: 68, nacional: 70, fullMark: 100 },
      { topico: 'Inteligência Artificial', curso: 72, nacional: 75, fullMark: 100 },
    ],
    perfilAluno: {
      tipoEscola: [
        { categoria: 'Pública', cursoFG: 58, cursoCE: 65, nacionalFG: 60, nacionalCE: 70 },
        { categoria: 'Privada', cursoFG: 65, cursoCE: 78, nacionalFG: 62, nacionalCE: 75 },
      ],
      faixaRenda: [
        { categoria: 'Até 1 SM', cursoFG: 55, cursoCE: 60 },
        { categoria: '1-3 SM', cursoFG: 60, cursoCE: 70 },
        { categoria: 'Acima de 3 SM', cursoFG: 68, cursoCE: 80 },
      ],
      turno: [
        { categoria: 'Diurno', cursoFG: 63, cursoCE: 76 },
        { categoria: 'Noturno', cursoFG: 59, cursoCE: 70 },
      ],
    },
  },
  'ES': {
    nome: 'Engenharia de Software',
    historico: [
      { ano: 2014, mediaFG: 52, mediaCE: 62, taxaParticipacao: 82 },
      { ano: 2017, mediaFG: 57, mediaCE: 70, taxaParticipacao: 89 },
      { ano: 2021, mediaFG: 64, mediaCE: 78, taxaParticipacao: 95 },
    ],
    comparativoAtual: {
      ano: 2021,
      mediaFG: 64,
      mediaCE: 78,
      mediaNacionalFG: 58,
      mediaNacionalCE: 70,
      mediaUFCQuixadaFG: 60,
      mediaUFCQuixadaCE: 72,
    },
    desempenhoTopico: [
      { topico: 'Engenharia de Requisitos', curso: 75, nacional: 70, fullMark: 100 },
      { topico: 'Testes de Software', curso: 68, nacional: 72, fullMark: 100 },
      { topico: 'Arquitetura de Software', curso: 80, nacional: 75, fullMark: 100 },
      { topico: 'Gerenciamento de Projetos', curso: 60, nacional: 68, fullMark: 100 },
      { topico: 'Programação Web', curso: 72, nacional: 65, fullMark: 100 },
      { topico: 'Ética e Sociedade', curso: 55, nacional: 60, fullMark: 100 },
      { topico: 'Qualidade de Software', curso: 65, nacional: 68, fullMark: 100 },
      { topico: 'Interface e Usabilidade', curso: 70, nacional: 65, fullMark: 100 },
    ],
    perfilAluno: {
      tipoEscola: [
        { categoria: 'Pública', cursoFG: 60, cursoCE: 70, nacionalFG: 60, nacionalCE: 70 },
        { categoria: 'Privada', cursoFG: 67, cursoCE: 80, nacionalFG: 62, nacionalCE: 75 },
      ],
      faixaRenda: [
        { categoria: 'Até 1 SM', cursoFG: 58, cursoCE: 65 },
        { categoria: '1-3 SM', cursoFG: 63, cursoCE: 75 },
        { categoria: 'Acima de 3 SM', cursoFG: 70, cursoCE: 82 },
      ],
      turno: [
        { categoria: 'Diurno', cursoFG: 65, cursoCE: 79 },
        { categoria: 'Noturno', cursoFG: 61, cursoCE: 72 },
      ],
    },
  },
};

const App = () => {
  const [selectedCourses, setSelectedCourses] = useState(
    JSON.parse(localStorage.getItem('selectedCourses')) || []
  );
  const [activeTab, setActiveTab] = useState(
    localStorage.getItem('activeTab') || 'visao-geral'
  );
  const [selectedYear, setSelectedYear] = useState(
    localStorage.getItem('selectedYear') || '2021'
  );

  const handleCourseChange = (event) => {
    const { value, checked } = event.target;
    if (checked) {
      setSelectedCourses((prev) => [...prev, value]);
    } else {
      setSelectedCourses((prev) => prev.filter((course) => course !== value));
    }
  };

  const getCourseData = (courseId) => mockData[courseId];
  const getCurrentYearData = (courseId) => getCourseData(courseId)?.comparativoAtual;

  useEffect(() => {
    localStorage.setItem('selectedCourses', JSON.stringify(selectedCourses));
  }, [selectedCourses]);

  useEffect(() => {
    localStorage.setItem('activeTab', activeTab);
  }, [activeTab]);

  useEffect(() => {
    localStorage.setItem('selectedYear', selectedYear);
  }, [selectedYear]);


  return (
    <div className="min-h-screen bg-gray-100 font-sans text-gray-800 p-4 sm:p-6">
      <Header selectedYear={selectedYear} setSelectedYear={setSelectedYear} />
      <div className="flex flex-col lg:flex-row gap-6">
        <Sidebar
          mockData={mockData}
          selectedCourses={selectedCourses}
          handleCourseChange={handleCourseChange}
        />
        <main className="flex-1 bg-white shadow-md rounded-lg p-6">
          {selectedCourses.length === 0 ? (
            <div className="text-center py-20 text-gray-500">
              <p className="text-2xl mb-4">👋 Bem-vindo(a)!</p>
              <p className="text-lg">Selecione um ou mais cursos na barra lateral para começar a analisar os dados do ENADE.</p>
            </div>
          ) : (
            <>
              <Tabs activeTab={activeTab} setActiveTab={setActiveTab} />
              {selectedCourses.map((courseId) => {
                const courseData = getCourseData(courseId);
                const currentYearData = getCurrentYearData(courseId);
                if (!courseData) return null;
                return (
                  <CoursePanel
                    key={courseId}
                    courseId={courseId}
                    courseData={courseData}
                    currentYearData={currentYearData}
                    activeTab={activeTab}
                    selectedYear={selectedYear}
                  />
                );
              })}
            </>
          )}
        </main>
      </div>
    </div>
  );
};

export default App;
