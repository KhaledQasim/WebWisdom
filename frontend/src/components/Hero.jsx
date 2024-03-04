export default function Hero() {
  return (
    <>
      {/* <div className={className + " hero min-h-96"}>
        <div className="hero-content text-center">
          <div className="">
            <h1 className="text-6xl font-bold ">
              Secure your website with a single click
            </h1>
            <div className="">
              <p className="py-6  max-w-md">
                Provident cupiditate voluptatem et in. Quaerat fugiat ut
                assumenda excepturi exercitationem quasi. In deleniti eaque aut
                repudiandae et a id nisi.
              </p>
            </div>

            <button className="btn btn-primary">Get Started</button>
          </div>
        </div>
      </div> */}
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
            <form className="flex space-x-2">
              <input
                className="max-w-lg flex-1 input input-bordered input-primary w-full "
                placeholder="Enter your website URL"
                type="url"
              />
              <button type="submit" className="btn btn-primary">Scan Now</button>
            </form>
            <p className="text-sm text-gray-500 dark:text-gray-400">Example domains: example.com, test.org, demo.net</p>

          </div>
        </div>
      </section>
    </>
  );
}
