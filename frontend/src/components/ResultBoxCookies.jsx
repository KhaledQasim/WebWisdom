/* eslint-disable react/prop-types */
/* eslint-disable no-unused-vars */
import StateOfBox from "./StateOfBox";
import { useSignals, useSignalEffect } from "@preact/signals-react/runtime";
import { signal } from "@preact/signals-react";
import Loading from "./Loading";

const cookies = signal();
const loading = signal(true);

const ResultBoxCookies = ({
  MainTitle,
  MainContent,
  title,
  content,
  good,
  data,
}) => {
  useSignals();

  useSignalEffect(() => {
    if (data.value.data[3]?.cookies !== null && !isEmptyObject(data.value.data[3]?.cookies)) {
      cookies.value = data.value.data[3].cookies;
    } else {
      cookies.value = false;
    }
  
    loading.value = false;
  });
  function isEmptyObject(obj) {
    return Object.keys(obj).length === 0 && obj.constructor === Object;
  }

  return loading.value ? (
    <Loading />
  ) : cookies.value ? (
    <div className="bg-base-200 container grid mx-auto mt-10">
      <div className=" text-4xl text-center bg-primary/95 rounded-lg h-16">
        <div className="object-center mt-2">{MainTitle}</div>
      </div>
      <div className="my-5 px-4 text-base ">{MainContent}</div>
      {cookies.value.map((cookies,index) => (
        <div key={index}>
          <div className="text-accent px-4 text-xl grid gap-1">
            {cookies.IssueDetail+", Risk Level: "+cookies.RiskLevel}
            <div className="border-b-2 border-base-content" />

            <StateOfBox
              content={"Description of Issue: "+cookies.Description}
              good={"neutral"}
              subHeading={""}
            />
            <StateOfBox
              content={"Recommendation to solve the issue: "+cookies.Recommendation}
              good={"neutral"}
              subHeading={""}
            />
            <StateOfBox
              content={"Evidence Detail: "+cookies.Evidence.EvidenceDetail+", -- Cookie Name: "+cookies.Evidence.CookieName+", -- URL of Cookie: "+cookies.Evidence.URL}
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

export default ResultBoxCookies;

