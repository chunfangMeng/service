import { message } from "antd";
import axios, { AxiosError, AxiosInstance } from "axios";


type RequestData = {}

export type Response<T> = {
  code: number;
  message: string;
  data: T;
}

class ApiHttp {
  instance: AxiosInstance
  constructor() {
    this.instance = axios.create({
      baseURL: 'http://localhost:8000',
      withCredentials: true
    })
    this.instance.interceptors.request.use(
      (values) => {
        // let token = ''
        // try {
        //    token = localStorage.getItem('http_token') ?? ''
        // } catch {
        //   token = ''
        // }
        // if (token !== null && typeof values.headers !== "undefined") {
        //   values['headers'].setAuthorization(`token ${token}`)
        // }
        return values
      },
      error => {}
    )
    this.instance.interceptors.response.use(
      (response) => {
        if (typeof window === 'undefined') {
          console.log('>>>', response.headers)
        } else {
          console.log('<<<', response.headers)
        }
        if (Object.keys(response.data).includes('code')) {
          return response.data
        }
        return response.data
      },
      (error: AxiosError<Response<unknown>>) => {
        try{
          message.error(error.response?.data.message ?? '请求失败')
        } catch {
          
        }
      }
    )
  }

  get<T>(url: string, params?: RequestData): Promise<Response<T>> {
    return this.instance.get(url, {params: params})
  }

  post<T>(url: string, data?: RequestData): Promise<Response<T>> {
    return this.instance.post(url, data)
  }

  patch<T>(url: string, data?: RequestData): Promise<Response<T>> {
    return this.instance.patch(url, data)
  }

  put<T>(url: string, data?: RequestData): Promise<Response<T>> {
    return this.instance.put(url, data)
  }

  delete<T>(url: string, data?: RequestData): Promise<Response<T>> {
    return this.instance.delete(url, data)
  }
}

export default ApiHttp;