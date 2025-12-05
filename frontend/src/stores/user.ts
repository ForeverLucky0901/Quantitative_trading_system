/**
 * 用户状态管理
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { login as loginApi, getCurrentUser, type LoginParams, type UserInfo } from '@/api'

export const useUserStore = defineStore('user', () => {
  const token = ref<string>(localStorage.getItem('access_token') || '')
  const userInfo = ref<UserInfo | null>(null)
  
  // 登录
  const login = async (params: LoginParams) => {
    const res = await loginApi(params)
    token.value = res.access_token
    localStorage.setItem('access_token', res.access_token)
    localStorage.setItem('refresh_token', res.refresh_token)
    
    // 获取用户信息
    await fetchUserInfo()
    
    return res
  }
  
  // 获取用户信息
  const fetchUserInfo = async () => {
    const res = await getCurrentUser()
    userInfo.value = res
    return res
  }
  
  // 登出
  const logout = () => {
    token.value = ''
    userInfo.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }
  
  return {
    token,
    userInfo,
    login,
    fetchUserInfo,
    logout
  }
})
