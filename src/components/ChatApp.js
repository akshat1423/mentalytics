import React, { useState, useRef, useEffect } from 'react';
import './ChatApp.css';
import { FaRobot, FaUser, FaMicrophone, FaPaperPlane, FaRecordVinyl } from 'react-icons/fa';
import { Link } from 'react-router-dom'; // Import Link for navigation

const ChatApp = ({ query, setQuery, onSend }) => {  // Accept onSend prop
    const [messages, setMessages] = useState([]);
    const [isRecording, setIsRecording] = useState(false);
    const [audioBlob, setAudioBlob] = useState(null);
    const [audioSent, setAudioSent] = useState(false);
    const [transcription, setTranscription] = useState('');
    const token = localStorage.getItem('access_token');
    const mediaRecorderRef = useRef(null);
    const audioChunksRef = useRef([]);
    const [hasPromptedLogin, setHasPromptedLogin] = useState(false); // State to track login prompt

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
            setQuery('');  // Clear input after sending

            if (onSend) onSend();  // Trigger suggestions refresh
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

    const handleSendAudioMessage = async (blob) => {
        if (blob && !audioSent) {
            const formData = new FormData();
            formData.append('audio', blob, 'recording.webm');

            try {
                const response = await fetch('https://akshatgooglehackathon.pythonanywhere.com/api/upload-audio/', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                    },
                    body: formData,
                });

                if (response.ok) {
                    const data = await response.json();
                    setTranscription(data.transcription);
                    setAudioSent(true);
                    setMessages((prevMessages) => [
                        ...prevMessages,
                        { user: true, transcription: data.transcription }
                    ]);

                    await sendMessageToAPI(data.transcription);
                }
            } catch (error) {
                console.error('Error uploading audio:', error);
            }
        }
    };

    useEffect(() => {
        if (audioBlob && !audioSent) {
            handleSendAudioMessage(audioBlob);
            setAudioBlob(null);
        }
    }, [audioBlob, audioSent]);

    const handleMicClick = async () => {
        if (isRecording) {
            mediaRecorderRef.current.stop();
            setIsRecording(false);
        } else {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorderRef.current = new MediaRecorder(stream);
            audioChunksRef.current = [];

            mediaRecorderRef.current.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    audioChunksRef.current.push(event.data);
                }
            };

            mediaRecorderRef.current.onstop = () => {
                const blob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
                if (blob.size > 0) {
                    setAudioBlob(blob);
                }
            };

            mediaRecorderRef.current.start();
            setIsRecording(true);
            setAudioSent(false);
        }
    };

    // Check if user is logged in
    const isLoggedIn = !!token;

    // Add a login prompt message if the user is not logged in and hasn't been prompted yet
    useEffect(() => {
        if (!isLoggedIn && !hasPromptedLogin) {
            setMessages((prevMessages) => [
                ...prevMessages,
                { user: false, text: 'Please <Link to="/login">login</Link> to access this feature.' }
            ]);
            setHasPromptedLogin(true); // Mark as prompted
        }
    }, [isLoggedIn, hasPromptedLogin]);

    return (
        <div className="chat-container">
            <h2 className="chat-recommendation"><FaRobot style={{ marginRight: '8px' }} /> AI Assistant - Menta</h2>
            <div className="chat-window">
                {messages.map((msg, index) => (
                    <div key={index} className={`message-container ${msg.user ? 'user' : 'assistant'}`}>
                        {!msg.user && <div className="icon-container"><FaRobot /></div>}
                        {msg.transcription ? (
                            <div className="transcription-message">
                                <strong>Audio Transcription:</strong> {msg.transcription}
                                <small style={{ display: 'block', fontSize: '0.8em', color: '#999' }}>This is an audio transcribed message.</small>
                            </div>
                        ) : (
                            <div className={`message ${msg.user ? 'user-message' : 'assistant-message'}`}>
                                {msg.text.includes('<Link') ? (
                                    <span dangerouslySetInnerHTML={{ __html: msg.text.replace(/<Link/g, '<a') }} />
                                ) : (
                                    msg.text
                                )}
                            </div>
                        )}
                        {msg.user && <div className="icon-container user-icon"><FaUser /></div>}
                    </div>
                ))}
            </div>
            <div className="input-container">
                <div className={`mic-icon ${isRecording ? 'recording' : ''}`} onClick={handleMicClick}>
                    {isRecording ? <FaRecordVinyl /> : <FaMicrophone />}
                </div>
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
