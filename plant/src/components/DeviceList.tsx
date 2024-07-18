import './DeviceList.css';
import ListItem from './ListItem';
import PlantForm from './PlantForm';
import { useState, useEffect } from 'react';

function DeviceList() {
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
    <div className="container-lg mt-5 mb-5">
      <div className="mt-5 mb-5">
        <div className="text-center">
          <div className="font">Device List</div>
        </div>
        <div className="row my-3 align-items-center justify-content-center">
          <div className="col-10 col-md-9">
            {/* <ListItem></ListItem> */}
            {plants.map((plant) => (
              <ListItem plant={plant} updateCallback={onUpdate}></ListItem>
            ))}
          </div>
        </div>
        <div className="pt-lg-5 pt-2 align-items-center justify-content-center d-flex container-lg">
          <PlantForm updateCallback={onUpdate}></PlantForm>
        </div>
      </div>
    </div>
  );
}

export default DeviceList;
