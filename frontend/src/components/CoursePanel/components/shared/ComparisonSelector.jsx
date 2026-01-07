import React from 'react';

const DEFAULT_OPTIONS = [
  { key: 'brasil', label: 'Brasil', color: '#FF7B00' },
  { key: 'regiao', label: 'Região', color: '#0A5C36' },
  { key: 'ceara', label: 'Ceará', color: '#FFE745' },
  { key: 'ufc', label: 'UFC (Área)', color: '#E70000' },
];

const ComparisonSelector = ({ comparisonState, onToggle }) => {
  return (
    <div className="flex flex-col sm:flex-row items-center gap-4">
      <span className="text-sm font-bold text-gray-500 uppercase tracking-wider">
        Comparar com:
      </span>
      
      <div className="flex flex-wrap justify-center gap-3">
        {DEFAULT_OPTIONS.map(({ key, label, color }) => {
          const isActive = comparisonState[key];

          return (
            <button
              key={key}
              onClick={() => onToggle(key, !isActive)}
              className={`
                group flex items-center cursor-pointer gap-2 px-4 py-2 rounded-full text-sm font-bold transition-all duration-200 border-2
                ${isActive ? 'shadow-sm' : 'bg-transparent border-gray-300 text-gray-500 hover:border-gray-300'}
              `}
              style={isActive ? {
                backgroundColor: `${color}15`,
                borderColor: color,
                color: color
              } : {}}
            >
              <span 
                className={`w-3 h-3 rounded-full transition-colors`}
                style={{ backgroundColor: color }}
              />
              {label}
            </button>
          );
        })}
      </div>
    </div>
  );
};

export default ComparisonSelector;