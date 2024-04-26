/* eslint-disable react/prop-types */
/* eslint-disable no-unused-vars */
import StateOfBox from "./StateOfBox";
import { useSignals, useSignalEffect } from "@preact/signals-react/runtime";
import { signal } from "@preact/signals-react";
import Loading from "./Loading";
import HtmlContent from "./HtmlContent";

const technologies = signal(false);
const loading = signal(true);

const ResultZAP = ({ MainTitle, MainContent, title, content, good, data }) => {
  useSignals();

  useSignalEffect(() => {
    const indexZAP = data.value.findIndex((item) => item.test === "ZAP");

    if (
      data.value[indexZAP]?.report !== null &&
      !isEmptyObject(data.value[indexZAP]?.report)
    ) {
      technologies.value = data.value[indexZAP]?.report;
    } else {
      technologies.value = false;
    }
   
    loading.value = false;
  });
  function isEmptyObject(obj) {
    return Object.keys(obj).length === 0 && obj.constructor === Object;
  }

  return loading.value ? (
    <Loading />
  ) : technologies.value ? (
    <div className="bg-base-200 container grid mx-auto mt-10">
      <div className=" text-4xl text-center bg-primary/95 rounded-lg h-16">
        <div className="object-center mt-2">{MainTitle}</div>
      </div>
      <div className="my-5 px-4 text-base ">{MainContent}</div>

      <div className="px-4 overflow-x-auto container mx-auto bg-accent-content ">
        <div className="table">
             <HtmlContent html={technologies.value} />
        </div>
       
      </div>
    </div>
  ) : (
    <></>
  );
};

export default ResultZAP;
