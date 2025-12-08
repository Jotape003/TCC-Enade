import React, { useState, useEffect, useCallback } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import Tabs from './components/Tabs';
import CoursePanel from './components/CoursePanel/CoursePanel';
import { getFilterOptions, getVisaoGeralData, getDesempenhoTopicoData, getEvolucaoHistorica} from './services/enadeService';

const App = () => {
  const [filterOptions, setFilterOptions] = useState(null);

  const [selectedYear, setSelectedYear] = useState('');
  const [selectedCampus, setSelectedCampus] = useState('');
  const [selectedCourse, setSelectedCourse] = useState('');

  const [activeTab, setActiveTab] = useState('visao-geral');

  const [visaoGeralData, setVisaoGeralData] = useState(null);
  const [componenteEspecificoData, setComponenteEspecificoData] = useState(null);
  const [formacaoGeralData, setFormacaoGeralData] = useState(null);
  const [historicoData, setHistoricoData] = useState(null);
  
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
      setComponenteEspecificoData(null);

      const fetchData = async () => {
        try {
          const p1 = getVisaoGeralData(selectedCampus, selectedYear, selectedCourse);
          const p2 = getDesempenhoTopicoData(selectedCampus, selectedYear, selectedCourse);
          const p3 = getEvolucaoHistorica(selectedCampus, selectedCourse);

          const [visGeralAnual, compDataAnual, eHistoricoData] = await Promise.all([p1, p2, p3]);

          if (visGeralAnual) {
            setVisaoGeralData(visGeralAnual);
          } else {
            setError("Dados de Visão Geral não encontrados");
          }

          if (compDataAnual) {
            setComponenteEspecificoData(compDataAnual.desempenho_CE);
            setFormacaoGeralData(compDataAnual.desempenho_FG);
          } else {
            console.warn(`Dados de desempenho por tópico não encontrados para ${selectedCourse} em ${selectedYear}`);
          }
          
          if (eHistoricoData) {
            setHistoricoData(eHistoricoData);
          } else {
            console.warn('Dados de evolução histórica não encontrados.');
          }
        } catch (err) {
          console.error("Erro ao buscar dados de análise:", err);
          setError("Falha ao carregar os dados de análise.");
        } finally {
          setLoading(false);
        }
      };

      fetchData();
    }
  }, [selectedYear, selectedCampus, selectedCourse]);

  useEffect(() => {
    setSelectedCourse('');
    setVisaoGeralData(null);
    setComponenteEspecificoData(null);
    setFormacaoGeralData(null);
  }, [selectedYear, selectedCampus]);

  return (
    <div className=" bg-gray-100 font-sans text-gray-800 p-4 sm:p-6 flex flex-col gap-4 min-h-screen">
      <Header />
      <div className="flex flex-col gap-4">
        <Sidebar
          filterOptions={filterOptions}
          selectedYear={selectedYear}
          setSelectedYear={setSelectedYear}
          selectedCampus={selectedCampus}
          setSelectedCampus={setSelectedCampus}
          selectedCourse={selectedCourse}
          setSelectedCourse={setSelectedCourse}
        />
        <main className="flex-1 bg-white shadow rounded-lg py-2 px-6 h-full">
          {!selectedCourse ? (
            <div className="flex flex-col items-center justify-center gap-4 text-gray-500">
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
                  componenteEspecificoData={componenteEspecificoData}
                  formacaoGeralData={formacaoGeralData}
                  evolucaoHistorica={historicoData}
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