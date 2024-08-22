import './Solution.css';
import { useState } from 'react';

interface Plant {
    id: number;
    ip: string;
    name: string;
    state: string;
    image_path: string;
    update_time: string;
  }
  
interface SolutionProps{
    plant: Plant | undefined;
  }

function Solution({plant}:SolutionProps){
    const [isCollapsed, setIsCollapsed] = useState(true);

  const toggleCollapse = () => {
    setIsCollapsed(!isCollapsed);
  };
  
  const sol_gen = (d:string) => {
    switch(d){
        case 'blight':
            return 'Blight is a plant disease causing rapid decay of leaves, stems, and fruits, often characterized by dark, sunken lesions. To manage blight, remove and discard affected plant parts. Improve air circulation and avoid overhead watering to keep foliage dry. Apply fungicides as needed, and ensure proper sanitation of tools and garden equipment. Monitor nearby plants to prevent spread and consider rotating crops to minimize recurrence.';
        case 'citrus':
            return 'Citrus diseases affect leaves, stems, and fruits, causing lesions, discoloration, and poor growth. To manage these diseases, prune and remove infected parts, ensuring proper disposal. Use copper-based fungicides as needed and maintain good air circulation around the plant. Avoid overhead watering and regularly clean gardening tools. Monitor the plant closely and consider soil and nutrient adjustments for overall health.';
        case 'measles':
            return 'Measles in plants, often a term for various viral or fungal diseases, causes spots and lesions on leaves and stems. To manage it, remove and dispose of affected plant parts. Ensure good air circulation and avoid overhead watering. Apply appropriate fungicides if fungal. Regularly inspect and clean tools to prevent spread. Maintain overall plant health with proper watering and nutrients.';
        case 'mildew':
            return 'Mildew is a fungal disease that appears as white or grayish powder on leaves, stems, and buds. It thrives in warm, dry environments with poor air circulation. To treat mildew, remove affected plant parts and improve air flow around the plant. Avoid overhead watering to keep foliage dry. Apply a fungicide labeled for mildew if necessary. Maintain proper watering and humidity levels to prevent recurrence.';
        case 'mite':
            return 'Mites are tiny pests that can cause damage to plants by sucking out plant fluids, leading to stippling, discoloration, and leaf drop. If your plant has mites, wash the leaves with water to dislodge them. Use insecticidal soap or neem oil to treat infestations. Increase humidity around the plant to make the environment less favorable for mites. Regularly inspect your plant and remove any heavily infested areas to prevent spread.';
        case 'mold':
            return 'Mold is a fungal disease that appears as fuzzy, white, or grayish growth on plant surfaces. It thrives in high humidity and poor air circulation. To manage mold, remove and dispose of affected plant parts. Increase air flow around the plant and avoid overwatering. Clean the surrounding area and sanitize tools. Apply a fungicide if necessary and consider using a dehumidifier to lower humidity levels.';
        case 'rot':
            return 'Rot is a plant disease caused by fungal or bacterial pathogens that leads to the decay of plant tissues, often appearing as soft, discolored areas. To manage rot, remove and discard affected parts of the plant. Ensure proper drainage and avoid overwatering. Improve air circulation around the plant and consider repotting it in fresh, well-draining soil. Apply appropriate fungicides or bactericides if necessary and regularly monitor the plant for further signs of decay.';
        case 'rust':
            return 'Rust is a fungal disease causing orange, reddish, or brown pustules on leaves, stems, and buds. It can weaken plants and reduce yields. To manage rust, remove and discard affected plant parts. Improve air circulation and avoid overhead watering. Apply a fungicide designed for rust. Ensure proper spacing between plants and regularly inspect them to catch early signs.';
        case 'scab':
            return 'Scab is a plant disease that causes rough, sunken lesions on leaves, stems, and fruits. To manage scab, remove and destroy affected plant parts. Improve air circulation and avoid overhead watering. Apply fungicides that target scab pathogens. Maintain a clean garden by removing debris and using disease-resistant plant varieties if available. Regularly inspect plants to catch issues early.';
        case 'scorch':
            return 'Scorch is a plant disease characterized by the browning or burning of leaf edges, often due to environmental stress like excessive heat or drought. To manage scorch, ensure your plant receives adequate water and avoid watering during the hottest part of the day. Provide shade to protect from intense sunlight and improve soil moisture. Increase air circulation around the plant and avoid using high-nitrogen fertilizers. Prune damaged leaves to reduce stress on the plant.';
        case 'spot':
            return 'Plant spot diseases are characterized by small, discolored spots on leaves, stems, or fruits. These spots can be caused by fungi, bacteria, or environmental conditions. To manage plant spots, remove and dispose of affected plant parts. Improve air circulation and avoid overhead watering. Apply appropriate fungicides or bactericides based on the disease. Maintain proper watering and fertilization practices, and monitor your plants regularly to catch any new outbreaks early.';
        case 'virus':
            return 'Plant viruses cause various symptoms, including leaf discoloration, stunted growth, and poor fruit development. They spread through insects, tools, or contaminated soil. If your plant has a virus, remove and destroy infected plants to prevent spread. Avoid overhead watering and use clean tools. Control pests that can transmit viruses and consider using disease-resistant plant varieties. Maintain proper plant care to strengthen the remaining healthy plants.';
        case 'No leaf':
            return 'Please adjust your camera; there are no leaves visible.';
        default:
            return 'Your plant is healthy!';
    }
    }

  return (
    <div className="container-lg my-2">
      <div className="d-flex justify-content-center align-items-center">
        <p className="d-inline-flex gap-1">
          <button
            className={`btn-solution p-2 px-4 ${isCollapsed ? 'btn-collapsed' : 'btn-expanded'}`}
            type="button"
            data-bs-toggle="collapse"
            onClick={toggleCollapse}
            data-bs-target="#collapseExample"
            aria-expanded={!isCollapsed}
            aria-controls="collapseExample"
          >
            {isCollapsed ? "Solution?" : "Close"}
          </button>
        </p>
      </div>
      <div className="d-flex justify-content-center align-items-center">
        <div className={`collapse col-md-8 ${isCollapsed ? '' : 'show'}`} id="collapseExample">
          <div className="card card-font text-center p-4 px-5">
            {plant ? sol_gen(plant?.state.slice(3)) : 'Refresh to get solution'}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Solution;
