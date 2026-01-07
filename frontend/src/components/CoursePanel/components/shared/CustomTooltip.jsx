const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-slate-800/95 backdrop-blur-sm p-4 rounded-xl shadow-xl border border-slate-700 text-white min-w-[150px]">
        <p className="text-sm font-medium text-slate-400 mb-2 border-b border-slate-700 pb-1">
            {label}
        </p>
        <div className="space-y-2">
          {payload.map((entry, index) => (
            <div key={index} className="flex items-center justify-between gap-4 text-sm">
              <span className="flex items-center gap-2">
                <span 
                  className={`w-2 h-2 rounded-full ${entry.dataKey.includes('nota_') ? 'ring-2 ring-indigo-400 bg-indigo-600' : ''}`}
                  style={{ backgroundColor: entry.color }}
                />
                <span className={entry.dataKey.includes('nota_') ? 'font-bold text-white' : 'opacity-80'}>
                  {entry.name}
                </span>
              </span>
              <span className="font-bold font-mono">{Number(entry.value).toFixed(1)}</span>
            </div>
          ))}
        </div>
      </div>
    );
  }
  return null;
};

export default CustomTooltip;