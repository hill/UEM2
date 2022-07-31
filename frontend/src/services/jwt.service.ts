const ID_TOKEN_KEY = "id_token";
const REFRESH_TOKEN_KEY = "refresh_token";

export const getToken = (): string | null => {
  return window.localStorage.getItem(ID_TOKEN_KEY);
};

export const saveToken = (token: string): void => {
  window.localStorage.setItem(ID_TOKEN_KEY, token);
};

export const getRefreshToken = (): string | null => {
  return window.localStorage.getItem(REFRESH_TOKEN_KEY);
};

export const saveRefreshToken = (refreshToken: string) => {
  window.localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
};

export const destroyToken = (): void => {
  window.localStorage.removeItem(ID_TOKEN_KEY);
};

export default { getToken, saveToken, destroyToken, getRefreshToken, saveRefreshToken };
