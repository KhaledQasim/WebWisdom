/* eslint-disable react/prop-types */
/* eslint-disable no-unused-vars */
import StateOfBox from "./StateOfBox";
import { useSignals, useSignalEffect } from "@preact/signals-react/runtime";
import { signal } from "@preact/signals-react";
import Loading from "./Loading";

const files = signal();
const loading = signal(true);

const ResultBoxFiles = ({
  MainTitle,
  MainContent,
  title,
  content,
  good,
  data,
}) => {
  useSignals();

  useSignalEffect(() => {
    const indexPTT = data.value.findIndex((item) => item.test === "PTT");
   
  
    if (
      data.value[indexPTT]?.report[2].files !== null &&
      !isEmptyObject(data.value[indexPTT]?.report[2].files)
    ) {
      files.value = data.value[indexPTT]?.report[2].files[0].data;
    } else {
      files.value = false;
    }

    loading.value = false;
  });
  function isEmptyObject(obj) {
    return Object.keys(obj).length === 0 && obj.constructor === Object;
  }

  function renderContentStateBasedOnFilesRiskLevel(Files) {
    let content;

    switch (
      true // The switch is always true, so we can use it to check multiple conditions
    ) {
      case Files.includes("1"):
        content = "neutral";
        break;
      case Files.includes("2"):
        content = "warning";
        break;
      case Files.includes("3"):
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
  ) : files.value ? (
    <div className="bg-base-200 container grid mx-auto mt-10">
      <div className=" text-4xl text-center bg-primary/95 rounded-lg h-16">
        <div className="object-center mt-2">{MainTitle}</div>
      </div>
      <div className="my-5 px-4 text-base ">{MainContent}</div>
      {files.value.map((files, index) => (
        <div key={index}>
          <div className="text-accent px-4 text-xl grid gap-1">
            {files.File + " Risk Level: " + files.RiskLevel}
            <div className="border-b-2 border-base-content" />

            <StateOfBox
              content={
                "Description of Issue: " +
                files.Description +
                "\n\n Recommendation to solve the issue: " +
                files.Recommendation
              }
              good={renderContentStateBasedOnFilesRiskLevel(files.RiskLevel)}
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

export default ResultBoxFiles;
