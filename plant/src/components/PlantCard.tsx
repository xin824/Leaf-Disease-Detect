import './PlantCard.css'
import EditBox from './EditBox';
import { useEffect, useState, useRef } from 'react';

interface Plant {
    id: number;
    ip: string;
    name: string;
    state: string;
    image_path: string;
    update_time: string;
  }
  
  interface PlantCardProps {
    plant: Plant | undefined;
    updateCallback: () => void;
    wifiIp: string;
  }
  
function useInterval(callback: () => void, delay: number|null) {
  const savedCallback = useRef<() => void>();

  // Remember the latest callback.
  useEffect(() => {
    savedCallback.current = callback;
  }, [callback]);

  // Set up the interval.
  useEffect(() => {
    if(delay !== null) {
	    let id = setInterval(() => {
		if(savedCallback.current) {
	      	savedCallback.current();
	      	}
	    }, delay);
	    return () => clearInterval(id);
	    }
	  }, [delay]);
   }

function PlantCard({ plant, updateCallback, wifiIp}: PlantCardProps) {
    const [progressValue, setProgressValue] = useState(0);
    const [updateTime, setUpdateTime] = useState('Refresh to load last updated time');
    const [key, setKey] = useState(new Date().getSeconds());


    useInterval(() => {
    	if(key + 0.25 < 60){
    	  setKey(key + 0.25);
    	}else{
    	  setKey(0.0);
    	}
	  
	}, 250);
	console.log(key)
    //console.log(new Date())
    //console.log("key: ", `./image/${plant?.ip}/${key.toFixed(1)}.jpg`)
    
    /**async function fetchImageLastModified(imageName: string): Promise<string | null> {
        try {
            const response = await fetch(`${wifiIp}/update_time/${encodeURIComponent(imageName)}`);
            if (response.ok) {
                const data = await response.json();
                return data.lastModified;
            } else {
                throw new Error('Failed to fetch image last modified time');
            }
        } catch (error) {
            console.error('Error fetching image last modified time:', error);
            return null;
        }
    }
    **/

  return (
    // <div className="container-fluid" style={{backgroundColor: "#405F43", height: '100vh'}}>
        <div className="d-flex container-xl justify-content-center align-items-center">
            <div className="card m-5 p-md-4 p-5">
                <div className="row g-0">
                    <div className="col-md-4 d-flex justify-content-center align-items-center">
                        {/* <img src={`./image/${plant?.ip}/${(new Date().getSeconds() + ((new Date().getMilliseconds() > 500)?0.5:0)).toFixed(1).toString()}.jpg`} className="img-fluid plantPicture" alt="plant picture"/>*/}
                        {/* <img src={`../../image/${plant?.ip}.jpg`} className="img-fluid plantPicture" alt="plant picture"/> */}
                        <img src={`./image/${plant?.ip}/${key.toFixed(2)}.jpg`} className="img-fluid plantPicture" alt="plant picture"/>
                    </div>
                    <div className="col-md-8 p-2">
                        <div className="card-body">
                            <EditBox plant={plant} updateCallback={updateCallback} wifiIp = {wifiIp}></EditBox>
                            <div className='PlantState'>{plant?.state}</div>
                            <div className="progress progress-cus2" role="progressbar" aria-label="progressbar" 
                                aria-valuenow={progressValue} aria-valuemin={0} aria-valuemax={100}>
                                <div className="progress-bar" style={{ width: `50%`, backgroundColor: '#92BA96', borderRadius: '50px'}}></div>
                            </div>
                            <p className="card-text">
                                <small className="font-time justify-content-end d-flex">Last updated: {plant?.update_time}</small>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    // </div>
  );
}

export default PlantCard;
