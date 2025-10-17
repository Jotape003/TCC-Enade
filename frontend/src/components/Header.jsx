import React from 'react';

const Header = ({ selectedYear, setSelectedYear }) => (
  <header className="bg-white shadow-md rounded-lg p-4 mb-6 flex flex-col sm:flex-row items-center justify-between">
    <h1 className="text-2xl sm:text-3xl font-bold text-indigo-700 mb-2 sm:mb-0">ENADE Insights - UFC</h1>
    <div className="flex items-center space-x-4">
      <span className="text-lg">Olá, Coordenador(a)!</span>
      <select
        className="p-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"
        value={selectedYear}
        onChange={(e) => setSelectedYear(e.target.value)}
      >
        <option value="2014">2014</option>
        <option value="2017">2017</option>
        <option value="2021">2021</option>
      </select>
    </div>
  </header>
);

export default Header;