/* eslint-disable react/prop-types */
/* eslint-disable no-unused-vars */
import { useSignals, useSignalEffect } from "@preact/signals-react/runtime";
import { signal } from "@preact/signals-react";
import Loading from "./Loading";

const stat = signal();

const ResultSummary = ({ content, data }) => {
  useSignals();

  useSignalEffect(() => {
    const siThereStat = data.value.data[6]?.security_score === undefined;
    if (!siThereStat) {
      stat.value = data.value.data[6].security_score;
    } else {
      stat.value = false;
    }
  });

  return (
    <div className=" mx-auto mt-10 p-6 border border-base-300 rounded-md shadow-md bg-base-200 container mb-20">
      <h1 className="text-center  text-4xl font-bold mb-4">
        Penetration Test Score
      </h1>
      {stat.value ? (
        <>
          <div className="flex justify-center">
            <div>
              <div className="stats shadow">
                <div className="stat">
                  <div className="stat-value text-primary">{stat.value}/10</div>
                </div>
              </div>
            </div>
          </div>
        </>
      ) : (
        <>
          <div className="flex justify-center">
            <div className="text-primary text-3xl">No score was available in the returned data!</div>
          </div>
        </>
      )}
    </div>
  );
};

export default ResultSummary;
