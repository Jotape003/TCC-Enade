import axios from 'axios';

const API_BASE_URL = '/data/';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
});

export const getFilterOptions = async () => {
  try {
    const response = await apiClient.get('/visao_geral.json/opcoes_filtro.json');
    return response.data;
  } catch (error) {
    console.error("Erro ao buscar opções de filtro:", error);
    throw error;
  }
};

export const getVisaoGeralData = async (campusName, year) => {
  try {
    const response = await apiClient.get(`/visao_geral.json/${campusName}/visao_geral_${year}.json`);
    console.log(response.data);
    return response.data;
  } catch (error) {
    console.error(`Erro ao buscar dados para ${campusName} ${year}:`, error);
    throw error;
  }
};

export const getCompetenciaData = async (campusName, year) => {
  try {
    const response = await apiClient.get(`/comp_especifico_grupo.json/${campusName}/competencias_${year}.json`);
    return response.data;
  } catch (error) {
    console.error(`Erro ao buscar dados de competência para ${campusName} ${year}:`, error);
    return {}; 
  }
};