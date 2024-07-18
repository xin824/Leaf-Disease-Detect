import React, { useState } from 'react';
import { Modal, Button, Form } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import './PlantForm.css'

interface PlantFormProps {
    updateCallback: () => void;
}

const PlantForm: React.FC<PlantFormProps> = ({ updateCallback }) => {
    const [show, setShow] = useState(false);
    const [ip, setIp] = useState('');
    const [state, setState] = useState('');
    const [update_time, setProgress] = useState('');
    const [image_path, setImage] = useState('');

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();

        const data = {
            ip,
            state,
            update_time,
            image_path,
        };

        const url = "http://10.5.16.152:5000/create_plant";

        const options = {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        };

        const response = await fetch(url, options);
        if (response.status !== 201 && response.status !== 200) {
            const data = await response.json();
            alert(data.message);
        } else {
            updateCallback();
        }

        setIp('');
        setState('');
        setProgress('');
        setImage('');
        handleClose();
    };

    return (
        <>
            <Button className = 'formButton' variant="primary" onClick={handleShow}>
                Add Device
            </Button>

            <Modal show={show} onHide={handleClose}>
                <Modal.Header closeButton>
                    <Modal.Title>Add Plant</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form onSubmit={handleSubmit}>
                        <Form.Group controlId="formIp">
                            <Form.Label>IP Address</Form.Label>
                            <Form.Control
                                type="text"
                                value={ip}
                                onChange={(e) => setIp(e.target.value)}
                                required
                            />
                        </Form.Group>
                        <Form.Group controlId="formState">
                            <Form.Label>Disease</Form.Label>
                            <Form.Control
                                type="text"
                                value={state}
                                onChange={(e) => setState(e.target.value)}
                                required
                            />
                        </Form.Group>
                        <Form.Group controlId="formProgress">
                            <Form.Label>Progress 1-100</Form.Label>
                            <Form.Control
                                type="text"
                                value={update_time}
                                onChange={(e) => setProgress(e.target.value)}
                                required
                            />
                        </Form.Group>
                        <Form.Group controlId="formImagePath">
                            <Form.Label>Connection</Form.Label>
                            <Form.Control
                                type="text"
                                value={image_path}
                                onChange={(e) => setImage(e.target.value)}
                                required
                            />
                        </Form.Group>
                        <Button className = 'formButton mt-3' variant="primary" type="submit">
                            Submit
                        </Button>
                    </Form>
                </Modal.Body>
            </Modal>
        </>
    );
};

export default PlantForm;
