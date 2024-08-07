import PlantCard from "../components/PlantCard";
import '../App.css'
import { useNavigate, useParams} from "react-router-dom";
import Solution from "../components/Solution";

interface Plant {
    id: number;
    ip: string;
    name: string;
    state: string;
    image_path: string;
    update_time: string;
}

interface DetailPageProps {
    plants: Plant[];
    updateCallback: () => void;
    wifiIp: string;
}

const DetailPage: React.FC<DetailPageProps> = ({ plants, updateCallback, wifiIp}) => {

    const navigate = useNavigate();

    const handleNavigate = () => {
        navigate('/');
    };

    const { id } = useParams<{ id: string }>();
    const plant = plants.find((p) => p.id === parseInt(id || '0'));

    const onUpdate = () => {
        updateCallback();
    }

  return (
    <div className="PlantDetailBg">
        <div className="PlantDetailComs">
            <div className="container-sm mt-5">
                <div className="d-flex align-items-center justify-content-start">
                    <button className="backButton" onClick={handleNavigate}></button>
                </div>
            </div>
            
            <PlantCard plant={plant} updateCallback={onUpdate} wifiIp = {wifiIp}></PlantCard>
            <Solution plant={plant}></Solution>
        </div>
    </div>
  );
}

export default DetailPage;
