import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import { configureStore } from '@reduxjs/toolkit';
import globalReducer from 'state';
import { Provider } from 'react-redux';
import { setupListeners } from '@reduxjs/toolkit/query';
import {api} from 'state/api';

const store = configureStore({
  reducer:{
    global:globalReducer,
    [api.reducerPath]: api.reducer,
  },
  middleware:(getDefaultMiddleware)=> getDefaultMiddleware().concat(api.middleware),
  devTools: true,
});

setupListeners(store.dispatch);


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Provider store={store}>
      <App />
    </Provider>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
// reportWebVitals();
