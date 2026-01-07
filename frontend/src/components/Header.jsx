import React from 'react';

const Header = () => (
  <header className="relative w-full bg-indigo-700 shadow-md rounded-2xl p-8 overflow-hidden">
    <div className="absolute top-0 right-0 w-64 h-64 bg-white opacity-5 rounded-full -mr-20 -mt-20"></div>
    <div className="absolute bottom-0 left-0 w-32 h-32 bg-indigo-500 opacity-20 rounded-full -ml-10 -mb-10"></div>

    <div className="relative z-10 flex flex-col items-center justify-center text-center">

      <h1 className="text-3xl sm:text-5xl text-white font-medium tracking-tight flex flex-col sm:flex-row items-center gap-2 sm:gap-4">
        <span>Observatório</span>
        
        <span className="bg-white/10 border border-white/20 px-4 py-1 rounded-lg font-bold shadow-sm backdrop-blur-sm">
          ENADE
        </span>

        <span className="hidden sm:inline text-indigo-400 font-light">|</span>
        <span className="font-light opacity-90">UFC</span>
      </h1>
      
      <p className="mt-4 text-indigo-100 text-sm sm:text-base font-normal max-w-2xl mx-auto border-t border-indigo-200/50 pt-2">
        Uma ferramenta para visualização do desempenho dos cursos da UFC Quixadá no ENADE
      </p>
    </div>
  </header>
);

export default Header;