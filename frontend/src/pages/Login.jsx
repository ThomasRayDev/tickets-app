import React from 'react';
import axios from '../utils/axios';
import { useNavigate } from 'react-router-dom';

import { Link } from 'react-router-dom';

const Login = () => {
  const navigate = useNavigate();

  const [login, setLogin] = React.useState('');
  const [password, setPassword] = React.useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (login == '' || password == '') {
      alert('Все поля должны быть заполены!');
      return;
    }

    try {
      const res = await axios.post('/login', {
        login,
        password,
      });
      window.localStorage.setItem('access_token', res.data.auth.access_token);
      navigate('/');
    } catch (error) {
      console.log(error);
      alert('Произошла ошибка');
    }
  };

  return (
    <div className="page-center">
      <div className="login">
        <h3>Вход в систему</h3>
        <p>Введите ваш логин и пароль для входа в систему</p>

        <form>
          <label htmlFor="login">Логин</label>
          <input type="text" id="login" value={login} onChange={(e) => setLogin(e.target.value)} />
          <label htmlFor="password">Пароль</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button onClick={handleSubmit}>Войти</button>
        </form>

        <p>
          Нет аккаунта? <Link to="/register">Зарегистрироваться</Link>
        </p>
      </div>
    </div>
  );
};

export default Login;
