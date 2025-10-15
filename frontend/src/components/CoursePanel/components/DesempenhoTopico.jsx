import React from 'react';
import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const DesempenhoTopico = ({ desempenhoTopico, currentYearData, loadingLlm }) => (
  <div className="space-y-6">
    <div className="bg-gray-50 p-4 rounded-lg shadow">
      <h3 className="text-xl font-semibold mb-2">Perfil de Desempenho por Tópico ({currentYearData.ano})</h3>
      <ResponsiveContainer width="100%" height={400}>
        <RadarChart outerRadius={120} data={desempenhoTopico}>
          <PolarGrid />
          <PolarAngleAxis dataKey="topico" />
          <PolarRadiusAxis domain={[0, 100]} />
          <Tooltip />
          <Legend />
          <Radar name="Média do Curso" dataKey="curso" stroke="#8884d8" fill="#8884d8" fillOpacity={0.6} />
          <Radar name="Média Nacional" dataKey="nacional" stroke="#82ca9d" fill="#82ca9d" fillOpacity={0.6} />
        </RadarChart>
      </ResponsiveContainer>
      <p className="text-sm text-gray-600 mt-2">
        Compare visualmente o perfil de desempenho do curso em diferentes tópicos em relação à média nacional.
      </p>
    </div>
    <div className="bg-gray-50 p-4 rounded-lg shadow">
      <h3 className="text-xl font-semibold mb-2">Detalhamento por Tópico Curricular ({currentYearData.ano})</h3>
      <ResponsiveContainer width="100%" height={400}>
        <BarChart
          layout="vertical"
          data={desempenhoTopico.sort((a, b) => (a.curso - a.nacional) - (b.curso - b.nacional))}
          margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis type="number" domain={[0, 100]} />
          <YAxis dataKey="topico" type="category" width={150} />
          <Tooltip />
          <Legend />
          <Bar dataKey="curso" fill="#8884d8" name="Média do Curso (%)" radius={[10, 10, 0, 0]} />
          <Bar dataKey="nacional" fill="#82ca9d" name="Média Nacional (%)" radius={[10, 10, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
      <p className="text-sm text-gray-600 mt-2">
        Analise o desempenho em tópicos específicos. Tópicos à esquerda podem indicar áreas de melhoria curricular.
      </p>
    </div>
  </div>
);

export default DesempenhoTopico;