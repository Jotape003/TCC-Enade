import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const VisaoGeral = ({ currentYearData }) => (
  <div className="grid grid-cols-1 gap-6">
    <div className="bg-blue-50 p-4 rounded-lg shadow">
      <h3 className="text-xl font-semibold mb-2">Média ENADE Geral</h3>
      <p className="text-4xl font-extrabold text-blue-700">
        {((currentYearData.mediaFG + currentYearData.mediaCE) / 2).toFixed(1)}
      </p>
      <p className="text-sm text-gray-600">Considerando Formação Geral e Componente Específico</p>
    </div>
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div className="bg-gray-50 p-4 rounded-lg shadow">
        <h3 className="text-xl font-semibold mb-2">Comparativo de Desempenho (FG e CE - {currentYearData.ano})</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart
            data={[
              { name: 'Formação Geral', Curso: currentYearData.mediaFG, Nacional: currentYearData.mediaNacionalFG, UFCQuixada: currentYearData.mediaUFCQuixadaFG },
              { name: 'Componente Específico', Curso: currentYearData.mediaCE, Nacional: currentYearData.mediaNacionalCE, UFCQuixada: currentYearData.mediaUFCQuixadaCE },
            ]}
            margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis domain={[0, 100]} />
            <Tooltip />
            <Legend />
            <Bar dataKey="Curso" fill="#8884d8" name="Média do Curso" radius={[10, 10, 0, 0]} />
            <Bar dataKey="Nacional" fill="#82ca9d" name="Média Nacional" radius={[10, 10, 0, 0]} />
            <Bar dataKey="UFCQuixada" fill="#ffc658" name="Média UFC Quixadá" radius={[10, 10, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
        <p className="text-sm text-gray-600 mt-2">
          Compare o desempenho geral do curso em Formação Geral e Componente Específico com médias nacional e da UFC Quixadá.
        </p>
      </div>
      <div className="bg-gray-50 p-4 rounded-lg shadow">
        <h3 className="text-xl font-semibold mb-2">Desempenho em Formação Geral ({currentYearData.ano})</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart
            data={[
              { name: 'FG', Curso: currentYearData.mediaFG, Nacional: currentYearData.mediaNacionalFG, UFCQuixada: currentYearData.mediaUFCQuixadaFG },
            ]}
            margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis domain={[0, 100]} />
            <Tooltip />
            <Legend />
            <Bar dataKey="Curso" fill="#ff7f50" name="Média do Curso (FG)" radius={[10, 10, 0, 0]} />
            <Bar dataKey="Nacional" fill="#20b2aa" name="Média Nacional (FG)" radius={[10, 10, 0, 0]} />
            <Bar dataKey="UFCQuixada" fill="#d8bfd8" name="Média UFC Quixadá (FG)" radius={[10, 10, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
        <p className="text-sm text-gray-600 mt-2">
          Análise aprofundada do desempenho do curso apenas no Componente de Formação Geral.
        </p>
      </div>
    </div>
  </div>
);

export default VisaoGeral;