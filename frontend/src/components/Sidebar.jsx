import React from 'react';

const Sidebar = ({
  filterOptions,
  selectedYear,
  setSelectedYear,
  selectedCampus,
  setSelectedCampus,
  selectedCourse,
  setSelectedCourse
}) => {
  
  const cursosDisponiveis = filterOptions?.cursosPorAnoECampus?.[selectedYear]?.[selectedCampus] || [];

  return (
    <aside className="bg-white shadow-md rounded-lg p-6">
      <h2 className="text-xl font-semibold text-gray-700 mb-4">Selecione sua Análise</h2>
      <div className="space-y-4">
        
        <div>
          <label htmlFor="ano-select" className="block text-lg font-medium text-gray-700">Ano</label>
          <select
            id="ano-select"
            className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 text-lg"
            value={selectedYear}
            onChange={(e) => setSelectedYear(e.target.value)}
            disabled={!filterOptions?.anos?.length}
          >
            <option value="">{filterOptions?.anos?.length ? 'Selecione um Ano' : 'Carregando...'}</option>
            {filterOptions?.anos?.map(year => (
              <option key={year} value={year}>{year}</option>
            ))}
          </select>
        </div>

        <div>
          <label htmlFor="campus-select" className="block text-lg font-medium text-gray-700">Campus</label>
          <select
            id="campus-select"
            className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 text-lg"
            value={selectedCampus}
            onChange={(e) => setSelectedCampus(e.target.value)}
            disabled={!filterOptions?.campi?.length}
          >
            <option value="">{filterOptions?.campi?.length ? 'Selecione um Campus' : 'Carregando...'}</option>
            {filterOptions?.campi?.map(campus => (
              <option key={campus} value={campus}>{campus}</option>
            ))}
          </select>
        </div>

        <div>
          <label htmlFor="curso-select" className="block text-lg font-medium text-gray-700">Curso</label>
          <select
            id="curso-select"
            className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 text-lg disabled:bg-gray-200"
            value={selectedCourse}
            onChange={(e) => setSelectedCourse(e.target.value)}
            disabled={!selectedYear || !selectedCampus}
          >
            <option value="">Selecione um Curso</option>
            {cursosDisponiveis.length === 0 && selectedYear && selectedCampus && (
              <option value="" disabled>Nenhum curso avaliado neste ano/campus</option>
            )}
            {cursosDisponiveis.map(curso => (
              <option key={curso.codigo} value={curso.codigo}>{curso.nome}</option>
            ))}
          </select>
        </div>
        
      </div>
    </aside>
  );
};

export default Sidebar;