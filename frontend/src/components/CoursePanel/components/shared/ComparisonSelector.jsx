import React from 'react';

const DEFAULT_OPTIONS = [
  { key: 'ufc', label: 'UFC (Área)', color: '#E70000' },
  { key: 'brasil', label: 'Brasil', color: '#FF7B00' },
  { key: 'regiao', label: 'Região', color: '#0A5C36' },
  { key: 'ceara', label: 'Ceará', color: '#FFE745' }
];

const ComparisonSelector = ({ comparisonState, onToggle }) => {
  const handleChange = (e) => {
    const { name, checked } = e.target;
    onToggle(name, checked);
  };

  return (
    <div className="flex flex-col sm:flex-row justify-center items-center space-y-2 sm:space-y-0 sm:space-x-7 mb-6">
      <h4 className="text-lg font-semibold text-gray-700">Comparar com:</h4>
      <div className="flex flex-wrap justify-center gap-4">
        {DEFAULT_OPTIONS.map(({ key, label, color }) => (
          <label key={key} className="flex items-center space-x-2 cursor-pointer hover:bg-gray-50 p-1 rounded transition-colors">
            <input
              type="checkbox"
              name={key}
              checked={comparisonState[key]}
              onChange={handleChange}
              className="form-checkbox h-5 w-5 rounded cursor-pointer border-gray-300 text-indigo-600 focus:ring-indigo-500"
              style={{ accentColor: color }}
            />
            <span className="text-gray-700 font-medium">{label}</span>
          </label>
        ))}
      </div>
    </div>
  );
};

export default ComparisonSelector;