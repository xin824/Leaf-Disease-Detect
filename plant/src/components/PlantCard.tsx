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
    const [imgURL, setImgURL] = useState(`./image/${plant?.ip}/annotation.jpg`);
    useInterval(() => {
    
    	const timestamp = new Date().getTime()
  	setImgURL(`./image/${plant?.ip}/annotation.jpg?t=${timestamp}`)
	  
	}, 300);

    console.log(imgURL)
  
  return (
    // <div className="container-fluid" style={{backgroundColor: "#405F43", height: '100vh'}}>
        <div className="d-flex container-xl justify-content-center align-items-center">
            <div className="card m-5 p-md-4 p-5">
                <div className="row g-0">
                    <div className="col-md-4 d-flex justify-content-center align-items-center">
                        {/* <img src={`./image/${plant?.ip}/${(new Date().getSeconds() + ((new Date().getMilliseconds() > 500)?0.5:0)).toFixed(1).toString()}.jpg`} className="img-fluid plantPicture" alt="plant picture"/>*/}
                        {/* <img src={`../../image/${plant?.ip}.jpg`} className="img-fluid plantPicture" alt="plant picture"/> */}
                        <img src={imgURL} className="img-fluid plantPicture" alt="plant picture"/>
                    </div>
                    <div className="col-md-8 p-2">
                        <div className="card-body">
                            <EditBox plant={plant} updateCallback={updateCallback} wifiIp = {wifiIp}></EditBox>
                            <div className='PlantState'>{plant?.state.slice(3)}</div>
                            <div className="progress progress-cus2" role="progressbar" aria-label="progressbar" 
                                aria-valuenow={progressValue} aria-valuemin={0} aria-valuemax={100}>
                                <div className="progress-bar" style={{ width: `${plant?.state.slice(0,3)}%`, backgroundColor: '#92BA96', borderRadius: '50px'}}></div>
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
