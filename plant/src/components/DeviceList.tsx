import './DeviceList.css';
import ListItem from './ListItem';
import PlantForm from './PlantForm';
import { useState, useEffect } from 'react';

interface Plant {
  id: number;
  ip: string;
  name: string;
  state: string;
  image_path: string;
  update_time: string;
}

interface DeviceListProps {
  plants: Plant[];
  updateCallback: () => void;
}

function DeviceList({plants, updateCallback}: DeviceListProps) {

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
              <ListItem plant={plant} updateCallback={updateCallback}></ListItem>
            ))}
          </div>
        </div>
        <div className="pt-lg-5 pt-2 align-items-center justify-content-center d-flex container-lg">
          <PlantForm updateCallback={updateCallback}></PlantForm>
        </div>
      </div>
    </div>
  );
}

export default DeviceList;
