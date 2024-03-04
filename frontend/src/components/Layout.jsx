/* eslint-disable react/prop-types */
import Footer from "./Footer";
import Navbar from "./Navbar";
import { Outlet } from "react-router-dom";
import { useSignals } from "@preact/signals-react/runtime";

function Layout({ user }) {
  useSignals();
  return (
    <>
      <div className="flex flex-col min-h-[100vh] min-h-[100svh]">
        <Navbar user={user} />
        <div className="flex-grow">
          <Outlet />
        </div>
        <Footer />
      </div>
    </>
  );
}
export default Layout;
