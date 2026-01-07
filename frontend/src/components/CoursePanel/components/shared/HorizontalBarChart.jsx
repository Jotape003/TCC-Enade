import React from 'react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend 
} from 'recharts';
import CustomTooltip from './CustomTooltip';

const HorizontalBarChart = ({ 
  data, 
  dataKey = "name",
  barGap = 4,
  children,
  barsConfig = [],
  maxValue = 100,
  yAxisWidth = 180,
  height
}) => {

  return (
    <div style={{ height: `${height}px`, width: '100%' }}>
      <ResponsiveContainer>
        <BarChart 
          data={data} 
          layout="vertical" 
          barGap={barGap}
        >
          <CartesianGrid strokeDasharray="3 3" horizontal={true} vertical={true} stroke="#f1f5f9" />
          
          <XAxis type="number" domain={[0, maxValue]} hide />
          
          <YAxis 
            dataKey={dataKey} 
            type="category" 
            width={dataKey === 'name' ? 180 : yAxisWidth}
            tick={{ fill: '#475569', fontSize: 14, fontWeight: 600 }} 
          />
          
          <Tooltip content={<CustomTooltip />} cursor={{ fill: '#f8fafc' }} />
          
          <Legend iconType="circle" />

          {barsConfig.map((bar) => (
            <Bar
              key={bar.key}
              dataKey={bar.key}
              name={bar.label || bar.key}
              fill={bar.color}
              barSize={bar.size || 20}
              radius={[0, 4, 4, 0]}
              animationDuration={1500}
            />
          ))}

          {children}

        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default HorizontalBarChart;