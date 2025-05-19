import React from 'react';
import axios from '../utils/axios';
import { useNavigate } from 'react-router-dom';

const Register = () => {
  const navigate = useNavigate();

  const [form, setForm] = React.useState({
    firstname: '',
    secondname: '',
    login: '',
    password: '',
    repeatPassword: '',
  });
  const [touched, setTouched] = React.useState({});

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleBlur = (event) => {
    const { name } = event.target;
    setTouched((prev) => ({ ...prev, [name]: true }));
  };

  const isInvalid = (name) => touched[name] && form[name].trim() === '';

  const handleSubmit = async (event) => {
    event.preventDefault();

    for (const [key] of Object.entries(form)) {
      setTouched((prev) => ({ ...prev, [key]: true }));
    }

    for (const [key] of Object.entries(form)) {
      if (form[key] === '') return alert('Все поля формы должны быть заполнены');
    }

    if (form.password !== form.repeatPassword) {
      alert('Пароли не совпадают');
      return;
    }

    try {
      const res = await axios.post('/register', {
        login: form.login,
        password: form.password,
        firstname: form.firstname,
        secondname: form.secondname,
      });
      if (res.data) {
        alert('Пользователь успешно зарегистрирован');
        navigate('/login');
      }
    } catch (error) {
      console.log(error);
      alert('Произошла ошибка');
    }
  };

  return (
    <div className="page-center">
      <div className="login">
        <h3>Создание аккаунта</h3>

        <form>
          <div className="register-name">
            <div className="form-col">
              <label htmlFor="firstname">Имя</label>
              <input
                type="text"
                id="firstname"
                name="firstname"
                value={form.firstname}
                onBlur={handleBlur}
                onChange={handleChange}
                className={isInvalid('firstname') ? 'input-error' : ''}
              />
            </div>
            <div className="form-col">
              <label htmlFor="secondname">Фамилия</label>
              <input
                type="text"
                id="secondname"
                name="secondname"
                value={form.secondname}
                onBlur={handleBlur}
                onChange={handleChange}
                className={isInvalid('secondname') ? 'input-error' : ''}
              />
            </div>
          </div>
          <label htmlFor="login">Логин</label>
          <input
            type="text"
            id="login"
            name="login"
            value={form.login}
            onBlur={handleBlur}
            onChange={handleChange}
            className={isInvalid('login') ? 'input-error' : ''}
          />
          <label htmlFor="password">Пароль</label>
          <input
            type="password"
            id="password"
            name="password"
            value={form.password}
            onBlur={handleBlur}
            onChange={handleChange}
            className={isInvalid('password') ? 'input-error' : ''}
          />
          <label htmlFor="repeat-password">Повторить пароль</label>
          <input
            type="password"
            id="repeat-password"
            name="repeatPassword"
            value={form.repeatPassword}
            onBlur={handleBlur}
            onChange={handleChange}
            className={isInvalid('repeatPassword') ? 'input-error' : ''}
          />
          <button onClick={handleSubmit}>Создать аккаунт</button>
        </form>

        <p>
          Нажимая на кнопку «Создать аккаунт», вы принимаете{' '}
          <a href="#">политику конфиденциальности</a>.
        </p>
      </div>
    </div>
  );
};

export default Register;
