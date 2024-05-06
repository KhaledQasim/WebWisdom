import axios from "../api/axios";
import { userSignal } from "./CheckUserAccount";



export function Logout() {
  axios.get("/auth/logout").then(()=>{
  }).catch((error)=>{
    console.error(error)
  });
  userSignal.value = "";
}
