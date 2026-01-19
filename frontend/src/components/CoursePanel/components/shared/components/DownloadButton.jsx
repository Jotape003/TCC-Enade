import React, { useState, useRef, useEffect } from 'react';

const DownloadButton = ({ onDownloadPNG, onDownloadCSV, className = "" }) => {
  const [isOpen, setIsOpen] = useState(false);
  const menuRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleAction = (action) => {
    action();
    setIsOpen(false);
  };

  return (
    <div className={`relative inline-block text-left ${className}`} ref={menuRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className={`
          p-2 rounded-lg transition-all duration-200 text-sm
          ${isOpen ? 'bg-indigo-50 shadow-sm ring-1' : 'bg-white text-gray-800 cursor-pointer  hover:bg-gray-100 hover:border-indigo-100'}
        `}
        title="Exportar dados"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-5">
          <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" />
        </svg>
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 origin-top-right bg-white rounded-xl shadow-xl ring-1 ring-gray-200 ring-opacity-5 focus:outline-none z-50 animate-in fade-in zoom-in-95 duration-200">
          <div className="py-1 cursor-pointer">
            
            <button
              onClick={() => handleAction(onDownloadPNG)}
              className="w-full text-left px-4 py-2.5 text-sm text-gray-700 hover:bg-indigo-50 hover:text-indigo-700 flex items-center gap-3 transition-colors group"
            >
              <span>PNG</span>
            </button>

            <button
              onClick={() => handleAction(onDownloadCSV)}
              className="w-full text-left px-4 py-2.5 text-sm text-gray-700 hover:bg-emerald-50 hover:text-emerald-700 flex items-center gap-3 transition-colors group"
            >
              <span>CSV</span>
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default DownloadButton;