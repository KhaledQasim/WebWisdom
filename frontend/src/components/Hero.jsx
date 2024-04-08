import { signal } from "@preact/signals-react";
import { useSignals } from "@preact/signals-react/runtime";
import { useNavigate } from "react-router-dom";
import { axiosStartScan } from "../api/axios";

const url = signal("");
const disabled = signal(false);
const isLoading = signal(false)

export default function Hero() {
  useSignals();

  // const navigate = useNavigate();

  function ScanDomain() {
    disabled.value = true;
    isLoading.value = true;
    axiosStartScan
      .post("", {
        url: "https://" + url.value,
      })
      .then(function response(response) {
        if (response.status === 200) {
          console.log(response.data.data);
        }

        setTimeout(() => {
          disabled.value = false;
          isLoading.value = false;

        }, 2000);
      })
      .catch(function error(error) {
        console.error(error);
        setTimeout(() => {
          disabled.value = false;
          isLoading.value = false;

        }, 2000);
      });
  }

  function HandleSubmit(e) {
    e.preventDefault();
    ScanDomain();
  }

  return (
    <>
      {isLoading.value ? (
        <div className="w-full flex justify-center">
          <div className="loading loading-ring text-primary w-[40%]">
          </div>
        </div>
        
      ) : (
        <section className="w-full py-6 sm:py-12 md:py-24 lg:py-32 xl:py-48 flex justify-center">
          <div className="container px-4 md:px-6 flex flex-col items-center justify-center space-y-4 text-center">
            <div className="space-y-2">
              <h1 className="text-3xl font-bold tracking-tighter sm:text-5xl xl:text-6xl/none text-base-content">
                Secure your website with a single click
              </h1>
              <p className="mx-auto max-w-[600px] text-gray-500 md:text-xl dark:text-gray-400">
                Enter your website URL to scan for security vulnerabilities. Get
                real-time threat alerts and comprehensive reports.
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
                Example domains: example.com, test.org, demo.net
              </p>
            </div>
          </div>
        </section>
      )}
    </>
  );
}
