import ApiHttp from "@/http";

export interface ILoginForm {
  check_code: string;
  hash_key: string;
  password: string;
  username: string;
}

export interface ILoginResponse {
  token: string;
}

class AuthMember extends ApiHttp {
  getMemberInfo = () => this.get('/api/v1/member/info/')
  memberLogin = (values: ILoginForm) => this.post<ILoginResponse>('/api/v1/member/login/', values)
}

export const authMember = new AuthMember();