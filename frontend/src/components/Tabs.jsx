import React from 'react';

const Tabs = ({ activeTab, setActiveTab }) => (
  <div className="border-b border-gray-200 mb-6">
    <nav className="-mb-px flex space-x-8" aria-label="Tabs">
      <button
        onClick={() => setActiveTab('visao-geral')}
        className={`whitespace-nowrap py-3 px-1 border-b-2 font-medium text-lg cursor-pointer ${
          activeTab === 'visao-geral'
            ? 'border-indigo-500 text-indigo-600'
            : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
        }`}
      >
        Visão Geral e Comparativo
      </button>
      <button
        onClick={() => setActiveTab('evolucao-historica')}
        className={`whitespace-nowrap py-3 px-1 border-b-2 font-medium text-lg cursor-pointer ${
          activeTab === 'evolucao-historica'
            ? 'border-indigo-500 text-indigo-600'
            : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
        }`}
      >
        Evolução Histórica
      </button>
      <button
        onClick={() => setActiveTab('desempenho-topico')}
        className={`whitespace-nowrap py-3 px-1 border-b-2 font-medium text-lg cursor-pointer ${
          activeTab === 'desempenho-topico'
            ? 'border-indigo-500 text-indigo-600'
            : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
        }`}
      >
        Desempenho por Tópico
      </button>
      <button
        onClick={() => setActiveTab('analise-perfil')}
        className={`whitespace-nowrap py-3 px-1 border-b-2 font-medium text-lg cursor-pointer ${
          activeTab === 'analise-perfil'
            ? 'border-indigo-500 text-indigo-600'
            : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
        }`}
      >
        Análise de Perfil do Aluno
      </button>
    </nav>
  </div>
);

export default Tabs;