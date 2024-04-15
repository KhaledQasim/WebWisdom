/* eslint-disable react/prop-types */
/* eslint-disable no-unused-vars */

const ResultSummary = ({ content }) => {
  return (
    <div className="max-w-4xl mx-auto mt-10 p-6 border border-base-300 rounded-md shadow-md bg-base-200">
      <h1 className="text-center text-xl font-bold mb-4">
        Web Software Security Test Summary
      </h1>
      <p>{content}</p>
    </div>
  );
};

export default ResultSummary;
