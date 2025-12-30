import React from 'react';

const colorVariants = {
  blue: {
    active: 'bg-blue-200 ring-2 ring-blue-400',
    inactive: 'bg-blue-100 hover:bg-blue-200',
    textTitle: 'text-blue-700',
    textValue: 'text-blue-900',
  },
  green: {
    active: 'bg-green-200 ring-2 ring-green-400',
    inactive: 'bg-green-100 hover:bg-green-200',
    textTitle: 'text-green-700',
    textValue: 'text-green-900',
  },
  yellow: {
    active: 'bg-yellow-200 ring-2 ring-yellow-400',
    inactive: 'bg-yellow-100 hover:bg-yellow-200',
    textTitle: 'text-yellow-700',
    textValue: 'text-yellow-900',
  },
  gray: {
    active: 'bg-gray-200',
    inactive: 'bg-gray-200', 
    textTitle: 'text-gray-700',
    textValue: 'text-gray-900',
  }
};

const StatCard = ({ label, value, color, isActive = false, onClick = null }) => {
  const theme = colorVariants[color];
  const baseClasses = `p-4 rounded-lg shadow transition-colors flex flex-col items-center justify-center h-full cursor-${onClick ? 'pointer' : 'default'}`;
  const stateClasses = isActive ? theme.active : theme.inactive;

  return (
    <div 
      className={`${baseClasses} ${onClick ? stateClasses : theme.inactive}`}
      onClick={onClick}
    >
      <p className={`text-lg font-semibold ${theme.textTitle} text-center`}>{label}</p>
      <p className={`text-3xl font-bold ${theme.textValue} mt-2`}>
        {value !== undefined && value !== null ? value : '-'}
      </p>
    </div>
  );
};

export default StatCard;