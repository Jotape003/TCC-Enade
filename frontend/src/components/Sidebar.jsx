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
    <aside className="bg-white w-full shadow-xl shadow-gray-200/50 rounded-2xl p-6 border border-gray-100 transition-all duration-300 hover:shadow-2xl hover:shadow-gray-200/60">
      <h2 className="text-xl font-bold text-gray-800 mb-6 flex items-center gap-2">
        <span className="w-1 h-6 bg-indigo-600 rounded-full"></span>
        Selecione sua Análise
      </h2>
      
      <div className="flex flex-col text-lg md:flex-row gap-6">
        
        <div className="flex-1">
          <label htmlFor="campus-select" className="block text-sm font-semibold text-gray-600 mb-2 uppercase tracking-wide">Campus</label>
          <div className="relative">
            <select
              id="campus-select"
              className="appearance-none w-full p-3 pl-4 pr-10 bg-gray-50 border border-gray-200 rounded-xl text-gray-700 font-medium focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 focus:rounded-b-none transition-all cursor-pointer hover:bg-gray-100"
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
            <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-4 text-gray-500">
              <svg className="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
            </div>
          </div>
        </div>

        <div className="flex-2">
          <label htmlFor="curso-select" className="block text-sm font-semibold text-gray-600 mb-2 uppercase tracking-wide">Curso</label>
          <div className="relative">
            <select
              id="curso-select"
              className="appearance-none w-full p-3 pl-4 pr-10 bg-gray-50 border border-gray-200 rounded-xl text-gray-700 font-medium focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 focus:rounded-b-none transition-all cursor-pointer disabled:bg-gray-100 disabled:text-gray-400 disabled:cursor-not-allowed hover:enabled:bg-gray-100"
              value={selectedCourse}
              onChange={(e) => setSelectedCourse(e.target.value)}
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
            <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-4 text-gray-500">
              <svg className="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
            </div>
          </div>
        </div>
        
      </div>
    </aside>
  );
};

export default Sidebar;