import axios from 'axios';

const API_BASE_URL = '/data/visao_geral.json';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
});

export const getFilterOptions = async () => {
  try {
    const response = await apiClient.get('/opcoes_filtro.json');
    return response.data;
  } catch (error) {
    console.error("Erro ao buscar opções de filtro:", error);
    throw error;
  }
};

export const getVisaoGeralData = async (campusName, year) => {
  try {
    const response = await apiClient.get(`/${campusName}/visao_geral_${year}.json`);
    return response.data;
  } catch (error) {
    console.error(`Erro ao buscar dados para ${campusName} ${year}:`, error);
    throw error;
  }
};
