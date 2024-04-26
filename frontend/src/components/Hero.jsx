import { signal } from "@preact/signals-react";
import { useSignals, useSignalEffect } from "@preact/signals-react/runtime";
import { useNavigate } from "react-router-dom";
import { axiosStartScan } from "../api/axios";
import Loading from "./Loading";

const url = signal("");
const disabled = signal(false);
const isLoading = signal(false);
const errorMessage = signal("");
const id = signal();

export default function Hero() {
  useSignals();

  //the user can not close or refresh the browser when the api call is active
  useSignalEffect(() => {
    const handleBeforeUnload = (event) => {
      event.preventDefault();
      event.returnValue = "";
    };

    if (disabled.value) {
      window.addEventListener("beforeunload", handleBeforeUnload);
    } else {
      window.removeEventListener("beforeunload", handleBeforeUnload);
    }

    return () => {
      window.removeEventListener("beforeunload", handleBeforeUnload);
    };
  });
  const navigate = useNavigate();

  function ScanDomain() {
    disabled.value = true;
    isLoading.value = true;
    errorMessage.value = "";
    axiosStartScan
      .post("", {
        url: "https://" + url.value,
      })
      .then(function response(response) {
        disabled.value = false;
        isLoading.value = false;
        const index = response.data.data.findIndex(item =>  Object.prototype.hasOwnProperty.call(item,'id'));
        id.value = response.data.data[index].id
        // print("id value of test",id.value," index of id",index," data associated with getting id: ",response.data.data)
        navigate(`/result/${id}`);
      
      })
      .catch(function error(error) {
        disabled.value = false;
        isLoading.value = false;
        console.log("error in hero test scan: ",error)
        errorMessage.value = String(error.response.data.detail)
        console.error("error in Hero page",error);
      });
  }

  function HandleSubmit(e) {
    e.preventDefault();
    ScanDomain();
  }

  return (
    <>
      {isLoading.value ? (
        <Loading/>
      ) : (
        <section className="w-full py-6 sm:py-12 md:py-24 lg:py-32 xl:py-48 flex justify-center">
          <div className="container px-4 md:px-6 flex flex-col items-center justify-center space-y-4 text-center">
            <div className="space-y-2">
              <h1 className="text-3xl font-bold tracking-tighter sm:text-5xl xl:text-6xl/none text-base-content">
                Check your website&apos;s security with a single click
              </h1>
              <p className="mx-auto max-w-[600px] text-gray-500 md:text-xl dark:text-gray-400">
                Enter your website URL to scan for security vulnerabilities.
                Understand which components of your site might be exploited by
                threat actors.
              </p>
            </div>
            <div className="mx-auto w-full max-w-sm space-y-2">
              <form
                className="flex space-x-2 items-center"
                onSubmit={HandleSubmit}
              >
                <div className="badge badge-accent">https://</div>
                <input
                  className="max-w-lg flex-1 input input-bordered input-primary w-full "
                  placeholder="Enter your website"
                  type="text"
                  onChange={(e) => (url.value = e.currentTarget.value)}
                  disabled={disabled.value}
                  required
                  value={url.value}
                />
                <button
                  type="submit"
                  className="btn btn-primary"
                  disabled={disabled.value}
                >
                  Scan Now
                </button>
              </form>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                Please only enter the hostname e.g: google.com youtube.com
              </p>
              {errorMessage.value ? (
                <>
                  <div role="alert" className="alert alert-error">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      className="stroke-current shrink-0 h-6 w-6"
                      fill="none"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth="2"
                        d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
                      />
                    </svg>
                    <span>Error! {errorMessage.value} </span>
                  </div>
                </>
              ) : (
                <></>
              )}
            </div>
          </div>
        </section>
      )}
    </>
  );
}
