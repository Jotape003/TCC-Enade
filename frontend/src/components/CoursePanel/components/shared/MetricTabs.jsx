import React from 'react';

const MetricTabs = ({ activeTab, onChange, options }) => {
  return (
    <div className="flex w-auto">
      <div className="flex items-center gap-2 px-2 py-1.5 bg-gray-100/80 backdrop-blur-sm border border-gray-200 rounded-full shadow-inner">
        {options.map((option) => {
          const isActive = activeTab === option.value;

          return (
            <button
              key={option.value}
              onClick={() => onChange(option.value)}
              className={`
                flex items-center gap-2 px-6 py-2 cursor-pointer rounded-full font-semibold
                transition-all duration-300 ease-out whitespace-nowrap
                focus:outline-none
                ${isActive
                  ? 'bg-indigo-600 text-white scale-105'
                  : 'bg-transparent text-gray-600 hover:bg-white hover:text-indigo-600 hover:shadow-sm'
                }
              `}
            >
              {option.icon && (
                <svg
                  className={`w-4 h-4 ${
                    isActive ? 'fill-amber-50' : 'fill-current'
                  }`}
                  viewBox="0 0 20 20"
                >
                  <path d={option.icon} />
                </svg>
              )}

              {option.label}
            </button>
          );
        })}
      </div>
    </div>
  );
};

export default MetricTabs;
