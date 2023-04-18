import { Button, Input, Space } from 'antd';
import React from 'react';


export const TopHeader: React.FC = () => {
  return (
    <>
      <div className='bg-slate-50'>
        <div className='flex h-10 items-center max-w-7xl justify-between my-0 mx-auto'>
          <div>公告栏</div>
          <div>用户名操作框</div>
        </div>
      </div>
      <div className='max-w-7xl my-0 mx-auto'>
        <div className="flex justify-between items-center my-0 mx-auto">
          <div className="bg-slate-500 h-16 w-40">Logo</div>
          <div className="p-2">
            <div className='flex'>
              <Space size={"large"}>
                <Input.Search className="w-96" size="large" placeholder="搜索商品" enterButton />
                <Button size="large">我的购物车</Button>
              </Space>
            </div>
            <div>搜索备选词条</div>
          </div>
        </div>
      </div>
    </>
  )
}