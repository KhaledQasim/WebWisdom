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
    if (data.value.data[2]?.files !== null && !isEmptyObject(data.value.data[2]?.files)) {
      files.value = data.value.data[2].files;
    } else {
      files.value = false;
    }

    loading.value = false;
  });
  function isEmptyObject(obj) {
    return Object.keys(obj).length === 0 && obj.constructor === Object;
  }

  return loading.value ? (
    <Loading />
  ) : files.value ? (
    <div className="bg-base-200 container grid mx-auto mt-10">
      <div className=" text-4xl text-center bg-primary/95 rounded-lg h-16">
        <div className="object-center mt-2">{MainTitle}</div>
      </div>
      <div className="my-5 px-4 text-base ">{MainContent}</div>
      {files.value.map((files,index) => (
        <div key={index}>
          <div className="text-accent px-4 text-xl grid gap-1">
            {files.File+" Risk Level: "+files.RiskLevel}
            <div className="border-b-2 border-base-content" />

            <StateOfBox
              content={"Description of Issue: "+files.Description}
              good={"neutral"}
              subHeading={""}
            />
            <StateOfBox
              content={"Recommendation to solve the issue: "+files.Recommendation}
              good={"neutral"}
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

