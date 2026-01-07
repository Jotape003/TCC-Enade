export const TabsSelector = ({ message, onClick, activeTab, path, type }) => {
    return (
        <button
        onClick={onClick}
        className={`flex gap-2 items-center whitespace-nowrap p-3 border-b-2 font-semibold text-lg cursor-pointer ${
          activeTab === type
            ? 'border-indigo-500 text-indigo-600'
            : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
        }`}
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
          <path d={path}/>
        </svg>

        {message}
      </button>
    )
}