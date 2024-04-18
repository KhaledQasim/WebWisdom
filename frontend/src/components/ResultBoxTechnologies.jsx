/* eslint-disable react/prop-types */
/* eslint-disable no-unused-vars */
import StateOfBox from "./StateOfBox";

const ResultBoxTechnologies = ({
  MainTitle,
  MainContent,
  title,
  content,
  good,
  data,
}) => {
  return (
    <div className="bg-base-200 container grid mx-auto mt-10">
      <div className=" text-4xl text-center bg-primary rounded-lg h-16">
        <div className="object-center mt-2">{MainTitle}</div>
      </div>
      <div className="my-5 px-4 text-base ">{MainContent}</div>
      {data.map((software) => (
        <div key={software.software_name}>
          <div className="text-accent px-4 text-xl grid gap-1">
            {software.software_name}
            <div className="border-b-2 border-base-content" />

            <StateOfBox content={"Version: "+software.software_version} good={"neutral"} subHeading={software.category} />
          </div>
        </div>
      ))}
    </div>
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
