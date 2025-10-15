import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const AnalisePerfil = ({ perfilAluno }) => (
  <div className="space-y-6">
    <div className="bg-gray-50 p-4 rounded-lg shadow">
      <h3 className="text-xl font-semibold mb-2">Desempenho por Tipo de Escola de Ensino Médio</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={perfilAluno.tipoEscola}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="categoria" />
          <YAxis domain={[0, 100]} />
          <Tooltip />
          <Legend />
          <Bar dataKey="cursoFG" fill="#ff7f50" name="Curso FG" radius={[10, 10, 0, 0]} />
          <Bar dataKey="cursoCE" fill="#6a5acd" name="Curso CE" radius={[10, 10, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
      <p className="text-sm text-gray-600 mt-2">
        Análise comparativa do desempenho de alunos que vieram de escola pública vs. privada.
        Isso pode indicar a necessidade de programas de nivelamento ou apoio inicial.
      </p>
    </div>
    <div className="bg-gray-50 p-4 rounded-lg shadow">
      <h3 className="text-xl font-semibold mb-2">Desempenho por Faixa de Renda Familiar</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={perfilAluno.faixaRenda}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="categoria" />
          <YAxis domain={[0, 100]} />
          <Tooltip />
          <Legend />
          <Bar dataKey="cursoFG" fill="#20b2aa" name="Curso FG" radius={[10, 10, 0, 0]} />
          <Bar dataKey="cursoCE" fill="#d8bfd8" name="Curso CE" radius={[10, 10, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
      <p className="text-sm text-gray-600 mt-2">
        Examine como a renda familiar pode se correlacionar com o desempenho. Pode indicar a necessidade de programas de assistência estudantil.
      </p>
    </div>
    <div className="bg-gray-50 p-4 rounded-lg shadow">
      <h3 className="text-xl font-semibold mb-2">Desempenho por Turno do Curso</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={perfilAluno.turno}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="categoria" />
          <YAxis domain={[0, 100]} />
          <Tooltip />
          <Legend />
          <Bar dataKey="cursoFG" fill="#ff6347" name="Curso FG" radius={[10, 10, 0, 0]} />
          <Bar dataKey="cursoCE" fill="#4682b4" name="Curso CE" radius={[10, 10, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
      <p className="text-sm text-gray-600 mt-2">
        Compare o desempenho entre os turnos diurno e noturno, o que pode influenciar ajustes pedagógicos.
      </p>
    </div>
  </div>
);

export default AnalisePerfil;