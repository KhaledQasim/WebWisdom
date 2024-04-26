/* eslint-disable react/prop-types */
/* eslint-disable no-unused-vars */
import { useSignals, useSignalEffect } from "@preact/signals-react/runtime";
import { signal } from "@preact/signals-react";
import Loading from "./Loading";

const statPTT = signal();
const statZAP = signal();

const ResultSummary = ({ content, data }) => {
  useSignals();

  useSignalEffect(() => {
    const indexZAP = data.value.findIndex((item) => item.test === "ZAP");
    const indexPTT = data.value.findIndex((item) => item.test === "PTT");
   

    const isThereZAP = data.value[indexZAP]?.score === undefined;
    if (!isThereZAP) {
      statZAP.value = JSON.stringify(data.value[indexZAP]?.score?.security_score);
    } else {
      statZAP.value = false;
    }

    const isTherePTT = data.value[indexPTT]?.score === undefined;
    if (!isTherePTT) {
      statPTT.value = JSON.stringify(data.value[indexPTT]?.score?.security_score);
    } else {
      statPTT.value = false;
    }
  });

  return (
    <div className=" mx-auto mt-10 p-6 border border-base-300 rounded-md shadow-md bg-base-200 container mb-20">
      <h1 className="text-center  text-4xl font-bold mb-4">
        Penetration Test Score
      </h1>
      {statPTT.value ? (
        <>
          <div className="flex justify-center mb-4">
            <div>
              <div className="stats shadow">
                <div className="stat">
                  <div className="stat-value text-primary">
                    {statPTT.value}/10 - Base Test
                  </div>
                </div>
              </div>
            </div>
          </div>
        </>
      ) : (
        <>
          <div className="flex justify-center">
            <div className="text-primary text-3xl">
              No score was available for Base PTT test in the returned data!
            </div>
          </div>
        </>
      )}

      {statZAP.value ? (
        <>
          <div className="flex justify-center">
            <div>
              <div className="stats shadow">
                <div className="stat">
                  <div className="stat-value text-primary">
                    {statZAP.value}/10 - ZAP test
                  </div>
                </div>
              </div>
            </div>
          </div>
        </>
      ) : (
        <>
          <div className="flex justify-center">
            <div className="text-primary text-3xl">
              No score was available for ZAP penetration test in the returned data!
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default ResultSummary;
