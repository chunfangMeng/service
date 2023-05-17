import BannerProduct from '@/components/Home/BannerProduct'


export default function Home() {
  return (
    <div>
      <BannerProduct />
    </div>
  )
}

export async function getStaticProps() {
  return {
    props: {
      
    }
  }
}
