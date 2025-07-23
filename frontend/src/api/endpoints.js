import { API } from "./axios";

export const getAccount = (gameName, tagLine) =>
  API.get(`/accounts/${gameName}/${tagLine}`).then(r => r.data);

export const getSummoner = (puuid) =>
  API.get(`/summoners/${puuid}`).then(r => r.data);

export const getHistory = (puuid, start = 0, count = 20) =>
  API.get(`/matches/history/${puuid}`, { params: { start, count } }).then(r => r.data);

export const getMatch = (matchId) =>
  API.get(`/matches/${matchId}`).then(r => r.data);

export const getChampions = () => API.get(`/static/champions`).then(r => r.data);
export const getItems     = () => API.get(`/static/items`).then(r => r.data);
export const getTraits    = () => API.get(`/static/traits`).then(r => r.data);
export const getAugments  = () => API.get(`/static/augments`).then(r => r.data);
