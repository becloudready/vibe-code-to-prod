import React, { useState } from 'react';
import dataService from '../services/dataService';
import { useLocation, useNavigate } from 'react-router-dom';
import './Profile.css';

const Profile = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const username = location.state?.username || 'Unknown';
  const isAdmin = location.state?.isAdmin || false;
  const [showUsers, setShowUsers] = useState(false);
  const [usersList, setUsersList] = useState([]);
  const [loadingUsers, setLoadingUsers] = useState(false);
  const [usersError, setUsersError] = useState('');

  const handleShowUsers = async () => {
    if (!showUsers) {
      setLoadingUsers(true);
      setUsersError('');
      try {
        const users = await dataService.getAllUsers();
        setUsersList(users);
      } catch (err) {
        setUsersError('Failed to fetch users');
      }
      setLoadingUsers(false);
    }
    setShowUsers((v) => !v);
  };

  // Placeholder data
  const profileData = {
    username,
    fullName: 'John Doe',
    email: 'johndoe@example.com',
    accountNumber: '1234567890',
    balance: '$10,000',
    address: '123 Main St, City, Country',
  };

  return (
    <div className="profile-container">
      <h2>{isAdmin ? 'Admin Profile' : 'Customer Profile'}</h2>
      <ul>
        <li><strong>Username:</strong> {profileData.username}</li>
        <li><strong>Full Name:</strong> {profileData.fullName}</li>
        <li><strong>Email:</strong> {profileData.email}</li>
        <li><strong>Account Number:</strong> {profileData.accountNumber}</li>
        <li><strong>Balance:</strong> {profileData.balance}</li>
        <li><strong>Address:</strong> {profileData.address}</li>
      </ul>
      {isAdmin && (
        <>
          <button onClick={handleShowUsers}>
            {showUsers ? 'Hide Registered Users' : 'List of Registered Users'}
          </button>
          {showUsers && (
            <div style={{ marginTop: '1.5rem' }}>
              <h3>Registered Users</h3>
              {loadingUsers ? (
                <p>Loading...</p>
              ) : usersError ? (
                <p style={{ color: 'red' }}>{usersError}</p>
              ) : (
                <ul>
                  {Array.isArray(usersList) && usersList.length === 0 ? (
                    <li>No users found.</li>
                  ) : (
                    usersList.map((u, idx) => <li key={u.username || u || idx}>{u.username || u}</li>)
                  )}
                </ul>
              )}
            </div>
          )}
        </>
      )}
      <button onClick={() => navigate('/')}>Logout</button>
    </div>
  );
};

export default Profile;
