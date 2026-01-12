import React from 'react';

const WelcomeGuide = () => {
  return (
    <div className="max-w-6xl mx-auto mt-8 p-8 bg-white animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="flex flex-col justify-center items-center border-b border-gray-100 pb-8 mb-8 text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-3">Bem-vindo ao Observatório ENADE</h1>
        <p className="text-gray-600 text-lg max-w-3xl">
          Uma ferramenta de visualização para apoio à gestão acadêmica da UFC Quixadá. Selecione um <strong>Curso</strong> no menu superior para iniciar a análise.
        </p>
      </div>

      <div className="grid md:grid-cols-2 gap-x-12 gap-y-10 mb-12">
        
        <div className="flex gap-4 items-start group">
          <div className="p-3 bg-blue-50 text-blue-700 rounded-lg border border-blue-100 group-hover:bg-blue-100 transition-colors">
            <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 0 1 3 19.875v-6.75ZM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V8.625ZM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V4.125Z" />
            </svg>
          </div>
          <div>
            <h3 className="font-bold text-gray-900 mb-1 text-lg">Visão Geral</h3>
            <p className="text-sm text-gray-600 leading-relaxed">
                Permite uma leitura rápida da situação atual do curso.
            </p>
          </div>
        </div>

        <div className="flex gap-4 items-start group">
          <div className="p-3 bg-emerald-50 text-emerald-700 rounded-lg border border-emerald-100 group-hover:bg-emerald-100 transition-colors">
            <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
            </svg>
          </div>
          <div>
            <h3 className="font-bold text-gray-900 mb-1 text-lg">Evolução Histórica</h3>
            <p className="text-sm text-gray-600 leading-relaxed">
              Análise longitudinal das notas ao longo das edições do exame.
            </p>
          </div>
        </div>

        <div className="flex gap-4 items-start group">
          <div className="p-3 bg-indigo-50 text-indigo-700 rounded-lg border border-indigo-100 group-hover:bg-indigo-100 transition-colors">
            <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M10.5 6a7.5 7.5 0 1 0 7.5 7.5h-7.5V6Z M13.5 10.5H21A7.5 7.5 0 0 0 13.5 3v7.5Z" />
            </svg>
          </div>
          <div>
            <h3 className="font-bold text-gray-900 mb-1 text-lg">Desempenho por Tópico</h3>
            <p className="text-sm text-gray-600 leading-relaxed">
              Diagnóstico detalhado dos Componentes Específicos e de Formação Geral.
            </p>
          </div>
        </div>

        <div className="flex gap-4 items-start group">
          <div className="p-3 bg-amber-50 text-amber-700 rounded-lg border border-amber-100 group-hover:bg-amber-100 transition-colors">
            <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M15 19.128a9.38 9.38 0 0 0 2.625.372 9.337 9.337 0 0 0 4.121-.952 4.125 4.125 0 0 0-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 0 1 8.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0 1 11.964-3.07M12 6.375a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0Zm8.25 2.25a2.625 2.625 0 1 1-5.25 0 2.625 2.625 0 0 1 5.25 0Z" />
            </svg>
          </div>
          <div>
            <h3 className="font-bold text-gray-900 mb-1 text-lg">Percepção do Curso</h3>
            <p className="text-sm text-gray-600 leading-relaxed">
              Dados do Questionário do Estudante que avaliam a infraestrutura, organização didática e oportunidades de ampliação da formação.
            </p>
          </div>
        </div>

      </div>

      <div className="bg-gray-50 rounded-lg border border-gray-200 p-6 flex flex-col sm:flex-row gap-5 items-center sm:items-start">
        
        <div className="text-center sm:text-left">
          <h3 className="font-bold text-gray-900 text-sm uppercase tracking-wide mb-1">
            Destaque
          </h3>
          <p className="text-gray-600 text-sm">
            Na aba <strong>Desempenho por Tópico</strong>, em <strong>Percepção da Prova</strong> o sistema oferece integração direta com os cadernos de prova. 
            Ao clicar no identificador de uma questão (ex: <span className="px-1.5 py-0.5 bg-gray-200 rounded text-gray-700 font-bold text-xs border border-gray-300">Q15</span>), 
            o PDF original será aberto automaticamente na página correspondente a questão selecionada.
          </p>
        </div>
      </div>

    </div>
  );
};

export default WelcomeGuide;