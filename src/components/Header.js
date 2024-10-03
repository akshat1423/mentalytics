import React from 'react';
import logo from './assets/logo.png';  // Path to your logo
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUser } from '@fortawesome/free-solid-svg-icons';
import { Link } from 'react-router-dom';  // Make sure you have react-router-dom installed

const Header = ({ name }) => (
    <div className="header">
        <img src={logo} alt="Wearlytics Logo" className="logo" />
        <h2>
            <FontAwesomeIcon icon={faUser} /> Welcome to Mentalytics, {name}
        </h2>
        {name !== "Guest" ? (
            <button className="header-button">
                <FontAwesomeIcon icon={faUser} /> Profile
            </button>
        ) : (
            <div style={{ display: "flex", justifyContent: "space-between", width: "300px" }}> {/* Adjust width as needed */}
            <Link to="/login" style={{ flex: 1, marginRight: "10px" }}> {/* Space between buttons */}
                <button className="header-button" style={{ width: "100%" }}>Login</button>
            </Link>
            <Link to="/register" style={{ flex: 1, marginLeft: "10px" }}>
                <button className="header-button" style={{ width: "100%" }}>Register</button>
            </Link>
        </div>
        )}
    </div>
);

export default Header;
