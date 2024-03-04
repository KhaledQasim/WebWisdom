import { signal } from "@preact/signals-react";
import { axiosRegister } from "../api/axios";
import { useNavigate } from "react-router-dom";
import { getUser } from "../lib/CheckUserAccount";
import { useSignals } from "@preact/signals-react/runtime";

const disabled = signal(false);
const username = signal("");
const password = signal("");
const confirmPassword = signal("");
const inputError = signal("");


export default function Register() {
  useSignals();
  const navigate = useNavigate();


  function RegisterUser() {
    disabled.value = true;
    axiosRegister
      .post("", {
        username: username.value,
        password: password.value,
      })
      .then((res) => {
        if (res.status === 200) {
          disabled.value = false;
          getUser();
          inputError.value = ""
          navigate("/");
        }
      })
      .catch((error) => {
        inputError.value = ""
        console.error(error);
        setTimeout(() => {
          disabled.value = false;
          inputError.value = "input-error"
        }, 2000);
      });
  }

  function HandleSubmit(e) {
    e.preventDefault();
    RegisterUser();
  }

  return (
    <form className="max-w-sm mx-auto mt-10" onSubmit={HandleSubmit}>
      <div className="mb-5">
        <label
          htmlFor="email"
          className="block mb-2 text-sm font-medium text-white"
        >
          Your Email
        </label>
        <input
          type="email"
          id="email"
          className={"rounded-lg block w-full p-2.5 input input-bordered input-primary  "+ inputError}
          required
          //   value={username.value}
          onChange={(e) => (username.value = e.currentTarget.value)}
          disabled={disabled.value}
        />
      </div>
      <div className="mb-5">
        <label
          htmlFor="password"
          className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
        >
          Your Password
        </label>
        <input
          type="password"
          id="password"
          className={"rounded-lg block w-full p-2.5 input input-bordered input-primary  "+ inputError}
          required
          //   value={password.value}
          onChange={(e) => (password.value = e.currentTarget.value)}
          disabled={disabled.value}
        />
      </div>
      <div className="mb-5">
        <label
          htmlFor="password"
          className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
        >
          Confirm Password
        </label>
        <input
          type="password"
          id="confirmPassword"
          className={"rounded-lg block w-full p-2.5 input input-bordered input-primary  "+ inputError}
          required
          //   value={password.value}
          onChange={(e) => (confirmPassword.value = e.currentTarget.value)}
          disabled={disabled.value}
        />
      </div>

      <div className="flex items-start mb-5">
        <div className="flex items-center h-5">
          <input
            id="remember"
            type="checkbox"
            value=""
            disabled={disabled.value}
            className="w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-blue-300 dark:bg-gray-700 dark:border-gray-600 dark:focus:ring-blue-600 dark:ring-offset-gray-800 dark:focus:ring-offset-gray-800"
          />
        </div>
        <label
          htmlFor="remember"
          className="ms-2 text-sm font-medium text-gray-900 dark:text-gray-300"
        >
          Remember me
        </label>
      </div>
      <button
        type="submit"
        disabled={disabled.value}
        className="btn text-white hover:bg-primary/50 hover:text-white bg-primary focus:ring-4 focus:outline-none rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center"
      >
        Submit
      </button>
    </form>
  );
}
