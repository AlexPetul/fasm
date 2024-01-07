import React from 'react';
import "./Spinner.css"

const Spinner = () => {
    return (
        <div className="overlay" id="overlay">
            <div className="spinner"></div>
        </div>
    );
};
export default Spinner;