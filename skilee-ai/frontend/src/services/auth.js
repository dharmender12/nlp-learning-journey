const TOKEN_KEY = 'skilee_token'
const USER_KEY = 'skilee_user'

export const setAuth = (token, user) => {
  localStorage.setItem(TOKEN_KEY, token)
  localStorage.setItem(USER_KEY, JSON.stringify(user))
}

export const clearAuth = () => {
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem(USER_KEY)
}

export const getToken = () => localStorage.getItem(TOKEN_KEY)

export const getUser = () => {
  const raw = localStorage.getItem(USER_KEY)
  return raw ? JSON.parse(raw) : null
}

export const isAuthed = () => Boolean(getToken())
