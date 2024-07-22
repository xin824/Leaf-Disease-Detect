import React, { useState } from 'react';
import './EditBox.css';
import wifiIP from '../wifi_ip';

interface Plant {
  id: number;
  ip: string;
  name: string;
  state: string;
  image_path: string;
  update_time: string;
}

interface EditBoxProps {
  plant: Plant | undefined;
  updateCallback: () => void;
}

function EditBox({ plant, updateCallback}: EditBoxProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [plantName, setPlantName] = useState('Unknown');

  const handleEditClick = () => {
    if(plant?.name && plant?.name !== 'Unknown') setPlantName(plant?.name);
    if(isEditing) setIsEditing(false)
    else setIsEditing(true);
  };

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setPlantName(event.target.value);
  };

  // const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
  //   if (event.key === 'Enter') {
  //     setIsEditing(false);
  //   }
  // };

  const handleKeyDown = async (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter') {
      setIsEditing(false);
      await updatePlantName(plant?plant.id:0, plantName); // Call function to update name
    }
  };

  const updatePlantName = async (plantId: number, newName: string) => {
      const url = `${wifiIP}/update_plant/${plantId}`;
      console.log(url)
      const options = {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name: newName })
      };
      console.log(options)

      const response = await fetch(url, options)
        if (response.status !== 201 && response.status !== 200) {
            const data = await response.json()
            alert(data.message)
        } else {
            updateCallback()
        }
    };

  return (
    <div className="row">
      <div className="col">
        {isEditing ? (
          <input
            type="text"
            className="form-control"
            value={plantName}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            onBlur={() => setIsEditing(false)}
            style={{fontSize:'21.6px', fontFamily: 'Outfit-ExtraBold'}}
            size={4}
          />
        ) : (
          <div className="PlantName">{plant?.name?plant.name:'Unknown'}</div>
        )}
      </div>
      <div className="col-auto d-flex justify-content-center align-items-center">
        <button className="editButton" onClick={handleEditClick}></button>
      </div>
    </div>
  );
}

export default EditBox;