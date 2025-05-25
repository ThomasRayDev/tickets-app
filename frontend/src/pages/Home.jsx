import React from 'react';
import axios from '../utils/axios';

import { useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';

import { setUserData } from '../redux/slices/userSlice';

import Header from '../components/Header';
import Ticket from '../components/Ticket';

const Home = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const [tickets, setTickets] = React.useState([]);

  const ticketList = tickets.map((obj) => (
    <Ticket
      title={obj.title}
      description={obj.description}
      author={obj.author}
      created_on={obj.created_on}
    />
  ));

  const getCurrentUser = async () => {
    try {
      const res = await axios.get('/current-user');
      dispatch(
        setUserData({
          firstname: res.data.firstname,
          secondname: res.data.secondname,
          login: res.data.login,
        }),
      );
    } catch (error) {
      navigate('/login');
    }
  };

  const fetchTickets = async () => {
    try {
      const res = await axios.get('/tickets');
      setTickets(res.data);
    } catch (error) {
      console.log(error);
      alert('Произошла ошибка');
    }
  };

  React.useEffect(() => {
    if (!window.localStorage.getItem('access_token')) {
      return navigate('/login');
    }

    getCurrentUser();
    fetchTickets();
  }, [navigate]);

  return (
    <>
      <Header />
      <div className="wrapper">
        <div className="navigation">
          <p>Навигация</p>
          <ul>
            <li>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                height="24px"
                viewBox="0 -960 960 960"
                width="24px"
                fill="#000000">
                <path d="M200-120q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h168q13-36 43.5-58t68.5-22q38 0 68.5 22t43.5 58h168q33 0 56.5 23.5T840-760v560q0 33-23.5 56.5T760-120H200Zm0-80h560v-560H200v560Zm80-80h280v-80H280v80Zm0-160h400v-80H280v80Zm0-160h400v-80H280v80Zm200-190q13 0 21.5-8.5T510-820q0-13-8.5-21.5T480-850q-13 0-21.5 8.5T450-820q0 13 8.5 21.5T480-790ZM200-200v-560 560Z" />
              </svg>
              <p>Все заявки</p>
            </li>
            <li>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                height="24px"
                viewBox="0 -960 960 960"
                width="24px"
                fill="#000000">
                <path d="M200-120q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h168q13-36 43.5-58t68.5-22q38 0 68.5 22t43.5 58h168q33 0 56.5 23.5T840-760v268q-19-9-39-15.5t-41-9.5v-243H200v560h242q3 22 9.5 42t15.5 38H200Zm0-120v40-560 243-3 280Zm80-40h163q3-21 9.5-41t14.5-39H280v80Zm0-160h244q32-30 71.5-50t84.5-27v-3H280v80Zm0-160h400v-80H280v80Zm200-190q13 0 21.5-8.5T510-820q0-13-8.5-21.5T480-850q-13 0-21.5 8.5T450-820q0 13 8.5 21.5T480-790ZM720-40q-83 0-141.5-58.5T520-240q0-83 58.5-141.5T720-440q83 0 141.5 58.5T920-240q0 83-58.5 141.5T720-40Zm-20-80h40v-100h100v-40H740v-100h-40v100H600v40h100v100Z" />
              </svg>
              <p>Создать заявку</p>
            </li>
            <li>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                height="24px"
                viewBox="0 -960 960 960"
                width="24px"
                fill="#000000">
                <path d="m370-80-16-128q-13-5-24.5-12T307-235l-119 50L78-375l103-78q-1-7-1-13.5v-27q0-6.5 1-13.5L78-585l110-190 119 50q11-8 23-15t24-12l16-128h220l16 128q13 5 24.5 12t22.5 15l119-50 110 190-103 78q1 7 1 13.5v27q0 6.5-2 13.5l103 78-110 190-118-50q-11 8-23 15t-24 12L590-80H370Zm70-80h79l14-106q31-8 57.5-23.5T639-327l99 41 39-68-86-65q5-14 7-29.5t2-31.5q0-16-2-31.5t-7-29.5l86-65-39-68-99 42q-22-23-48.5-38.5T533-694l-13-106h-79l-14 106q-31 8-57.5 23.5T321-633l-99-41-39 68 86 64q-5 15-7 30t-2 32q0 16 2 31t7 30l-86 65 39 68 99-42q22 23 48.5 38.5T427-266l13 106Zm42-180q58 0 99-41t41-99q0-58-41-99t-99-41q-59 0-99.5 41T342-480q0 58 40.5 99t99.5 41Zm-2-140Z" />
              </svg>
              <p>Настройки</p>
            </li>
          </ul>
        </div>
        <div className="container">
          <h2>Все заявки</h2>
          <p>Здесь вы можете просматривать и редактировать все назначенные на вас заявки</p>
          <div className="tickets">{ticketList}</div>
        </div>
      </div>
    </>
  );
};

export default Home;
