import React, { useState, useEffect, useCallback } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import Tabs from './components/Tabs';
import CoursePanel from './components/CoursePanel/CoursePanel';
import { getFilterOptions, getVisaoGeralData } from './services/enadeService';

const App = () => {
  const [filterOptions, setFilterOptions] = useState(null);

  const [selectedYear, setSelectedYear] = useState('');
  const [selectedCampus, setSelectedCampus] = useState('');
  const [selectedCourse, setSelectedCourse] = useState('');

  const [activeTab, setActiveTab] = useState('visao-geral');

  const [visaoGeralData, setVisaoGeralData] = useState(null);
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    getFilterOptions()
      .then(options => {
        setFilterOptions(options);
        if (options?.anos?.length > 0) {
          setSelectedYear(options.anos[0]);
        }
      })
      .catch(err => {
        console.error("Erro ao carregar filtros:", err);
        setError("Não foi possível carregar as opções de filtro.");
      });
  }, []);

  useEffect(() => {
    if (selectedYear && selectedCampus && selectedCourse) {
      setLoading(true);
      setError(null);
      setVisaoGeralData(null);

      getVisaoGeralData(selectedCampus, selectedYear)
        .then(cursosDoAno => {
          const dadosDoCurso = cursosDoAno.find(c => c.CO_CURSO == selectedCourse);
          if (dadosDoCurso) {
            setVisaoGeralData(dadosDoCurso);
          } else {
            setError("Dados não encontrados para este curso neste ano.");
          }
        })
        .catch(err => {
          console.error("Erro ao buscar dados da visão geral:", err);
          setError("Falha ao carregar os dados de análise.");
        })
        .finally(() => {
          setLoading(false);
        });
    }
  }, [selectedYear, selectedCampus, selectedCourse]);

  useEffect(() => {
    setSelectedCourse('');
    setVisaoGeralData(null);
  }, [selectedYear, selectedCampus]);

  return (
    <div className=" bg-gray-100 font-sans text-gray-800 p-4 sm:p-6">
      <Header />
      <div className="flex flex-col lg:flex-row gap-4">
        <Sidebar
          filterOptions={filterOptions}
          selectedYear={selectedYear}
          setSelectedYear={setSelectedYear}
          selectedCampus={selectedCampus}
          setSelectedCampus={setSelectedCampus}
          selectedCourse={selectedCourse}
          setSelectedCourse={setSelectedCourse}
        />
        <main className="flex-1 bg-white shadow rounded-lg p-6">
          {!selectedCourse ? (
            <div className="flex flex-col items-center justify-center min-h-full gap-4 text-gray-500">
              <p className="text-2xl">Bem-vindo(a)!</p>
              <p className="text-lg">Selecione o Ano, Campus e Curso na barra lateral para começar.</p>
            </div>
          ) : (
            <>
              <Tabs activeTab={activeTab} setActiveTab={setActiveTab} />
              
              {loading && <p className="text-center mt-4 text-blue-600">Carregando dados...</p>}
              {error && <p className="text-center mt-4 text-red-600">{error}</p>}

              {visaoGeralData && (
                <CoursePanel
                  key={selectedCourse}
                  courseId={selectedCourse}
                  visaoGeralData={visaoGeralData}
                  activeTab={activeTab}
                  selectedYear={selectedYear}
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