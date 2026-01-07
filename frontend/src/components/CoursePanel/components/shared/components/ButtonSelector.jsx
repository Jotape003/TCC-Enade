export const ButtonSelector = ({ messageButton, onClick, value, path, type }) => {
    return (
        <button
            onClick={onClick}
            className={`
            flex items-center gap-2 px-6 py-2 cursor-pointer rounded-full font-semibold transition-all duration-300
            ${value === type
                ? 'bg-indigo-600 text-white scale-105'
                  : 'bg-transparent text-gray-600 hover:bg-white hover:text-indigo-600 hover:shadow-sm'
                
            }
            `}
        >
            <svg className={`w-4 h-4 ${value === type ? 'fill-amber-50' : 'fill-current'}`} viewBox="0 0 20 20">
            <path d={path}/>
            </svg>
            {messageButton}
        </button>
    )
}