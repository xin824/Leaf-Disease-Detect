import './Solution.css';
import { useState } from 'react';

function Solution() {
    const [isCollapsed, setIsCollapsed] = useState(true);

    const toggleCollapse = () => {
        setIsCollapsed(!isCollapsed);
    };

  return (
    <div className="container-lg my-2">
        <div className="d-flex justify-content-center align-items-center">
            <p className="d-inline-flex gap-1">
                <button className={`btn-solution p-2 px-4 ${isCollapsed ? 'btn-collapsed' : 'btn-expanded'}`}
                        type="button" data-bs-toggle="collapse" onClick={toggleCollapse}
                        data-bs-target="#collapseExample" aria-expanded="false" aria-controls="collapseExample">
                    {isCollapsed?"Solution?":"close"}
                </button>
            </p>
        </div>
        <div className="d-flex justify-content-center align-items-center">
        <div className="collapse col-md-8" id="collapseExample">
            <div className="card card-font text-center p-4 px-5">
                Some placeholder content for the collapse component. This panel is hidden by default but revealed when the user activates the relevant trigger.
                Some placeholder content for the collapse component. This panel is hidden by default but revealed when the user activates the relevant trigger.
                Some placeholder content for the collapse component. This panel is hidden by default but revealed when the user activates the relevant trigger.
            </div>
        </div>
        </div>
        
    </div>
  );
}

export default Solution;
