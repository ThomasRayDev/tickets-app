import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  firstname: '',
  secondname: '',
  login: '',
};

export const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    setUserData: (state, action) => {
      state.firstname = action.payload.firstname;
      state.secondname = action.payload.secondname;
      state.login = action.payload.login;
    },
  },
});

export const { setUserData } = userSlice.actions;

export default userSlice.reducer;
