/* eslint-disable react/prop-types */
/* eslint-disable no-unused-vars */
import StateOfBox from "./StateOfBox";
import { useSignals, useSignalEffect } from "@preact/signals-react/runtime";
import { signal } from "@preact/signals-react";
import Loading from "./Loading";

const technologies = signal();
const loading = signal(true);

const ResultBoxTechnologies = ({
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
   
    if (data.value[indexPTT]?.report[0].technologies !== null && !isEmptyObject(data.value[indexPTT]?.report[0].technologies)) {
      technologies.value = data.value[indexPTT]?.report[0].technologies;
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
      {technologies.value.map((software) => (
        <div key={software.software_name}>
          <div className="text-accent px-4 text-xl grid gap-1">
            {software.software_name}
            <div className="border-b-2 border-base-content" />

            <StateOfBox
              content={"Version: " + software.software_version}
              good={"neutral"}
              subHeading={software.category}
            />
          </div>
        </div>
      ))}
    </div>
  ) : (
    <></>
  );
};

export default ResultBoxTechnologies;

// {data.map((software) => {
//     <div key={software.software_name}>
//       <div className="text-accent px-4 text-xl grid gap-1">
//         {title}
//         <div className="border-b-2 border-base-content" />

//         <StateOfBox content={"content"} good={"good"} subHeading={"sub"} />
//       </div>
//     </div>
//   })}
