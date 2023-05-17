import zhCN from "antd/lib/locale/zh_CN";
import AuthLayout from '@/layout/Authenticate';
import { BlankLayout } from '@/layout/Blank';
import '@/styles/globals.css'
import { ConfigProvider } from 'antd';
import { NextPage } from 'next';
import type { AppContext, AppProps } from 'next/app'
import { ReactElement, ReactNode, createContext } from 'react';
import { Response } from '@/http'
import router from "next/router";
import { authMember } from "@/api/auth";
import { useLocalObservable, useLocalStore } from "mobx-react-lite";
import createStore, { TStore } from "@/store";

type NextPageWithLayout = NextPage & {
  getLayout?: (page: ReactElement) => ReactNode;
};

type AuthProps = {
  isAuth: boolean,
  authResponse: Response<any>;
}

type AppPropsWithLayout = AppProps & {
  Component: NextPageWithLayout;
  props: AuthProps;
};

const notAuthRoutes = ['/', '/login']

export const StoreContext = createContext<TStore | null>(null);

const StoreProvider = ({children}: any) => {
  const store = useLocalObservable(createStore);
  return <StoreContext.Provider value={store}>{children}</StoreContext.Provider>
}

function App({ Component, router, pageProps, props }: AppPropsWithLayout) {
  const getLayout = Component.getLayout ?? ((elelment) => {
    if (props.isAuth && router.pathname !== '/login') {
      return (
        <AuthLayout>{elelment}</AuthLayout>
      )
    }
    return <BlankLayout>{elelment}</BlankLayout>
  })
  return (
    <ConfigProvider
      locale={zhCN}>
      <StoreProvider>
        {getLayout(<Component {...pageProps} />)}
      </StoreProvider>
    </ConfigProvider>
  )
}

App.getInitialProps = async (context: AppContext) => {
  let isAuth = true;
  const { req, res } = context.ctx;
  const memberInfo = await authMember.getMemberInfo()
  if (memberInfo && [401, 403].includes(memberInfo.code)) {
    isAuth = notAuthRoutes.includes(context.router.pathname)
    if (!notAuthRoutes.includes(context.router.pathname)) {
      if (res) {
        res.writeHead(302, {Location: '/login'})
        res.end()
      } else {
        router.push('/login')
      }
    }
  }
  return {
    props: {
      isAuth: isAuth,
      authResponse: memberInfo
    }, // will be passed to the page component as props
  }
}

export default App;
