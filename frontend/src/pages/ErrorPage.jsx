import { useNavigate } from "react-router-dom";



export default function ErrorPage(){
    const navigate = useNavigate();
    function handleClick(){
        navigate("/")
    }

    return(
        <div className="min-h-screen flex flex-grow items-center justify-center">
        <div className="rounded-lg bg-base-200  p-8 text-center shadow-xl">
          <h1 className="mb-4 text-4xl font-bold text-base-content">404</h1>
          <p className="text-neutral-content ">
            Oops! The page you are looking for could not be found.
          </p>
          <button
            onClick={handleClick}
      
            className="mt-4 inline-block rounded bg-primary  px-4 py-2 font-semibold text-base-content hover:bg-primary/50 "
          >
            {" "}
            Go back to Home{" "}
          </button>
        </div>
      </div>
    )
}