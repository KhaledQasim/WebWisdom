import { axiosGetResultByID } from "../api/axios";
import { useSignals, useSignalEffect } from "@preact/signals-react/runtime";
import { signal } from "@preact/signals-react";
import Loading from "../components/Loading";
import ResultBox from "../components/ResultBox";
import ResultSummary from "../components/ResultSummary";
import ResultBoxWithIP from "../components/ResultBoxWithIP";
import ResultBoxTechnologies from "../components/ResultBoxTechnologies";
import { useParams } from "react-router-dom";

const resultData = signal();
const loading = signal(true);
const idOfResult = signal();
const ipKeys = signal();

export default function Result() {
  useSignals();
  const { id } = useParams();
  idOfResult.value = id;

  useSignalEffect(() => {
    axiosGetResultByID
      .post(`${idOfResult.value}`)
      .then((response) => {
        if (response.status === 200) {
          resultData.value = JSON.parse(response.data.result);
          console.log("result data in results page",resultData.value);
          handleDataVariables();
        }
      })
      .catch((error) => {
        console.error("there was an error in Result page", error);
        loading.value = false;
      });
  });

  function isEmptyObject(obj) {
    return Object.keys(obj).length === 0 && obj.constructor === Object;
  }

  function handleDataVariables() {
    // get A record IPs object keys
    ipKeys.value = Object.keys(resultData.value.connection_and_records).filter(
      (key) => key.startsWith("IP_")
    );

    loading.value = false;
  }

  return (
    <>
      {loading.value ? (
        <>
          <Loading />
        </>
      ) : (
        <>
          <ResultSummary content={"result summary content"} />

          {/* Box for connection records */}
          <ResultBoxWithIP
            title={"Connection Records"}
            content={"result box content "}
            MainTitle={"Connection Records"}
            MainContent={"Details about the target site"}
            good={"neutral"}
            data={resultData}
            ipKeys={ipKeys}
            subHeading={"sub"}
          />

          {/* Box for Technologies used on the website*/}
          {/* {
            // check that the object technologies is present in the data array
            resultData.value.data.find((item) =>
              Object.prototype.hasOwnProperty.call(item, "technologies")
            ) ? (
              <ResultBoxTechnologies
                // array of objects that contain the technologies used on the website, including name version and category
                data={resultData.value.data[0].technologies}
                content={"result box content "}
                MainTitle={"Technologies"}
                MainContent={"List of the technologies used on the website"}
                good={"neutral"}
              />
            ) : (
              console.warn("No technologies object inside the data array.")
            )
          } */}
        </>
      )}
    </>
  );
}
