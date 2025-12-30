import React from 'react';

const YearSelector = ({ years, selectedYear, onChange }) => {
  if (!years || years.length === 0) return null;

  return (
    <div className="flex justify-center items-center mb-6 animate-in fade-in slide-in-from-top-2 duration-500">
      <div className="flex items-center space-x-3 bg-gray-50 px-3 py-2 rounded-lg border border-gray-200 shadow-sm">
        <span className="text-lg font-semibold text-gray-600">Ano da Edição:</span>
        <select
          value={selectedYear}
          onChange={(e) => onChange(e.target.value)}
          className="bg-white border border-gray-300 text-gray-700 text-lg rounded focus:ring-indigo-500 focus:border-indigo-500 block p-1 font-bold cursor-pointer transition-colors hover:border-indigo-400"
        >
          {years.map((year) => (
            <option key={year} value={year}>
              {year}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
};

export default YearSelector;