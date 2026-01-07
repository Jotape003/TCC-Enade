import React from 'react';

const colorVariants = {
  blue: {
    container: 'bg-gradient-to-br from-blue-50 to-blue-100 border-blue-200 hover:shadow-blue-200/50',
    activeRing: 'ring-2 ring-blue-500',
    textTitle: 'text-blue-600',
    textValue: 'text-blue-900',
  },
  yellow: {
    container: 'bg-gradient-to-br from-amber-50 to-amber-100 border-amber-200 hover:shadow-amber-200/50',
    activeRing: 'ring-2 ring-amber-500 shadow-amber-200',
    textTitle: 'text-amber-600',
    textValue: 'text-amber-900',
  },
  green: {
    container: 'bg-gradient-to-br from-emerald-50 to-emerald-100 border-emerald-200 hover:shadow-emerald-200/50',
    activeRing: 'ring-2 ring-emerald-500 shadow-emerald-200',
    textTitle: 'text-emerald-600',
    textValue: 'text-emerald-900',
  },
  gray: {
    container: 'bg-gradient-to-br from-gray-50 to-gray-100 border-gray-200 hover:shadow-gray-200/50',
    activeRing: 'ring-2 ring-gray-400',
    textTitle: 'text-gray-500',
    textValue: 'text-gray-800',
  }
};

const StatCard = ({ label, value, color, isActive = false, onClick = null }) => {
  const theme = colorVariants[color];
  
  // Base classes para estrutura e transições
  const baseClasses = `
    relative overflow-hidden p-5 rounded-2xl border transition-all duration-300 ease-out 
    flex flex-col items-center justify-center h-full 
    ${onClick ? 'cursor-pointer hover:-translate-y-1' : 'cursor-default'}
    ${theme.container}
  `;

  // Classes condicionais para estado ativo
  const activeClasses = isActive ? theme.activeRing : 'shadow-sm hover:shadow-md';

  return (
    <div 
      className={`${baseClasses} ${activeClasses}`}
      onClick={onClick}
    >
      <div className={`absolute -top-10 -right-10 w-24 h-24 rounded-full opacity-10 bg-current ${theme.textTitle}`}></div>
      
      <p className={`text-sm font-bold uppercase tracking-wider mb-1 z-10 ${theme.textTitle} text-center`}>
        {label}
      </p>
      
      <p className={`text-4xl font-extrabold z-10 ${theme.textValue} mt-1`}>
        {value !== undefined && value !== null ? value : '-'}
      </p>
    </div>
  );
};

export default StatCard;