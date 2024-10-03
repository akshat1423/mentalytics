import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FaUser } from 'react-icons/fa';
import Cookies from 'js-cookie'; // Import js-cookie for cookie management

const Login = ({ setUserId }) => {
    const [userId, setUserIdLocal] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
    
        const response = await fetch('https://akshatgooglehackathon.pythonanywhere.com/api/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user_id: userId, password }),
        });
    
        if (response.ok) {
            const data = await response.json();
    
            // Store the access and refresh tokens in localStorage or cookies
            localStorage.setItem('access_token', data.access);
            localStorage.setItem('refresh_token', data.refresh);
            localStorage.setItem('name', data.user_name);
    
            setUserId(data.user_id);  // Set the user ID in your state
            navigate('/');  // Redirect to dashboard or home page
        } else {
            console.error('Login failed');
        }
    };
    
    return (
        <div 
            style={{
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                height: '100vh', // Full screen height
                padding: '20px',  // Padding for smaller screen adjustments
            }}
        >
            <div 
                className="card" 
                style={{ 
                    width: '100%',
                    maxWidth: '400px', 
                    padding: '20px', 
                    border: '1px solid #ddd', 
                    borderRadius: '8px', 
                    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)', 
                    backgroundColor: '#fff'
                }}
            >
                <h2 style={{ textAlign: 'center', marginBottom: '15px' }}>
                    Login <FaUser />
                </h2>

                <form onSubmit={handleLogin}>
                    <input
                        type="text"
                        placeholder="User ID"
                        value={userId}
                        onChange={(e) => setUserIdLocal(e.target.value)}
                        required
                        style={{ 
                            width: '100%', 
                            padding: '10px', 
                            marginBottom: '15px', 
                            borderRadius: '6px', 
                            border: '1px solid #ccc' 
                        }}
                    />
                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        style={{ 
                            width: '100%', 
                            padding: '10px', 
                            marginBottom: '15px', 
                            borderRadius: '6px', 
                            border: '1px solid #ccc' 
                        }}
                    />
                    <button 
                        type="submit"
                        style={{ 
                            width: '100%', 
                            padding: '10px', 
                            backgroundColor: '#28a745', 
                            color: '#fff', 
                            border: 'none', 
                            borderRadius: '6px', 
                            display: 'flex', 
                            justifyContent: 'center', 
                            alignItems: 'center' 
                        }}
                    >
                        <FaUser style={{ marginRight: '8px' }} /> Login
                    </button>
                </form>
            </div>
        </div>
    );
};

export default Login;
