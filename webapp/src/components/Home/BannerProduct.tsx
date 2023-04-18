import { Carousel } from 'antd';
import React from 'react';

const contentStyle: React.CSSProperties = {
  height: '200px',
  color: '#fff',
  lineHeight: '200px',
  textAlign: 'center',
  background: '#364d79',
};
const BannerProduct: React.FC = () => {
  return (
    <div className='max-w-7xl my-0 mx-auto columns-3xs'>
      <Carousel autoplay effect="fade">
        <div>
          <h3 style={contentStyle}>1</h3>
        </div>
        <div>
          <h3 style={contentStyle}>2</h3>
        </div>
        <div>
          <h3 style={contentStyle}>3</h3>
        </div>
        <div>
          <h3 style={contentStyle}>4</h3>
        </div>
      </Carousel>
      <div>1</div>
      <div>2</div>
    </div>
  )
}

export default React.memo(BannerProduct);