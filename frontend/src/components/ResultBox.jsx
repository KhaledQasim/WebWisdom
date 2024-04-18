/* eslint-disable react/prop-types */
/* eslint-disable no-unused-vars */
import StateOfBox from "./StateOfBox";


const ResultBox = ({ MainTitle, MainContent, title, content, good }) => {
  return (
    <div className="bg-base-200 container grid mx-auto mt-5">
      <div className=" text-4xl text-center bg-primary rounded-lg h-16">
        <div className="object-center mt-2">
            {MainTitle}
        </div>
      </div>
      <div className="my-5 px-4 text-base ">{MainContent}</div>

      <div className="text-accent px-4 text-xl grid gap-1">
        {title}
        <div className="border-b-2 border-base-content" />
        
        <StateOfBox content={content} good={good}/>
      </div>
    </div>
  );
};

export default ResultBox;
