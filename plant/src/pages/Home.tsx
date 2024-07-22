import '../App.css';
import Header from '../components/Header';
import '../fonts/outfit.css';
import DeviceList from '../components/DeviceList';
import Contact from '../components/Contact';

interface Plant {
  id: number;
  ip: string;
  name: string;
  state: string;
  image_path: string;
  update_time: string;
}

interface HomeProps {
  updateCallback: () => void;
  plants: Plant[];
}

function Home({updateCallback, plants}: HomeProps) {
  return (
    <div className="App">
        <Header></Header>
        <DeviceList plants={plants} updateCallback={updateCallback}></DeviceList>
        <Contact></Contact>
    </div>
  );
}

export default Home;
