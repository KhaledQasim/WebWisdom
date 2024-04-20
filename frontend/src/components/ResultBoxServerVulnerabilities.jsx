/* eslint-disable react/prop-types */
/* eslint-disable no-unused-vars */
import StateOfBox from "./StateOfBox";
import { useSignals, useSignalEffect } from "@preact/signals-react/runtime";
import { signal } from "@preact/signals-react";
import Loading from "./Loading";

const serverVulnerabilities = signal();
const loading = signal(true);

const ResultBoxServerVulnerabilities = ({
  MainTitle,
  MainContent,
  title,
  content,
  good,
  data,
}) => {
  useSignals();

  useSignalEffect(() => {

    if (data.value.data[5]?.serverVulnerabilities !== null &&  !isEmptyObject(data.value.data[5]?.serverVulnerabilities)) {
      serverVulnerabilities.value = data.value.data[5].serverVulnerabilities;
    } else {
      serverVulnerabilities.value = false;
    }


    loading.value = false;
  });
  function isEmptyObject(obj) {
    return Object.keys(obj).length === 0 && obj.constructor === Object;
  }

  return loading.value ? (
    <Loading />
  ) : serverVulnerabilities.value ? (
    <div className="bg-base-200 container grid mx-auto mt-10">
      <div className=" text-4xl text-center bg-primary/95 rounded-lg h-16">
        <div className="object-center mt-2">{MainTitle}</div>
      </div>
      <div className="my-5 px-4 text-base ">{MainContent}</div>
      {serverVulnerabilities.value.cve_list.map((serverVulnerabilities,index) => (
        <div key={index}>
          <div className="text-accent px-4 text-xl grid gap-1">
            {serverVulnerabilities.id+" -- CVSS 0-10 (Common Vulnerability Scoring System) : "+serverVulnerabilities.CVSS}
            <div className="border-b-2 border-base-content" />

            <StateOfBox
              content={"Description of Issue: "+serverVulnerabilities.summary}
              good={"bad"}
              subHeading={"Affected Software: "+serverVulnerabilities.affected_software}
            />
        
         
            
          </div>
        </div>
      ))}
      
    </div>
  ) : (
    <></>
  );
};

export default ResultBoxServerVulnerabilities;

