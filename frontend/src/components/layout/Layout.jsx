import Navbar from "./Navbar";
import Footer from "./Footer";
import { Outlet } from "react-router-dom";

function Layout() {
  return (
    // <div >
    //   <Navbar />
    //   {/* <main className="md:min-h-[89vh] min-h-[79vh]"> */}
    //   <main>
    //     <Outlet />
    //   </main>

    //   <Footer />
    // </div>
    <div className="flex flex-col min-h-screen">
      <Navbar />
      <div className="flex-grow">
        <Outlet />
      </div>
      <div>
        <Footer />
      </div>
    </div>
  );
}

export default Layout;
