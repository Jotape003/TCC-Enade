import React, { useState, useEffect, useMemo } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import Tabs from './components/Tabs';

import CoursePanel from './components/CoursePanel/CoursePanel';

import { 
  getFilterOptions, 
  getVisaoGeralData, 
  getDesempenhoTopicoData, 
  getEvolucaoHistorica,
  getPerfilConsolidado
} from './services/enadeService';
import { useEnadeData } from './hooks/useEnadeData';

const App = () => {
  const [filterOptions, setFilterOptions] = useState(null);
  
  const [selectedCampus, setSelectedCampus] = useState('');
  const [selectedCourse, setSelectedCourse] = useState('');
  const [activeTab, setActiveTab] = useState('visao-geral');

  const { visaoGeral, desempenhoTopico, evolucaoHistorica, perfilConsolidado, loading, error } = useEnadeData(selectedCampus, selectedCourse);

  useEffect(() => {
    getFilterOptions()
      .then(options => setFilterOptions(options))
      .catch(err => {
        console.error("Erro filtros:", err);
        setError("Erro ao carregar filtros.");
      });
  }, []);

  const availableCourses = useMemo(() => {
    if (!filterOptions || !selectedCampus) return [];
    const uniqueCourses = new Map();

    if (filterOptions.cursosPorAnoECampus) {
      Object.values(filterOptions.cursosPorAnoECampus).forEach(yearData => {
        const coursesInYear = yearData[selectedCampus] || [];
        coursesInYear.forEach(course => {
          if (!uniqueCourses.has(course.codigo)) {
            uniqueCourses.set(course.codigo, course);
          }
        });
      });
    }
    
    return Array.from(uniqueCourses.values()).sort((a, b) => a.nome.localeCompare(b.nome));
  }, [filterOptions, selectedCampus]);

  return (
    <div className="bg-gray-100 font-sans text-gray-800 p-4 sm:p-6 flex flex-col gap-4 min-h-screen">
      <div className="flex flex-col gap-4">
        <div className='flex flex-row justify-between gap-4'>
          <Sidebar
            filterOptions={filterOptions}
            selectedCampus={selectedCampus}
            setSelectedCampus={setSelectedCampus}
            selectedCourse={selectedCourse}
            setSelectedCourse={setSelectedCourse}
            availableCourses={availableCourses}
          />
          <Header />
        
        </div>
        <main className="flex-1 bg-white shadow rounded-lg py-2 px-6 h-full min-h-[500px]">
          {!selectedCourse ? (
            <div className="flex flex-col items-center justify-center gap-4 text-gray-500 h-64">
              <p className="text-2xl">Bem-vindo(a)!</p>
              <p className="text-lg">Selecione o Campus e Curso acima para começar.</p>
            </div>
          ) : (
            <>
              <Tabs activeTab={activeTab} setActiveTab={setActiveTab} />
              
              {loading && (
                <div className="text-center mt-10 text-indigo-600">
                  <span className="loading-spinner"></span> Carregando dados históricos...
                </div>
              )}
              {error && <p className="text-center mt-4 text-red-600">{error}</p>}

              {!loading && visaoGeral && (
                <CoursePanel
                  visaoGeralData={visaoGeral}
                  desempenhoTopicoData={desempenhoTopico} 
                  evolucaoHistorica={evolucaoHistorica}
                  perfilConsolidadoData={perfilConsolidado}
                  activeTab={activeTab}
                />
              )}
            </>
          )}
        </main>
      </div>
    </div>
  );
};

export default App;