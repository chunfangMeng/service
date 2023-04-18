import React from 'react';
import { useLocalStore } from 'mobx-react-lite';
import { createStore, TStore } from './'


export const StoreContext = React.createContext<TStore | null>(null)

export const StoreProvider: React.FC = ({children}: any) => {
  const store = useLocalStore(createStore)
  return (
    <StoreContext.Provider value={store}>{children}</StoreContext.Provider>
  )
}