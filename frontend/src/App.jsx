import React, { useState, useEffect, useMemo } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import Tabs from './components/Tabs';

import CoursePanel from './components/CoursePanel/CoursePanel';

// Import services
import { 
  getFilterOptions, 
  getVisaoGeralData, 
  getDesempenhoTopicoData, 
  getEvolucaoHistorica 
} from './services/enadeService';

const App = () => {
  const [filterOptions, setFilterOptions] = useState(null);
  
  // Estado: Apenas Campus e Curso (Ano agora é local das abas)
  const [selectedCampus, setSelectedCampus] = useState('');
  const [selectedCourse, setSelectedCourse] = useState('');
  const [activeTab, setActiveTab] = useState('visao-geral');

  // Estados de Dados (Histórico Completo)
  const [visaoGeralData, setVisaoGeralData] = useState(null);
  const [desempenhoTopicoData, setDesempenhoTopicoData] = useState(null);
  const [evolucaoHistoricaData, setEvolucaoHistoricaData] = useState(null);
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // 1. Carregar Opções de Filtro
  useEffect(() => {
    getFilterOptions()
      .then(options => setFilterOptions(options))
      .catch(err => {
        console.error("Erro filtros:", err);
        setError("Erro ao carregar filtros.");
      });
  }, []);

  // 2. Lógica para extrair cursos únicos do Campus (independente do ano)
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

  // 3. Buscar Dados Consolidados quando Campus/Curso mudam
  useEffect(() => {
    if (selectedCampus && selectedCourse) {
      const fetchData = async () => {
        setLoading(true);
        setError(null);
        try {
          // Promise.all para buscar os 3 arquivos consolidados de uma vez
          const [vg, dt, eh] = await Promise.all([
            getVisaoGeralData(selectedCampus, selectedCourse),
            getDesempenhoTopicoData(selectedCampus, selectedCourse),
            getEvolucaoHistorica(selectedCampus, selectedCourse)
          ]);

          setVisaoGeralData(vg);
          setDesempenhoTopicoData(dt);
          setEvolucaoHistoricaData(eh);

        } catch (err) {
          console.error("Erro fetch:", err);
          setError("Falha ao carregar dados do curso.");
        } finally {
          setLoading(false);
        }
      };

      fetchData();
    } else {
      // Limpa dados se deselecionar
      setVisaoGeralData(null);
      setDesempenhoTopicoData(null);
      setEvolucaoHistoricaData(null);
    }
  }, [selectedCampus, selectedCourse]);

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

              {!loading && visaoGeralData && (
                <CoursePanel
                  visaoGeralData={visaoGeralData}
                  desempenhoTopicoData={desempenhoTopicoData} 
                  evolucaoHistorica={evolucaoHistoricaData}
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