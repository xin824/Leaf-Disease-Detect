import {HashRouter as Router, Routes, Route} from 'react-router-dom'
import { useEffect, useState} from 'react';
import Home from './pages/Home';
import DetailPage from './pages/DetailPage';

function App() {
  const [plants, setPlants] = useState([]);
  const [ip, setIp] = useState('');
  var wifiIp = ''

  useEffect(() => {
    fetch(`${process.env.PUBLIC_URL}/wifi_ip.txt`)
      .then(response => response.text())
      .then(data => {
        wifiIp = data;
      })
      .then( () => {
        onUpdate();
      })
      
      .catch(error => {
        console.error('Error fetching the text file:', error);
      });

    const interval = setInterval(() => {
      onUpdate();
    }, 200);

    return () => clearInterval(interval);
  }, []);

  const onUpdate = () => {
    fetchPlants()
  }

  const fetchPlants = async () => {
    const response = await fetch(`${wifiIp}/plants`);
    const data = await response.json();
    setPlants(data.plants);
  };

  return (
    <Router>
      <Routes>
        <Route path='/' element={<Home  plants={plants} updateCallback={onUpdate} wifiIp = {wifiIp}/>}/>
        {/* <Route path='/Detail' element={<DetailPage/>}/> */}
        <Route path="/Detail/:id" element={<DetailPage plants={plants} updateCallback={onUpdate} wifiIp = {wifiIp}/>} />
      </Routes>
    </Router>
  );
}

export default App;
