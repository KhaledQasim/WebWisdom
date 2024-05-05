/* eslint-disable react/prop-types */
import { useNavigate } from "react-router-dom";
import { axiosLoginForm } from "../api/axios";
import { signal } from "@preact/signals-react";
import { useSignals } from "@preact/signals-react/runtime";
import { getUser } from "../lib/CheckUserAccount";

const username = signal("");
const password = signal("");
const disabled = signal(false);
const inputError = signal("");
const errorResponse = signal({
  data: "data",
  isTrue: false,
});

export default function Login() {
  useSignals();

  const navigate = useNavigate();

  function LoginUser() {
    disabled.value = true;

    axiosLoginForm
      .post("", {
        username: username.value,
        password: password.value,
      })
      .then(function response(response) {
        if (response.status === 200) {
          getUser();
          disabled.value = false;
          inputError.value = "";
          navigate("/");
        } else {
          disabled.value = false;
        }
      })
      .catch(function error(error) {
        console.error(error);
        inputError.value = "";
        setTimeout(() => {
          disabled.value = false;
          inputError.value = "input-error";
          errorResponse.value.isTrue = true;
          errorResponse.value.data = error.response.data.detail
        }, 2000);


      });
  }

  function HandleSubmit(e) {
    e.preventDefault();
    LoginUser();
  }
  return (
    <form className="max-w-sm mx-auto mt-10" onSubmit={HandleSubmit}>
      <div className="mb-5">
        <label
          htmlFor="email"
          className="block mb-2 text-sm font-medium text-base-content"
        >
          Your Email
        </label>
        <input
          type="email"
          id="email"
          className={
            "rounded-lg block w-full p-2.5 input input-bordered  input-primary " +
            inputError
          }
          required
          //   value={username.value}
          onChange={(e) => (username.value = e.currentTarget.value)}
          disabled={disabled.value}
        />
      </div>
      <div className="mb-5">
        <label
          htmlFor="password"
          className="block mb-2 text-sm font-medium text-base-content"
        >
          Your Password
        </label>
        <input
          type="password"
          id="password"
          className={
            "rounded-lg block w-full p-2.5 input input-bordered input-primary  " +
            inputError
          }
          required
          //   value={password.value}
          onChange={(e) => (password.value = e.currentTarget.value)}
          disabled={disabled.value}
        />
        {errorResponse.value.isTrue ? (
          <>
            <span className="label-text-alt text-error">{errorResponse.value.data}</span>
          </>
        ) : (
          <></>
        )}
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
