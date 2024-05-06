import { effect, signal } from "@preact/signals-react";

import axios from "../api/axios";

const user = signal("");

export const getUser = async () => {
  try {
    const response = await axios.get("/auth/users/me-cookie");
    if (response.status == 200) {
      user.value = response.data;
    } else {
      user.value = "";
    }
  } catch (error) {
    user.value = "";
    console.error("error in CheckUserAccount get auth/users/me-cookie", error);
  }
};

effect(() => {
  getUser();
});

export const userSignal = user;
