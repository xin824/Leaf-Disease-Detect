import '../App.css';
import Header from '../components/Header';
import '../fonts/outfit.css';
import DeviceList from '../components/DeviceList';
import Contact from '../components/Contact';

function Home() {
  return (
    <div className="App">
        <Header></Header>
        <DeviceList></DeviceList>
        <Contact></Contact>
    </div>
  );
}

export default Home;
