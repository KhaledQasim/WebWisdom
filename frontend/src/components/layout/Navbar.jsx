// import Avatar from "../../assets/avatar.png";

function Navbar() {
  return (
    <div className="navbar bg-base-200 border-b border-b-neutral-content/5 sticky top-0 transition-all duration-300 z-10">
      <div className="flex-1">
        <a className="btn btn-ghost normal-case text-xl text-primary font-bold">
          WebWisdom
        </a>
      </div>
      <div className="flex-none ">
        <button className="btn btn-ghost normal-case font-bold text-base">Login/Register</button>
      </div>
    </div>
  );
}

export default Navbar;
