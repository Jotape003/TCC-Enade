import React from 'react';

const MetricTabs = ({ activeTab, onChange, options }) => {
  return (
    <div className="flex justify-center bg-gray-50 p-4 space-x-4 rounded-lg mb-6 overflow-x-auto">
      {options.map((option) => (
        <button
          key={option.value}
          onClick={() => onChange(option.value)}
          className={`px-4 py-2 rounded-md text-lg font-medium transition-all cursor-pointer whitespace-nowrap ${
            activeTab === option.value
              ? 'bg-white text-indigo-600 shadow-sm ring-1 ring-gray-200'
              : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          {option.label}
        </button>
      ))}
    </div>
  );
};

export default MetricTabs;