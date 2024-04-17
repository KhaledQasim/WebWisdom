import { useSignals } from "@preact/signals-react/runtime";
import Logo from "../assets/oig-clean.png";
import { Link, useNavigate } from "react-router-dom";
import { Logout } from "../lib/Logout";

/* eslint-disable react/prop-types */
export default function Navbar({ user }) {
  useSignals();
  const navigate = useNavigate();
  return (
    <div className="navbar bg-base-100 drop-shadow-xl">
      <div className="flex-1 space-x-2">
        <Link to={"/"}>
          <img src={Logo} alt="Logo" className="w-16 rounded-xl" />
        </Link>
        <Link to={"/"}>
          <div className="text-lg text-neutral-content">WebWisdom</div>
        </Link>
      </div>
      <div className="flex-none space-x-2">
        {user.value ? (
          <>
            <div>
              Welcome {JSON.stringify(user.value.username).split('"').join("")}
            </div>
            <button
              className="btn btn-primary"
              onClick={() => {
               
                navigate("/results");
              }}
            >
              Past Results
            </button>
            <button
              className="btn btn-primary"
              onClick={() => {
                Logout();
                navigate("/");
              }}
            >
              Logout
            </button>
          </>
        ) : (
          <>
            <button
              className="btn btn-neutral"
              onClick={() => {
                navigate("/login");
              }}
            >
              Login
            </button>
            <button
              className="btn btn-neutral "
              onClick={() => {
                navigate("/register");
              }}
            >
              Register
            </button>
          </>
        )}
      </div>
    </div>
    //    <header className="px-4 lg:px-6 h-14 flex items-center">
    //    <Link className="flex items-center justify-center" href="#">
    //      <MountainIcon className="h-6 w-6" />
    //      <span className="sr-only">Acme Inc</span>
    //    </Link>
    //    <nav className="ml-auto flex gap-4 sm:gap-6">
    //      <Link className="text-sm font-medium hover:underline underline-offset-4" href="#">
    //        Features
    //      </Link>
    //      <Link className="text-sm font-medium hover:underline underline-offset-4" href="#">
    //        Pricing
    //      </Link>
    //      <Link className="text-sm font-medium hover:underline underline-offset-4" href="#">
    //        About
    //      </Link>
    //      <Link className="text-sm font-medium hover:underline underline-offset-4" href="#">
    //        Contact
    //      </Link>
    //    </nav>
    //  </header>
  );
}
