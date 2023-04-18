import { ILoginForm, authMember } from '@/api/auth';
import { captchaHttp } from '@/api/captcha';
import { useDebounceFn, useRequest, useSafeState } from 'ahooks';
import { Button, Card, Form, Input, Image, Space, message, notification } from 'antd';
import { useRouter } from 'next/router';
import React, { useContext } from 'react';


const Login: React.FC = () => {
  const [ loginForm ] = Form.useForm();
  const [ initReq, setInitReq ] = useSafeState(true)
  const router = useRouter()
  const captcha = useRequest(() => {
    return captchaHttp.getCaptcha()
  }, {
    onSuccess: res => {
      if (res.code === 200) {
        setInitReq(false)
        loginForm.setFieldsValue({hash_key: res.data.hash_key})
      }
    }
  })
  const login = useRequest((values: ILoginForm) => {
    return authMember.memberLogin(values)
  }, {
    manual: true,
    onSuccess: res => {
      console.log(res)
      if (res.code === 200) {
        // localStorage.setItem('http_token', res.data.token)
        message.success(res.message);
        router.push('/')
        return false
      }
      message.error(res.message)
    }
  })

  const captchaDebounce = useDebounceFn(
    () => {
      captcha.run();
    },
    {
      wait: 500,
    },
  );

  const onLoginFinish = (values: ILoginForm) => {
    login.run(values)
  }
  return (
    <div className='xl:max-w-7xl my-0 mx-auto'>
      <div className='flex justify-center h-screen items-center'>
        <Card
          className='w-2/4'>
          <Form
            form={loginForm}
            name="basic"
            labelCol={{span: 5}}
            style={{ maxWidth: 400 }}
            onFinish={onLoginFinish}
            autoComplete="off"
          >
            <Form.Item
              label="用户名"
              name="username"
              rules={[{ required: true, message: '用户名不能为空' }]}
            >
              <Input />
            </Form.Item>

            <Form.Item
              label="密码"
              name="password"
              rules={[{ required: true, message: '密码不能为空' }]}
            >
              <Input.Password />
            </Form.Item>

            <Form.Item
              required
              label="验证码">
              <Space
                className='w-full'>
                <Form.Item
                  noStyle
                  name="check_code"
                  className='flex-1'
                  rules={[
                    {required: true, message: '请输入验证码'}
                  ]}>
                  <Input className=''/>
                </Form.Item>
                <Form.Item
                  hidden
                  name="hash_key">
                  <Input />
                </Form.Item>
                <Form.Item
                  noStyle>
                  <Image
                   preview={false}
                   className='max-h-10 h-10 w-[100px]'
                   src={initReq ? '' : `data:image/png;base64, ${captcha.data?.data.base64_image}`} 
                   onClick={() => captchaDebounce.run()}/>
                </Form.Item>
              </Space>
            </Form.Item>

            <Form.Item wrapperCol={{ offset: 5, span: 16 }}>
              <Button disabled={captcha.loading} type="primary" htmlType="submit">
                登录
              </Button>
            </Form.Item>
          </Form>
        </Card>
      </div>
    </div>
  )
}

export default Login;