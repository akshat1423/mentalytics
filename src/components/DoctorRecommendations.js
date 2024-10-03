import React, { useState } from 'react';
import './DoctorRecommendations.css';
import ReactStars from 'react-rating-stars-component'; // Import the library
import placeholderImage from './assets/doctor.png'; // Import the local image
import Button from './Button';
import { faCalendarAlt, faComments, faArrowRight } from '@fortawesome/free-solid-svg-icons';


const doctorsList = [
  {
    name: 'Dr. Aamir Khan',
    specialization: 'Therapist',
    rating: 4.5,
    review: 'Helped me navigate my anxiety and depression, and I feel much better now!',
    image: placeholderImage,
  },
  {
    name: 'Dr. Sarah Lee',
    specialization: 'Clinical Psychologist',
    rating: 4.8,
    review: 'Provided great coping strategies for stress management. Highly recommend!',
    image: placeholderImage,
  },
  {
    name: 'Dr. James Smith',
    specialization: 'Psychiatrist',
    rating: 4.2,
    review: 'Excellent support through tough times, really improved my mental well-being.',
    image: placeholderImage,
  },
];


const DoctorRecommendations = () => {
  const [currentDoctorIndex, setCurrentDoctorIndex] = useState(0);

  const handleNext = () => {
    setCurrentDoctorIndex((prevIndex) => (prevIndex + 1) % doctorsList.length);
  };

  const handlePrev = () => {
    setCurrentDoctorIndex((prevIndex) => 
      (prevIndex - 1 + doctorsList.length) % doctorsList.length
    );
  };

  const doctor = doctorsList[currentDoctorIndex];

  return (
    <div className="card doctor-recommendation">
      <h2>Doctor Recommendations</h2>
      <div className="carousel">
        <button className="carousel-button left" onClick={handlePrev}>
          &#10094;
        </button>
        <div className="doctor-info">
          <img
            src={doctor.image}
            alt={doctor.name}
            className="doctor-image"
          />
          <div className="doctor-details">
            <h3>{doctor.name}</h3>
            <p><strong>{doctor.specialization}</strong></p>
            <div className="doctor-rating">
              <ReactStars
                count={5} // Maximum number of stars
                value={doctor.rating} // The rating value
                size={24} // Size of the stars
                edit={false} // Prevent users from editing
                activeColor="black" // Color for the stars
              />
            </div>
            <p className="doctor-review">
              <em>{doctor.review}</em>
            </p>
           
          </div>
          
        </div>
        <button className="carousel-button right" onClick={handleNext}>
          &#10095;
        </button>
      </div>
      <div className="doctor-actions">
        <Button icon={faCalendarAlt} text="Schedule Appointment" color="#007bff" />
        <Button icon={faComments} text="Chat with Doctor" color="#28a745" />
      </div>
    </div>
  );
};

export default DoctorRecommendations;
