import React, { useEffect, useMemo, useState } from 'react';
import { getCoursesLinks } from '../../../../services/enadeService';

const ExamViewerModal = ({
  isOpen,
  onClose,
  courseID,
  year,
  questionLabel,
  type = 'objetivas'
}) => {
  const [linksData, setLinksData] = useState(null);

  const questionNumber = useMemo(() => {
    return questionLabel ? questionLabel.toString().replace(/\D/g, '') : null;
  }, [questionLabel]);

  useEffect(() => {
    if (!isOpen || !courseID) return;

    const fetchLinksData = async () => {
      try {
        const response = await getCoursesLinks(courseID);
        setLinksData(response);
      } catch (error) {
        console.error('Erro ao buscar dados de links:', error);
      }
    };

    fetchLinksData();
  }, [isOpen, courseID]);

  const fullUrl = useMemo(() => {
    if (!linksData || !year || !questionNumber) return null;

    const yearData = linksData[String(year)];
    if (!yearData) return null;

    const pdfUrl = yearData.url;
    const mapaPaginas = yearData.mapa_paginas?.[type];
    const page = mapaPaginas?.[questionNumber];

    if (!pdfUrl || !page) return null;

    const basePath = import.meta.env.BASE_URL;

    return `${basePath}${pdfUrl}#page=${page}`;
  }, [linksData, year, questionNumber, type]);

  if (!isOpen || !courseID) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
      <div className="bg-white w-full max-w-6xl h-[90vh] rounded-xl shadow-2xl flex flex-col overflow-hidden">
        
        <div className="bg-indigo-900 text-white px-6 py-4 flex justify-between items-center">
          <div>
            <h3 className="text-xl font-bold">Caderno de Questões - {year}</h3>
            <p className="text-indigo-200 text-sm">
              Visualizando: Questão {questionLabel}
            </p>
          </div>

          <button
            onClick={onClose}
            className="p-2 hover:bg-white/10 rounded-full text-2xl font-bold"
          >
            &times;
          </button>
        </div>

        <div className="flex-1 bg-gray-100 relative">
          {fullUrl ? (
            <object
              data={fullUrl}
              type="application/pdf"
              className="w-full h-full"
            >
              <div className="flex flex-col items-center justify-center h-full text-gray-500 gap-4">
                <p>Visualização direta indisponível.</p>
                <a
                  href={fullUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700"
                >
                  Abrir PDF em nova aba
                </a>
              </div>
            </object>
          ) : (
            <div className="flex items-center justify-center h-full text-gray-500">
              Não foi possível localizar a página da questão.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ExamViewerModal;
