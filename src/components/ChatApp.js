import React, { useState, useRef, useEffect } from 'react';
import './ChatApp.css';
import { FaRobot, FaUser, FaMicrophone, FaPaperPlane, FaRecordVinyl } from 'react-icons/fa';

const ChatApp = ({ query, setQuery, onSend }) => {
    const [messages, setMessages] = useState([]);
    const [isRecording, setIsRecording] = useState(false);
    const [audioBlob, setAudioBlob] = useState(null);
    const [audioSent, setAudioSent] = useState(false);
    const [transcription, setTranscription] = useState('');
    const token = localStorage.getItem('access_token');
    const mediaRecorderRef = useRef(null);
    const audioChunksRef = useRef([]);
    const [hasPromptedLogin, setHasPromptedLogin] = useState(false);

    useEffect(() => {
        return () => {
            if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
                mediaRecorderRef.current.stop();
            }
        };
    }, []);

    const handleSendTextMessage = async () => {
        if (query) {
            setMessages((prevMessages) => [
                ...prevMessages,
                { user: true, text: query }
            ]);
            await sendMessageToAPI(query);
            setQuery('');  // Clear the input field after sending
            if (onSend) onSend();  // Trigger the onSend function to fetch new suggestions
        }
    };

    const sendMessageToAPI = async (message) => {
        const token = localStorage.getItem('access_token');
        try {
            const response = await fetch('https://akshatgooglehackathon.pythonanywhere.com/api/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
                body: JSON.stringify({ query: message }),
            });

            if (!response.ok) {
                throw new Error('Error sending message');
            }

            const data = await response.json();
            setMessages((prevMessages) => [
                ...prevMessages,
                { user: false, text: data.response }
            ]);
        } catch (error) {
            console.error('Error sending message:', error);
        }
    };

    return (
        <div className="chat-container">
            <h2 className="chat-recommendation"><FaRobot style={{ marginRight: '8px' }} /> AI Assistant - Menta</h2>
            <div className="chat-window">
                {messages.map((msg, index) => (
                    <div key={index} className={`message-container ${msg.user ? 'user' : 'assistant'}`}>
                        {!msg.user && <div className="icon-container"><FaRobot /></div>}
                        <div className={`message ${msg.user ? 'user-message' : 'assistant-message'}`}>
                            {msg.text}
                        </div>
                        {msg.user && <div className="icon-container user-icon"><FaUser /></div>}
                    </div>
                ))}
            </div>
            <div className="input-container">
                <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    onKeyDown={(e) => { if (e.key === 'Enter') handleSendTextMessage(); }}
                    placeholder="Ask a question..."
                />
                <button className="chat-btn" onClick={handleSendTextMessage}>
                    <FaPaperPlane />
                </button>
            </div>
        </div>
    );
};

export default ChatApp;
