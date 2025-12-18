import axios from 'axios';

const API_BASE_URL = '/data/';
const VG_BASE_URL = `${API_BASE_URL}/Visao_Geral`;
const EH_BASE_URL = `${API_BASE_URL}/Evolucao_Historica`;
const DT_BASE_URL = `${API_BASE_URL}/Desempenho_Topico`;
const QUESTOES_BASE_URL = `${API_BASE_URL}/Analise_Perfil`;

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
})

export const vgClient = axios.create({
  baseURL: VG_BASE_URL,
});

export const dtClient = axios.create({
  baseURL: DT_BASE_URL,
});

export const questoesClient = axios.create({
  baseURL: QUESTOES_BASE_URL,
})

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

export const getVisaoGeralData = async (campusName, courseId) => {
  try {
    const response = await vgClient.get(`/${campusName}/visao_geral_consolidado.json`);
    const todosCursosHistorico = response.data;
    
    return todosCursosHistorico[courseId] || {};
  } catch (error) {
    console.error(`Erro ao buscar Visão Geral consolidada para ${campusName}:`, error);
    return {};
  }
};

export const getDesempenhoTopicoData = async (campusName, courseId) => {
  try {
    const response = await dtClient.get(`/${campusName}/competencias_consolidado.json`);
    const todosCursosTodosAnos = response.data;
    
    return todosCursosTodosAnos[courseId] || {};
  } catch (error) {
    console.error(`Erro ao buscar dados consolidados para ${campusName}:`, error);
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

export const getPerfilConsolidado = async (campusName, courseId) => {
   try {
     const response = await questoesClient.get(`/${campusName}/perfil_consolidado.json`);
     const todosCursos = response.data;

     return todosCursos[courseId] || {};
   } catch (error) {
     console.warn(`Dados de perfil não encontrados para ${campusName}`);
     return {};
   }
};