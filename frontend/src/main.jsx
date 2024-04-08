import "../dist/output.css"
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";
import { Route, Routes, BrowserRouter } from "react-router-dom";
import Layout from "./components/Layout.jsx";
import Login from "./pages/Login.jsx";
import Register from "./pages/Register.jsx";
import ErrorPage from "./pages/ErrorPage.jsx";
import { userSignal } from "./lib/CheckUserAccount.jsx";



ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout user={userSignal} />}>
          <Route index element={<App />} />
          <Route path="/login" element={<Login user={userSignal}  />} />
          <Route path="/register" element={<Register user={userSignal}/>} />
          <Route path="*" element={<ErrorPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);
