import {HashRouter as Router, Routes, Route} from 'react-router-dom'
import { useEffect, useState} from 'react';
import Home from './pages/Home';
import DetailPage from './pages/DetailPage';
import wifiIP from './wifi_ip'

function App() {
  const [plants, setPlants] = useState([]);

  useEffect(() => {
    fetchPlants()

    const interval = setInterval(() => {
      onUpdate();
    }, 10000);

    return () => clearInterval(interval);
  }, []);

  const onUpdate = () => {
    fetchPlants()
  }

  const fetchPlants = async () => {
    const response = await fetch(`${wifiIP}/plants`);
    const data = await response.json();
    console.log(`${wifiIP}/plants`)
    setPlants(data.plants);
  };

  return (
    <Router>
      <Routes>
        <Route path='/' element={<Home  plants={plants} updateCallback={onUpdate}/>}/>
        {/* <Route path='/Detail' element={<DetailPage/>}/> */}
        <Route path="/Detail/:id" element={<DetailPage plants={plants} updateCallback={onUpdate}/>} />
      </Routes>
    </Router>
  );
}

export default App;
