import { axiosGetResultByID } from "../api/axios";
import { useSignals, useSignalEffect } from "@preact/signals-react/runtime";
import { signal } from "@preact/signals-react";
import Loading from "../components/Loading";
import ResultBox from "../components/ResultBox";
import ResultSummary from "../components/ResultSummary";
import ResultBoxWithIP from "../components/ResultBoxWithIP";
import { useParams } from "react-router-dom";

const resultData = signal();
const loading = signal(true);
const port = signal();
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
          console.log(resultData.value);
          handleDataVariables();
        }
      })
      .catch((error) => {
        console.error("there was an error in Result page", error);
        loading.value = false;
      });
  });

  function handleDataVariables() {
    // get A record IPs object keys
    ipKeys.value = Object.keys(resultData.value.connection_and_records).filter(key => key.startsWith("IP_"));
    
    port.value = JSON.stringify(resultData.value.connection_and_records.url);
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
            content={"result box content " + idOfResult.value}
            MainTitle={"Connection Records"}
            MainContent={"Details about the target site"}
            good={"neutral"}
            data={resultData.value}
            ipKeys={ipKeys.value}
          />

          {/* Box for missing headers*/}
          <ResultBox
            title={"Technology"}
            content={"result box content " + idOfResult.value}
            MainTitle={"Technologies"}
            MainContent={"Details about the technologies used on the website"}
            good={"neutral"}
          />
        </>
      )}
    </>
  );
}

