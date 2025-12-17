import React from 'react';

const Sidebar = ({
  filterOptions,
  selectedCampus,
  setSelectedCampus,
  selectedCourse,
  setSelectedCourse,
  availableCourses
}) => {
  
  return (
    <aside className="bg-white w-full shadow-md rounded-lg p-6">
      <h2 className="text-xl font-semibold text-gray-700 mb-4">Selecione sua Análise</h2>
      <div className="flex flex-row gap-10">
        
        <div>
          <label htmlFor="campus-select" className="block text-lg font-medium text-gray-700">Campus</label>
          <select
            id="campus-select"
            className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 text-lg"
            value={selectedCampus}
            onChange={(e) => {
              setSelectedCampus(e.target.value);
              setSelectedCourse('');
            }}
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
            className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 text-lg disabled:bg-gray-100"
            value={selectedCourse}
            onChange={(e) => {
              setSelectedCourse(e.target.value)}
            }
            disabled={!selectedCampus || !availableCourses?.length}
          >
            <option value="">Selecione um Curso</option>
            
            {selectedCampus && availableCourses?.length === 0 && (
               <option value="" disabled>Nenhum curso encontrado</option>
            )}

            {availableCourses?.map(curso => (
              <option key={curso.codigo} value={curso.codigo}>{curso.nome}</option>
            ))}
          </select>
        </div>
        
      </div>
    </aside>
  );
};

export default Sidebar;