import React from 'react';
import { useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';

const Header = () => {
  const navigate = useNavigate();
  const userLogin = useSelector((state) => state.user.login);

  const handleLogout = (event) => {
    event.preventDefault();

    window.localStorage.removeItem('access_token');
    navigate('/login');
  };

  return (
    <div className="header">
      <h2 onClick={() => navigate('/')}>Tixly</h2>
      <div className="header-account">
        <p>{userLogin}</p>
        <button onClick={handleLogout}>Выйти</button>
      </div>
    </div>
  );
};

export default Header;
