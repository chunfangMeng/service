import { Carousel, Col, Row } from 'antd';
import React from 'react';

const contentStyle: React.CSSProperties = {
  height: '234px',
  color: '#fff',
  lineHeight: '234px',
  textAlign: 'center',
  background: '#364d79',
};
const BannerProduct: React.FC = () => {
  return (
    <div className='max-w-7xl my-0 mx-auto'>
      <Row gutter={[16, 16]}>
        <Col span={8}>
          <Carousel autoplay effect="fade">
            <div>
              <div style={contentStyle}>1</div>
            </div>
            <div>
              <div style={contentStyle}>2</div>
            </div>
            <div>
              <div style={contentStyle}>3</div>
            </div>
            <div>
              <div style={contentStyle}>4</div>
            </div>
          </Carousel>
        </Col>
        <Col span={16}>
          <div className='grid grid-cols-4 gap-4'>
            <div>1</div>
            <div>2</div>
            <div>3</div>
            <div>4</div>
            <div>5</div>
            <div>6</div>
            <div>7</div>
            <div>8</div>
          </div>
        </Col>
      </Row>
    </div>
  )
}

export default React.memo(BannerProduct);