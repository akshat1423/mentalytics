import React, { useState, useEffect } from 'react';
import { FaQuestionCircle, FaPlusSquare, FaFileUpload, FaPaperclip, FaUserMd } from 'react-icons/fa'; // Import necessary icons
import ChatApp from './ChatApp';
import spinner from './assets/3d.gif';  // Path to your spinner image

const HealthAssistant = () => {
    const [query, setQuery] = useState(''); // Query to send to ChatApp
    const [suggestedQuestions, setSuggestedQuestions] = useState([]); // List of suggested questions
    const [loading, setLoading] = useState(false); // Loading spinner state

    const token = localStorage.getItem('access_token'); // Retrieve token from localStorage

    // Function to fetch suggested questions
    const fetchSuggestions = async () => {
        setLoading(true); // Start loading
        try {
            const response = await fetch('localhost:8000/api/suggestions/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`, // Add the Authorization header with JWT token
                },
                body: JSON.stringify({}),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();

            // Adjust to match the structure of the response: questions array
            setSuggestedQuestions(data.questions);
        } catch (error) {
            console.error('Error fetching suggestions:', error);
        } finally {
            setLoading(false); // Stop loading
        }
    };

    // Fetch suggestions when the component first loads
    useEffect(() => {
        fetchSuggestions();
    }, []); // Empty dependency array ensures this runs only on mount

    // Function to handle adding suggested question to input field
    const addSuggestedQuestion = (suggestion) => {
        setQuery(suggestion); // Update query with the selected suggested question
    };

    return (
        <div 
            className="card" 
            style={{ 
                padding: '15px', 
                maxWidth: '400px', 
                margin: '0 auto 20px auto', 
                border: '1px solid #ddd', 
                borderRadius: '8px', 
                boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)' 
            }}
        >
            {/* Title */}
            <h2 style={{ textAlign: 'center', marginBottom: '15px' }}>
                Health Assistant <FaQuestionCircle />
            </h2>
            
            {/* Pass down query state and fetchSuggestions as props to ChatApp */}
            <ChatApp 
                query={query}  // Pass the updated query to ChatApp
                setQuery={setQuery}  // Allow ChatApp to update the query as well
                onSend={() => fetchSuggestions()} // Trigger suggestions when sending chat
            />

            {/* Suggested questions */}
            <div style={{ marginBottom: '15px' }}>
                <h4 style={{ marginBottom: '10px' }}>Suggested Questions</h4>
                
                {loading ? (
                    // Display loading spinner in the center when loading
                    <div style={{ textAlign: 'center' }}>
                        <img src={spinner} alt="Loading..." style={{ width: '50px', animation: 'spin 1s linear infinite' }} />
                    </div>
                ) : (
                    <ul style={{ listStyleType: 'none', paddingLeft: '0' }}>
                        {suggestedQuestions.map((suggestion, index) => (
                            <li 
                                key={index} 
                                style={{ 
                                    display: 'flex', 
                                    justifyContent: 'space-between', 
                                    alignItems: 'center', 
                                    padding: '10px', 
                                    borderBottom: '1px solid #ddd' 
                                }}
                            >
                                <span>{suggestion}</span>
                                <button 
                                    style={{ 
                                        padding: '5px', 
                                        backgroundColor: '#28a745', 
                                        color: '#fff', 
                                        border: 'none', 
                                        borderRadius: '4px', 
                                        width: '40px', 
                                        display: 'flex', 
                                        justifyContent: 'center', 
                                        alignItems: 'center'
                                    }}
                                    onClick={() => addSuggestedQuestion(suggestion)}
                                >
                                    <FaPlusSquare />
                                </button>
                            </li>
                        ))}
                    </ul>
                )}
            </div>

            {/* File upload and attach buttons */}
            {/* <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '15px' }}>
                <button 
                    style={{ 
                        flex: 1, 
                        marginRight: '10px', 
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
                    <FaFileUpload style={{ marginRight: '8px' }} /> Choose file
                </button>
                <button 
                    style={{ 
                        flex: 1, 
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
                    <FaPaperclip style={{ marginRight: '8px' }} /> Attach
                </button>
            </div> */}

            {/* Connect with live doctor button */}
            {/* <div style={{ display: 'flex', justifyContent: 'center' }}>
                <button 
                    style={{ 
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
                    <FaUserMd style={{ marginRight: '8px' }} /> Connect with Live Doctor
                </button>
            </div> */}
        </div>
    );
};

export default HealthAssistant;
