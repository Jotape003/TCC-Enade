import React from 'react';

const Sidebar = ({ mockData, selectedCourses, handleCourseChange }) => (
  <aside className="bg-white shadow-md rounded-lg p-6 lg:w-1/4">
    <h2 className="text-xl font-semibold text-gray-700 mb-4">Selecione o(s) Curso(s) para Análise</h2>
    <div className="space-y-3">
      {Object.keys(mockData).map((courseId) => (
        <label key={courseId} className="flex items-center space-x-2 text-lg cursor-pointer">
          <input
            type="checkbox"
            value={courseId}
            checked={selectedCourses.includes(courseId)}
            onChange={handleCourseChange}
            className="form-checkbox h-5 w-5 text-indigo-600 rounded focus:ring-indigo-500"
          />
          <span>{mockData[courseId].nome}</span>
        </label>
      ))}
    </div>
    {selectedCourses.length > 0 && (
      <p className="mt-4 text-sm text-gray-500">
        {selectedCourses.map(id => mockData[id].nome).join(', ')} selecionado(s).
      </p>
    )}
  </aside>
);

export default Sidebar;