
import Hero from '@/components/sections/Hero';
import Resources from '@/components/sections/Resources';
import Solutions from '@/components/sections/Solutions';
import Navbar from '../components/layout/Navbar';
import Footer from '../components/layout/Footer';
// import ExploreAtlas from '../components/sections/ExploreAtlas';
// import Pricing from '@/components/sections/Pricing';
// import About from '@/components/sections/About';


export default function LandingPage() {
  return (
    <div>
      <Navbar />
      <Hero />
      <Resources />
      <Solutions />
      <Footer />
      {/* <ExploreAtlas />
      <Pricing />
      <About /> */}
    </div>
  );
}
