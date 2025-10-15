import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const EvolucaoHistorica = ({ historico }) => (
  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
    <div className="bg-gray-50 p-4 rounded-lg shadow">
      <h3 className="text-xl font-semibold mb-2">Evolução da Média ENADE (FG e CE)</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={historico}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="ano" />
          <YAxis domain={[0, 100]} />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="mediaFG" stroke="#8884d8" name="Média FG" strokeWidth={3} dot={{ r: 5 }} activeDot={{ r: 8 }} />
          <Line type="monotone" dataKey="mediaCE" stroke="#82ca9d" name="Média CE" strokeWidth={3} dot={{ r: 5 }} activeDot={{ r: 8 }} />
        </LineChart>
      </ResponsiveContainer>
      <p className="text-sm text-gray-600 mt-2">
        Acompanhe a tendência das notas do curso ao longo das edições do ENADE.
      </p>
    </div>
    <div className="bg-gray-50 p-4 rounded-lg shadow">
      <h3 className="text-xl font-semibold mb-2">Evolução da Taxa de Participação</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={historico}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="ano" />
          <YAxis domain={[0, 100]} />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="taxaParticipacao" stroke="#ffc658" name="Taxa de Participação (%)" strokeWidth={3} dot={{ r: 5 }} activeDot={{ r: 8 }} />
        </LineChart>
      </ResponsiveContainer>
      <p className="text-sm text-gray-600 mt-2">
        Monitore o engajamento dos alunos no exame, um fator que pode influenciar o desempenho geral.
      </p>
    </div>
  </div>
);

export default EvolucaoHistorica;