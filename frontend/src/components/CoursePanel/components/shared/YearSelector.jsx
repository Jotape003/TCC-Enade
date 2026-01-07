import React from 'react';

const YearSelector = ({ years, selectedYear, onChange }) => {
  const sortedYears = [...(years || [])].sort((a, b) => a - b);

  if (!sortedYears.length) return null;

  return (
    <div className="flex flex-wrap items-center gap-2 p-1.5 bg-gray-50 border border-gray-100 rounded-xl w-fit mx-auto sm:mx-0 shadow-inner">
      <span className=" font-semibold text-gray-500 uppercase tracking-wider px-3 hidden sm:block">
        Edição:
      </span>
      
      {sortedYears.map((year) => {
        const isSelected = selectedYear === year;
        
        return (
          <button
            key={year}
            onClick={() => onChange(year)}
            className={`
              relative px-4 py-1.5 cursor-pointer rounded-xl font-semibold transition-all duration-300 ease-out
              focus:outline-none
              ${isSelected 
                ? 'bg-indigo-600 text-white scale-105' 
                : 'bg-transparent text-gray-600 hover:bg-white hover:text-indigo-600 hover:shadow-sm'
              }
            `}
          >
            {year}
          </button>
        );
      })}
    </div>
  );
};

export default YearSelector;