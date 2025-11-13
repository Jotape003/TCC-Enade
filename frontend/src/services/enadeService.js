import axios from 'axios';

const API_BASE_URL = '/data/';
const DT_BASE_URL = `${API_BASE_URL}/Desempenho_Topico`

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
});

export const dtClient = axios.create({
  baseURL: DT_BASE_URL,
});

export const getFilterOptions = async () => {
  try {
    const response = await apiClient.get('/Visao_Geral/opcoes_filtro.json');
    return response.data;
  } catch (error) {
    console.error("Erro ao buscar opções de filtro:", error);
    throw error;
  }
};

export const getVisaoGeralData = async (campusName, year) => {
  try {
    const response = await apiClient.get(`/Visao_Geral/${campusName}/visao_geral_${year}.json`);
    return response.data;
  } catch (error) {
    console.error(`Erro ao buscar dados para ${campusName} ${year}:`, error);
    throw error;
  }
};

export const getDesempenhoTopicoData = async (campusName, year) => {
  try {
    const response = await dtClient.get(`/${campusName}/${year}/competencias_ce_${year}.json`);
    return response.data;
  } catch (error) {
    console.error(`Erro ao buscar dados de competência para ${campusName} ${year}:`, error);
    return {}; 
  }
};