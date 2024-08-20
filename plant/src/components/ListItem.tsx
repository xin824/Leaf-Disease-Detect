import './ListItem.css';
import { useNavigate } from 'react-router-dom';
import { useEffect, useState, useRef } from 'react';

interface Plant {
  id: number;
  ip: string;
  name: string;
  state: string;
  image_path: string;
  update_time: string;
}

interface ListItemProps {
  plant: Plant;
  updateCallback: () => void;
  wifiIp: string;
}

function ListItem({ plant, updateCallback, wifiIp}: ListItemProps) {

  const navigate = useNavigate();
  const [progressValue, setProgressValue] = useState(0);
  const progressRef = useRef(null);

  useEffect(() => {
    const handleScroll = () => {
      if (isInViewport(progressRef.current)) {
        setProgressValue(parseInt(plant.update_time, 10));
        window.removeEventListener('scroll', handleScroll);
      }
      if(progressValue!=0){
        const interval = setInterval(() => {
          setProgressValue(parseInt(plant.update_time, 10));
          console.log('fetch')
        }, 10000);
      }
    };

    window.addEventListener('scroll', handleScroll);

    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  const isInViewport = (element: HTMLElement | null): boolean => {
    if (!element) return false;
  
    const rect = element.getBoundingClientRect();
  
    return (
      rect.top >= 0 &&
      rect.left >= 0 &&
      rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
      rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
  };

  const handleNavigate = () => {
    navigate(`/Detail/${plant.id}`);
    // navigate('/Detail', { state: { plant } });
  };

  const onDelete = async (id:number) => {
    try {
        const options = {
            method: "DELETE"
        }
        const response = await fetch(`${wifiIp}/delete_plant/${id}`, options)
        if (response.status === 200) {
            updateCallback()
        } else {
            console.error("Failed to delete")
        }
    } catch (error) {
        alert(error)
    }
  }

  return (
    <div className="container-lg my-4">
        <div className="d-flex align-items-end justify-content-center">
            {/* <img src={connect} className="img-fluid col-1" alt="connect"/> */}
            {plant.image_path === 'connect' && (
              <button className="deleteButton" onClick={() => onDelete(plant.id)}></button>
            )}
            {plant.image_path === 'disconnect' && (
              <button className="deleteButtonUn" onClick={() => onDelete(plant.id)}></button>
            )}
            {/* <button className="deleteButtonUn" onClick={() => onDelete(plant.id)}></button> */}
            <div className="col px-3">
                <div className='FontName'>{plant.name?plant.name:'Unknown'}</div>
                <div className="progress" role="progressbar" aria-label="progressbar" 
                     aria-valuenow={parseInt(plant.update_time, 10)} aria-valuemin={0} aria-valuemax={100}
                     ref={progressRef}>
                    <div className="progress-bar"
                         style={{ width: `${plant?.state.slice(0,3)}%`, backgroundColor: '#708F73' }}
                    ></div>
                </div>
            </div> 
            <button className="goButton" onClick={handleNavigate}></button>
        </div>
    </div>
  );
}

export default ListItem;
