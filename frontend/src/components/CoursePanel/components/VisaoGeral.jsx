// src/components/CoursePanel/VisaoGeral.js
import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LabelList } from 'recharts';

const VisaoGeral = ({ visaoGeralData }) => {

  const dataNotaGeral = [
    { name: 'Nota Geral',
      'Curso': visaoGeralData.nota_geral_media_curso ?? 0,
      'UFC': visaoGeralData.media_ufc_geral ?? 0,
      'Brasil': visaoGeralData.media_nacional_geral ?? 0,
      'Região': visaoGeralData.media_regiao_geral ?? 0,
      'Ceará': visaoGeralData.media_uf_geral ?? 0
    }
  ];
  const dataFormacaoGeral = [
    { name: 'Form. Geral',
      'Curso': visaoGeralData.nota_fg_media_curso ?? 0,
      'UFC': visaoGeralData.media_ufc_fg ?? 0,
      'Brasil': visaoGeralData.media_nacional_fg ?? 0,
      'Região': visaoGeralData.media_regiao_fg ?? 0,
      'Ceará': visaoGeralData.media_uf_fg ?? 0
    }
  ];
  const dataCompEspecifico = [
    { name: 'Comp. Específico',
      'Curso': visaoGeralData.nota_ce_media_curso ?? 0,
      'UFC': visaoGeralData.media_ufc_ce ?? 0,
      'Brasil': visaoGeralData.media_nacional_ce ?? 0,
      'Região': visaoGeralData.media_regiao_ce ?? 0,
      'Ceará': visaoGeralData.media_uf_ce ?? 0
    }
  ];

  return (
    <div className="space-y-10">
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-center">
        <div className="bg-blue-100 p-4 rounded-lg shadow">
          <p className="text-sm text-blue-700 font-semibold">Nota Média Geral</p>
          <p className="text-3xl font-bold text-blue-900">{visaoGeralData.nota_geral_media_curso ?? 'N/A'}</p>
        </div>
        <div className="bg-green-100 p-4 rounded-lg shadow">
          <p className="text-sm text-green-700 font-semibold">Nota Formação Geral</p>
          <p className="text-3xl font-bold text-green-900">{visaoGeralData.nota_fg_media_curso ?? 'N/A'}</p>
        </div>
        <div className="bg-yellow-100 p-4 rounded-lg shadow">
          <p className="text-sm text-yellow-700 font-semibold">Nota Comp. Específico</p>
          <p className="text-3xl font-bold text-yellow-900">{visaoGeralData.nota_ce_media_curso ?? 'N/A'}</p>
        </div>
        <div className="bg-gray-200 p-4 rounded-lg shadow">
          <p className="text-sm text-gray-700 font-semibold">Total de Participantes</p>
          <p className="text-3xl font-bold text-gray-900">{visaoGeralData.total_participantes ?? 'N/A'}</p>
        </div>
      </div>

      <div className="bg-white pb-4 gap-12 flex flex-col">
        <div style={{ width: '100%', height: 300 }}>
          <h4 className="text-lg font-semibold text-gray-700 mb-2 text-center">Comparativo - Nota Geral</h4>
          <ResponsiveContainer>
            <BarChart data={dataNotaGeral} layout="vertical" margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" domain={[0, 100]} />
              <YAxis type="category" dataKey="name" hide />
              <Tooltip />
              <Bar dataKey="Curso" fill="#051650" radius={[0, 10, 10, 0]}>
                <LabelList dataKey="Curso" position="right" formatter={(value) => value?.toFixed(1)} />
              </Bar>
              <Bar dataKey="UFC" fill="#E70000" radius={[0, 10, 10, 0]}>
                <LabelList dataKey="UFC" position="right" formatter={(value) => value?.toFixed(1)} />
              </Bar>
              <Bar dataKey="Brasil" fill="#FF7B00" radius={[0, 10, 10, 0]}>
                <LabelList dataKey="Brasil" position="right" formatter={(value) => value?.toFixed(1)} />
              </Bar>
              <Bar
                dataKey="Região" fill="#0A5C36" radius={[0, 10, 10, 0]}>
                <LabelList dataKey="Região" position="right" formatter={(value) => value?.toFixed(1)} />
              </Bar>
              <Bar dataKey="Ceará" fill="#FFE745" radius={[0, 10, 10, 0]}>
                <LabelList dataKey="Ceará" position="right" formatter={(value) => value?.toFixed(1)} />
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div style={{ width: '100%', height: 300 }}>
          <h4 className="text-lg font-semibold text-gray-700 mb-2 text-center">Comparativo - Formação Geral</h4>
          <ResponsiveContainer>
            <BarChart data={dataFormacaoGeral} layout="vertical" margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" domain={[0, 100]} />
              <YAxis type="category" dataKey="name" hide />
              <Tooltip />
              <Bar dataKey="Curso" fill="#051650" radius={[0, 10, 10, 0]}>
                 <LabelList dataKey="Curso" position="right" formatter={(value) => value?.toFixed(1)} />
              </Bar>
              <Bar dataKey="UFC" fill="#E70000" radius={[0, 10, 10, 0]}>
                 <LabelList dataKey="UFC" position="right" formatter={(value) => value?.toFixed(1)} />
              </Bar>
              <Bar dataKey="Brasil" fill="#FF7B00" radius={[0, 10, 10, 0]}>
                 <LabelList dataKey="Brasil" position="right" formatter={(value) => value?.toFixed(1)} />
              </Bar>
              <Bar
                dataKey="Região" fill="#0A5C36" radius={[0, 10, 10, 0]}>
                <LabelList dataKey="Região" position="right" formatter={(value) => value?.toFixed(1)} />
              </Bar>
              <Bar dataKey="Ceará" fill="#FFE745" radius={[0, 10, 10, 0]}>
                <LabelList dataKey="Ceará" position="right" formatter={(value) => value?.toFixed(1)} />
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Gráfico Componente Específico */}
        <div style={{ width: '100%', height: 300 }}>
          <h4 className="text-lg font-semibold text-gray-700 mb-2 text-center">Comparativo - Componente Específico</h4>
          <ResponsiveContainer>
            <BarChart data={dataCompEspecifico} layout="vertical" margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" domain={[0, 100]} />
              <YAxis type="category" dataKey="name" hide />
              <Tooltip />
              <Legend />
              <Bar dataKey="Curso" fill="#051650" radius={[0, 10, 10, 0]}>
                 <LabelList dataKey="Curso" position="right" formatter={(value) => value?.toFixed(1)} />
              </Bar>
              <Bar dataKey="UFC" fill="#E70000" radius={[0, 10, 10, 0]}>
                 <LabelList dataKey="UFC" position="right" formatter={(value) => value?.toFixed(1)} />
              </Bar>
              <Bar dataKey="Brasil" fill="#FF7B00" radius={[0, 10, 10, 0]}>
                 <LabelList dataKey="Brasil" position="right" formatter={(value) => value?.toFixed(1)} />
              </Bar>
              <Bar
                dataKey="Região" fill="#0A5C36" radius={[0, 10, 10, 0]}>
                <LabelList dataKey="Região" position="right" formatter={(value) => value?.toFixed(1)} />
              </Bar>
              <Bar dataKey="Ceará" fill="#FFE745" radius={[0, 10, 10, 0]}>
                <LabelList dataKey="Ceará" position="right" formatter={(value) => value?.toFixed(1)} />
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default VisaoGeral;