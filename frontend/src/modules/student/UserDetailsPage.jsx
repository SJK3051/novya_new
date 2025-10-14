

//// UserDetailsPage.jsx
import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { FaCamera, FaEdit, FaSave } from "react-icons/fa";
import "./UserDetailsPage.css";
import { API_CONFIG, djangoAPI } from "../../config/api";

const UserDetailsPage = () => {
  const navigate = useNavigate();
  const [userData, setUserData] = useState(null);
  const [editMode, setEditMode] = useState(false);
  const [tempAvatar, setTempAvatar] = useState(null);

  // Fetch user data based on role
  useEffect(() => {
    const fetchUserData = async () => {
      const userRole = localStorage.getItem("userRole"); // "student" or "parent"
      const userToken = localStorage.getItem("userToken");
      
      console.log('🔍 Debug - UserDetailsPage loading data...');
      console.log('🔍 Debug - User role:', userRole);
      console.log('🔍 Debug - User token exists:', !!userToken);
      
      try {
        // Try to fetch fresh data from backend first
        if (userToken) {
          console.log('🔍 Debug - Fetching fresh data from backend...');
          const response = await djangoAPI.get(API_CONFIG.DJANGO.AUTH.USER_PROFILE);
          console.log('🔍 Debug - Backend profile data:', response);
          
          if (response && response.user) {
            const backendData = {
              firstName: response.user.firstname || 'User',
              lastName: response.user.lastname || 'Name',
              email: response.user.email || 'user@example.com',
              userName: response.user.username || 'username',
              phone: response.user.phonenumber || '',
              role: userRole || 'student',
              address: response.user.address || '',
              ...(userRole === 'student' && {
                grade: response.user.grade || '',
                course: response.user.course || '',
                parentEmail: response.user.parent_email || '',
                parentName: response.user.parent_name || '',
                parentPhone: response.user.parent_phone || ''
              })
            };
            
            console.log('🔍 Debug - Using backend data:', backendData);
            setUserData(backendData);
            
            // Update localStorage with fresh data
            if (userRole === "student") {
              localStorage.setItem("studentData", JSON.stringify(backendData));
            } else {
              localStorage.setItem("parentData", JSON.stringify(backendData));
            }
            return;
          }
        }
      } catch (error) {
        console.error('❌ Error fetching from backend:', error);
        // Fall through to localStorage fallback
      }
      
      // Fallback to localStorage data
      let storedData = null;
      if (userRole === "student") {
        storedData = localStorage.getItem("studentData");
      } else if (userRole === "parent") {
        storedData = localStorage.getItem("parentData");
      }

      console.log('🔍 Debug - Stored data exists:', !!storedData);
      
      if (storedData) {
        try {
          const parsedData = JSON.parse(storedData);
          console.log('🔍 Debug - Parsed user data:', parsedData);
          setUserData(parsedData);
        } catch (error) {
          console.error('❌ Error parsing stored data:', error);
          // Fallback: create basic user data from available info
          const fallbackData = {
            firstName: "User",
            lastName: "Name",
            email: "user@example.com",
            role: userRole || "student",
            userName: "username"
          };
          console.log('🔍 Debug - Using fallback data:', fallbackData);
          setUserData(fallbackData);
        }
      } else {
        // No stored data - create fallback data
        console.log('🔍 Debug - No stored data found, creating fallback');
        const fallbackData = {
          firstName: "User",
          lastName: "Name", 
          email: "user@example.com",
          role: userRole || "student",
          userName: "username"
        };
        setUserData(fallbackData);
      }
    };

    fetchUserData();
  }, []);

  // Logout function
 const handleLogout = () => {
  // ❌ Do NOT remove studentData/parentData here
  localStorage.removeItem("userRole"); 
  localStorage.removeItem("userToken");
  navigate("/");
};


  // Input change
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setUserData((prev) => ({ ...prev, [name]: value }));
  };

  // Save updated data
  const handleSave = async () => {
    try {
      // Check authentication first
      const token = localStorage.getItem('userToken');
      const userRole = localStorage.getItem('userRole');
      
      console.log('🔍 Debug - Authentication check:');
      console.log('🔍 Debug - Token exists:', !!token);
      console.log('🔍 Debug - Token preview:', token ? token.substring(0, 50) + '...' : 'No token');
      console.log('🔍 Debug - User role:', userRole);
      
      if (!token) {
        alert('You are not logged in. Please login again.');
        navigate('/login');
        return;
      }

      setEditMode(false);
      const updatedData = tempAvatar
        ? { ...userData, avatar: tempAvatar }
        : userData;

      console.log('🔍 Debug - Saving user data:', updatedData);

      // Send data to backend database
      const profileData = {
        firstName: updatedData.firstName,
        lastName: updatedData.lastName,
        email: updatedData.email,
        phone: updatedData.phone,
        userName: updatedData.userName,
        address: updatedData.address,
        ...(userData.role === "student" && {
          grade: updatedData.grade,
          course: updatedData.course,
          parentEmail: updatedData.parentEmail,
          parentName: updatedData.parentName,
          parentPhone: updatedData.parentPhone
        })
      };

      console.log('🔍 Debug - Profile data to send:', profileData);
      console.log('🔍 Debug - API URL:', API_CONFIG.DJANGO.AUTH.PROFILE_UPDATE);

      // Call backend API to update profile
      const response = await djangoAPI.put(API_CONFIG.DJANGO.AUTH.PROFILE_UPDATE, profileData);
      
      console.log('🔍 Debug - Backend response:', response);

      // Update local state
      setUserData(updatedData);

      // Update localStorage
      if (userData.role === "student") {
        localStorage.setItem("studentData", JSON.stringify(updatedData));
      } else {
        localStorage.setItem("parentData", JSON.stringify(updatedData));
      }

      // Show success message
      alert('Profile updated successfully!');

    } catch (error) {
      console.error('❌ Error updating profile:', error);
      console.error('❌ Error details:', error.message);
      
      // Check if it's an authentication error
      if (error.message.includes('401')) {
        alert('Your session has expired. Please login again.');
        localStorage.removeItem('userToken');
        localStorage.removeItem('userRole');
        navigate('/login');
      } else {
        alert('Failed to update profile. Please try again.');
        // Revert edit mode on error
        setEditMode(true);
      }
    }
  };

  // Avatar change
  const handleAvatarChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setTempAvatar(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  if (!userData) {
    return (
      <div className="user-details-container">
        <div className="loading">Loading user data...</div>
      </div>
    );
  }

  return (
    <div className="user-details-container">
      <motion.div
        className="user-details-card"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="user-details-header">
          <h1>User Details</h1>
          <div className="header-buttons">
            <button className="back-button" onClick={() => navigate(-1)}>
              &larr; Back
            </button>
            <button className="logout-button-page" onClick={handleLogout}>
              Logout
            </button>
          </div>
        </div>

        <div className="user-details-content">
          <div className="avatar-section">
            <div className="user-avatar">
              {userData.avatar || tempAvatar ? (
                <img
                  src={tempAvatar || userData.avatar}
                  alt="User Avatar"
                  className="avatar-img"
                />
              ) : (
                <span>{userData.firstName?.charAt(0) || "U"}</span>
              )}
              {editMode && (
                <label className="avatar-upload">
                  <FaCamera />
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleAvatarChange}
                    style={{ display: "none" }}
                  />
                </label>
              )}
            </div>
            {editMode ? (
              <div className="name-inputs">
                <input
                  type="text"
                  name="firstName"
                  value={userData.firstName || ""}
                  onChange={handleInputChange}
                  placeholder="First Name"
                />
                <input
                  type="text"
                  name="lastName"
                  value={userData.lastName || ""}
                  onChange={handleInputChange}
                  placeholder="Last Name"
                />
              </div>
            ) : (
              <h2>
                {userData.firstName} {userData.lastName}
              </h2>
            )}
            <p className="user-role">
              {userData.role === "student" ? "Student" : "Parent"}
            </p>
          </div>

          <div className="details-section">
            <h3>Personal Information</h3>
            {[
              { label: "Email", name: "email" },
              { label: "Phone", name: "phone" },
              { label: "User Name", name: "userName" },
              ...(userData.role === "student"
                ? [
                    { label: "Grade", name: "grade" },
                 
                    { label: "Course", name: "course" },
                  ]
                : []),
              { label: "Address", name: "address" },
            ].map((field) => (
              <div className="detail-row" key={field.name}>
                <span className="detail-label">{field.label}:</span>
                {editMode ? (
                  <input
                    type="text"
                    name={field.name}
                    value={userData[field.name] || ""}
                    onChange={handleInputChange}
                    placeholder={field.label}
                  />
                ) : (
                  <span className="detail-value">
                    {userData[field.name] || "Not provided"}
                  </span>
                )}
              </div>
            ))}

            {userData.role === "student" && (
              <section className="parent-info-section">
                <h3>Parent/Guardian Information</h3>
                {[
                  { label: "Parent Name", key: "parentName" },
                  { label: "Parent Email", key: "parentEmail" },
                  { label: "Parent Phone", key: "parentPhone" },
                ].map(({ label, key }) => (
                  <div className="detail-row" key={key}>
                    <span className="detail-label">{label}:</span>
                    {editMode ? (
                      <input
                        type="text"
                        name={key}
                        value={userData[key] || ""}
                        onChange={handleInputChange}
                        placeholder={`Enter ${label}`}
                      />
                    ) : (
                      <span className="detail-value">
                        {userData[key] || "Not provided"}
                      </span>
                    )}
                  </div>
                ))}
              </section>
            )}

            <div className="edit-save-buttons">
              {editMode ? (
                <button className="save-button" onClick={handleSave}>
                  <FaSave /> Save
                </button>
              ) : (
                <button
                  className="edit-button"
                  onClick={() => setEditMode(true)}
                >
                  <FaEdit /> Edit
                </button>
              )}
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default UserDetailsPage;









