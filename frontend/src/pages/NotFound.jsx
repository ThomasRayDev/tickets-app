import React from 'react';

import Header from '../components/Header';

const NotFound = () => {
  return (
    <>
      <Header />
      <div className="page-center">
        <div className="not-found">
          <img src="img/not-found.png" alt="Not found" width="256" />
          <p>Похоже, что такой страницы не существует.</p>
          <p>Если адрес страницы введен верно, возможно, возникла какая-то ошибка.</p>
        </div>
      </div>
    </>
  );
};

export default NotFound;
