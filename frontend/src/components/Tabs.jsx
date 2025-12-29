const Tabs = ({ activeTab, setActiveTab }) => (
  <div className="border-b border-gray-200">
    <nav className="-mb-px flex justify-around" aria-label="Tabs">
      <button
        onClick={() => setActiveTab('visao-geral')}
        className={`whitespace-nowrap p-3 border-b-2 font-medium text-lg cursor-pointer ${
          activeTab === 'visao-geral'
            ? 'border-indigo-500 text-indigo-600'
            : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
        }`}
      >
        Visão Geral e Comparativo
      </button>
      <button
        onClick={() => setActiveTab('evolucao-historica')}
        className={`whitespace-nowrap p-3 border-b-2 font-medium text-lg cursor-pointer ${
          activeTab === 'evolucao-historica'
            ? 'border-indigo-500 text-indigo-600'
            : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
        }`}
      >
        Evolução Histórica
      </button>
      <button
        onClick={() => setActiveTab('desempenho-topico')}
        className={`whitespace-nowrap p-3 border-b-2 font-medium text-lg cursor-pointer ${
          activeTab === 'desempenho-topico'
            ? 'border-indigo-500 text-indigo-600'
            : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
        }`}
      >
        Desempenho por Tópico
      </button>
      <button
        onClick={() => setActiveTab('analise-perfil')}
        className={`whitespace-nowrap p-3 border-b-2 font-medium text-lg cursor-pointer ${
          activeTab === 'analise-perfil'
            ? 'border-indigo-500 text-indigo-600'
            : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
        }`}
      >
        Percepção do Curso
      </button>
    </nav>
  </div>
);

export default Tabs;