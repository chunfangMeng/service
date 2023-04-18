import React, { PropsWithChildren } from 'react';


export const BlankLayout: React.FC<PropsWithChildren<{}>> = ({children}) => {
  return (
    <>{children}</>
  )
}