/**
 * 认证相关 API
 */
import { request } from './request'

export interface LoginParams {
  username: string
  password: string
}

export interface RegisterParams {
  username: string
  email: string
  password: string
}

export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
}

export interface UserInfo {
  id: number
  username: string
  email: string
  is_active: boolean
  is_superuser: boolean
  created_at: string
}

// 用户登录
export const login = (data: LoginParams) => {
  // FastAPI OAuth2 需要使用 form-data 格式
  const formData = new FormData()
  formData.append('username', data.username)
  formData.append('password', data.password)
  
  return request.post<TokenResponse>('/auth/login', formData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  })
}

// 用户注册
export const register = (data: RegisterParams) => {
  return request.post<UserInfo>('/auth/register', data)
}

// 获取当前用户信息
export const getCurrentUser = () => {
  return request.get<UserInfo>('/users/me')
}
