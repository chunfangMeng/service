import ApiHttp from "@/http";

type CaptchaResponse = {
  base64_image: string;
  hash_key: string;
}

class CaptchaHttp extends ApiHttp {
  getCaptcha = () => this.get<CaptchaResponse>('/api/v1/open/captcha/')
}

export const captchaHttp = new CaptchaHttp()