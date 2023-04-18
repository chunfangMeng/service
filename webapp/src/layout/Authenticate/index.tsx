import React, { PropsWithChildren } from 'react';
import { TopHeader } from './Header';


const AuthLayout: React.FC<PropsWithChildren<{}>> = ({children}) => {
  return (
    <>
      <TopHeader></TopHeader>
      {children}
    </>
  )
}

export default AuthLayout;