import {HashRouter as Router, Routes, Route} from 'react-router-dom'
import { useEffect, useState} from 'react';
import Home from './pages/Home';
import DetailPage from './pages/DetailPage';

function App() {
  const [plants, setPlants] = useState([]);

  useEffect(() => {
    fetchPlants()
  }, []);

  const onUpdate = () => {
    fetchPlants()
  }

  const fetchPlants = async () => {
    const response = await fetch("http://10.5.16.152:5000/plants");
    const data = await response.json();
    setPlants(data.plants);
  };

  return (
    <Router>
      <Routes>
        <Route path='/' element={<Home/>}/>
        {/* <Route path='/Detail' element={<DetailPage/>}/> */}
        <Route path="/Detail/:id" element={<DetailPage plants={plants} updateCallback={onUpdate}/>} />
      </Routes>
    </Router>
  );
}

export default App;
