import axios from 'axios';

const API_BASE_URL = '/data/';
const VG_BASE_URL = `${API_BASE_URL}/Visao_Geral`;
const EH_BASE_URL = `${API_BASE_URL}/Evolucao_Historica`;
const DT_BASE_URL = `${API_BASE_URL}/Desempenho_Topico`

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
})

export const vgClient = axios.create({
  baseURL: VG_BASE_URL,
});

export const dtClient = axios.create({
  baseURL: DT_BASE_URL,
});

export const ehClient = axios.create({
  baseURL: EH_BASE_URL,
})

export const getFilterOptions = async () => {
  try {
    const response = await apiClient.get('/opcoes_filtro.json');
    return response.data;
  } catch (error) {
    console.error("Erro ao buscar opções de filtro:", error);
    throw error;
  }
};

export const getVisaoGeralData = async (campusName, year, courseId) => {
  try {
    const response = await vgClient.get(`/${campusName}/visao_geral_${year}.json`);
    const todosCursos = response.data;
    
    return todosCursos.find(c => c.CO_CURSO == courseId);
  } catch (error) {
    console.error(`Erro ao buscar dados para ${campusName} ${year}:`, error);
    throw error;
  }
};

export const getDesempenhoTopicoData = async (campusName, year, courseId) => {
  try {
    const response = await dtClient.get(`/${campusName}/${year}/competencias_${year}.json`);
    const todosCursos = response.data;
    
    return todosCursos[courseId] || {};
  } catch (error) {
    console.error(`Erro ao buscar dados de competência para ${campusName} ${year}:`, error);
    return {}; 
  }
};

export const getEvolucaoHistorica = async (campusName, courseId) => {
  try {
    const response = await ehClient.get(`/${campusName}/evolucao_historica.json`);
    const todosCursos = response.data;
    
    return todosCursos[courseId] || [];
  } catch (error) {
    console.error(`Erro ao buscar histórico para ${campusName}/${courseId}:`, error);
    return [];
  }
};