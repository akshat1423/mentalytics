import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FaUser } from 'react-icons/fa'; // Import necessary icons

const Signup = () => {
    const [name, setName] = useState('');
    const [userId, setUserId] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleSignup = async (e) => {
        e.preventDefault();

        const response = await fetch('http://localhost:8000/api/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name, user_id: userId, password }),
        });

        if (response.ok) {
            navigate('/login'); // Navigate to login on success
        } else {
            console.error('Signup failed');
        }
    };

    return (
        <div 
            style={{
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                height: '100vh', // Full screen height for vertical centering
                padding: '20px',  // Padding for responsiveness
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
                    Signup  <FaUser style={{ marginRight: '8px' }} />
                </h2>

                <form onSubmit={handleSignup}>
                    <input
                        type="text"
                        placeholder="Name"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
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
                        type="text"
                        placeholder="User ID"
                        value={userId}
                        onChange={(e) => setUserId(e.target.value)}
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
                    ><FaUser style={{ marginRight: '8px' }} />
                        Signup
                    </button>
                </form>
            </div>
        </div>
    );
};

export default Signup;
