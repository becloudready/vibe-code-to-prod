import React, { useState } from 'react';
import dataService from '../services/dataService';
import { useNavigate } from 'react-router-dom';
import './RegistrationLogin.css';

const RegistrationLogin = () => {
  const navigate = useNavigate();
  const [isLogin, setIsLogin] = useState(true);
  const [form, setForm] = useState({ username: '', password: '' });
  const [message, setMessage] = useState('');

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleRegister = (e) => {
    e.preventDefault();
    const users = JSON.parse(localStorage.getItem('users') || '{}');
    if (users[form.username]) {
      setMessage('User already exists!');
      return;
    }
    users[form.username] = form.password;
    localStorage.setItem('users', JSON.stringify(users));
    setMessage('Registration successful! Please login.');
    setIsLogin(true);
    setForm({ username: '', password: '' });
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setMessage('');
    const result = await dataService.login(form.username, form.password);
    if (result.success) {
      setMessage('Login successful!');
      setTimeout(() => {
        navigate('/profile', {
          state: {
            username: result.user.username,
            isAdmin: result.user.role === 'admin',
          },
        });
      }, 500);
    } else {
      setMessage(result.message || 'Invalid username or password!');
    }
  };

  return (
    <div className="auth-container">
      <h2>{isLogin ? 'Login' : 'Register'}</h2>
      <form onSubmit={isLogin ? handleLogin : handleRegister}>
        <input
          type="text"
          name="username"
          placeholder="Username"
          value={form.username}
          onChange={handleChange}
          required
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={form.password}
          onChange={handleChange}
          required
        />
        <button type="submit">{isLogin ? 'Login' : 'Register'}</button>
      </form>
      <button onClick={() => { setIsLogin(!isLogin); setMessage(''); setForm({ username: '', password: '' }); }}>
        {isLogin ? 'Need an account? Register' : 'Already have an account? Login'}
      </button>
      {message && <p>{message}</p>}
    </div>
  );
};

export default RegistrationLogin;
