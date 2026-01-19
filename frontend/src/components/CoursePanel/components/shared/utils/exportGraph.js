import { toPng } from 'html-to-image';

export const exportToPNG = async (elementRef, fileName) => {
  if (elementRef.current === null) {
    return;
  }

  try {
    const dataUrl = await toPng(elementRef.current, { 
      backgroundColor: '#ffffff',
      cacheBust: true,
      skipFonts: true
    });
    
    const link = document.createElement('a');
    link.download = `${fileName}.png`;
    link.href = dataUrl;
    link.click();
  } catch (err) {
    console.error('Erro ao exportar a imagem:', err);
  }
};

export const exportToCSV = (data, fileName) => {
  if (!data || !data.length) {
    alert("Sem dados para exportar.");
    return;
  }

  const headers = Object.keys(data[0]);
  
  const csvRows = [
    headers.join(','),
    ...data.map(row => 
      headers.map(fieldName => {
        const value = row[fieldName];
        return `"${String(value).replace(/"/g, '""')}"`;
      }).join(',')
    )
  ];

  const csvString = csvRows.join('\n');
  const blob = new Blob([csvString], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', `${fileName}.csv`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};