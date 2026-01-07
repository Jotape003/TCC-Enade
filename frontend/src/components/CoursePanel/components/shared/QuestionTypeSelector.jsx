import React from 'react';
import { ButtonSelector } from './components/ButtonSelector';

const QuestionTypeSelector = ({ value, onChange }) => {
  return (
    <div className="flex">
      <div className="bg-gray-100 p-1.5 gap-4 cursor-pointer rounded-full inline-flex items-center shadow-inner border border-gray-200 text-2xs">
        <ButtonSelector 
            path="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
            messageButton="Questões Objetivas"
            onClick={() => onChange('objetivas')}
            value={value}
            type="objetivas"
        />

        <ButtonSelector 
            path="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"
            messageButton="Questões Discursivas"
            onClick={() => onChange('discursivas')}
            value={value}
            type="discursivas"
        />

      </div>
    </div>
  );
};

export default QuestionTypeSelector;