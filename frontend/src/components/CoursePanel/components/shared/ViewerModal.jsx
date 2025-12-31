import React from 'react';

const ExamViewerModal = ({ isOpen, onClose, pdfUrl, questionLabel, year }) => {
  if (!isOpen || !pdfUrl) return null;
  const questionNumber = questionLabel ? questionLabel.toString().replace(/\D/g, '') : '';

  const searchTerm = `QUESTÃO ${questionNumber}`;
  const fullUrl = `${pdfUrl}#search="${searchTerm}"`;
  console.log(fullUrl);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 animate-in fade-in duration-200">
      <div className="bg-white w-full max-w-6xl h-[90vh] rounded-xl shadow-2xl flex flex-col overflow-hidden animate-in zoom-in-95 duration-300">
        
        <div className="bg-indigo-900 text-white px-6 py-4 flex justify-between items-center">
          <div>
            <h3 className="text-xl font-bold">Caderno de Questões - {year}</h3>
            <p className="text-indigo-200 text-sm">Visualizando: Questão {questionLabel}</p>
          </div>
          <button 
            onClick={onClose}
            className="p-2 hover:bg-white/10 rounded-full transition-colors cursor-pointer text-2xl font-bold"
          >
            &times;
          </button>
        </div>

        <div className="flex-1 bg-gray-100 relative">
          <object data={fullUrl} type="application/pdf" className="w-full h-full">
            <div className="flex flex-col items-center justify-center h-full text-gray-500 gap-4">
              <p>Visualização direta indisponível.</p>
              <a 
                href={pdfUrl} 
                target="_blank" 
                rel="noopener noreferrer"
                className="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700"
              >
                Abrir PDF em nova aba
              </a>
            </div>
          </object>
        </div>
      </div>
    </div>
  );
};

export default ExamViewerModal;