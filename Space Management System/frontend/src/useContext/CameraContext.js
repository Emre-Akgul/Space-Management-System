import React, { createContext, useState, useContext } from 'react';

const CameraContext = createContext();

export const useCamera = () => useContext(CameraContext);

export const CameraProvider = ({ children }) => {
    const [position, setPosition] = useState([0, 0, 18]);

    const moveCamera = (newPosition) => {
        setPosition(newPosition);
    };

    return (
        <CameraContext.Provider value={{ position, moveCamera }}>
            {children}
        </CameraContext.Provider>
    );
};
