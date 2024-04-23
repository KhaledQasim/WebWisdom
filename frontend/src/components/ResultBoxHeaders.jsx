/* eslint-disable react/prop-types */
/* eslint-disable no-unused-vars */
import StateOfBox from "./StateOfBox";
import { useSignals, useSignalEffect } from "@preact/signals-react/runtime";
import { signal } from "@preact/signals-react";
import Loading from "./Loading";

const headers = signal();
const loading = signal(true);

const ResultBoxHeaders = ({
  MainTitle,
  MainContent,
  title,
  content,
  good,
  data,
}) => {
  useSignals();

  useSignalEffect(() => {
    if (
      data.value.data[1]?.headers !== null &&
      !isEmptyObject(data.value.data[1]?.headers)
    ) {
      headers.value = data.value.data[1].headers[0].data;
    } else {
      headers.value = false;
    }
    
    loading.value = false;
  });
  function isEmptyObject(obj) {
    return Object.keys(obj).length === 0 && obj.constructor === Object;
  }

  function renderContentStateBasedOnHeadersRiskLevel(headers) {
    let content;

    switch (
      true // The switch is always true, so we can use it to check multiple conditions
    ) {
      case headers.includes("1"):
        content = "neutral";
        break;
      case headers.includes("2"):
        content = "warning";
        break;
      case headers.includes("3"):
        content = "bad";
        break;
      default:
        content = "neutral";
        break;
    }

    return content;
  }

  return loading.value ? (
    <Loading />
  ) : headers.value ? (
    <div className="bg-base-200 container grid mx-auto mt-10">
      <div className=" text-4xl text-center bg-primary/95 rounded-lg h-16">
        <div className="object-center mt-2">{MainTitle}</div>
      </div>
      <div className="my-5 px-4 text-base ">{MainContent}</div>
      {headers.value.map((headers, index) => (
        <div key={index}>
          <div className="text-accent px-4 text-xl grid gap-1">
            {headers.Header + " -- Risk Level: " + headers.RiskLevel}
            <div className="border-b-2 border-base-content" />

            <StateOfBox
              content={
                "Description of Issue: " +
                headers.Description +
                "\n\n Recommendation on solving the issue: " +
                headers.Recommendation +
                "\n\n Evidence of issue: " +
                headers.Evidence.EvidenceDetail +
                " --- The URL associated with this header issue: --- " +
                headers.Evidence.URL
              }
              good={renderContentStateBasedOnHeadersRiskLevel(headers.RiskLevel)}
              subHeading={""}
            />
          </div>
        </div>
      ))}
    </div>
  ) : (
    <></>
  );
};

export default ResultBoxHeaders;
