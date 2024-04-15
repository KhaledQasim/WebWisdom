/* eslint-disable react/prop-types */
/* eslint-disable no-unused-vars */

const ResultBox = ({ MainTitle, MainContent, title, content, good }) => {
  return (
    <div className="bg-base-200 container grid mx-auto mt-5">
      <div className=" text-4xl text-center bg-primary rounded-lg h-16">
        <div className="object-center mt-2">
            {MainTitle}
        </div>
      </div>
      <div className="my-5 px-4 text-base ">{MainContent}</div>

      <div className="text-accent px-4 text-xl grid gap-1">
        {title}
        <div className="border-b-2 border-base-content" />

        {good ? (
          <div role="alert" className="alert alert-success">
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
                d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <span className="text-base">{content}</span>
          </div>
        ) : (
          <div role="alert" className="alert alert-warning">
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
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
              />
            </svg>
            <span className="text-base">{content}</span>
          </div>
        )}
      </div>
    </div>
  );
};

export default ResultBox;
