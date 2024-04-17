import { axiosGetResultByID } from "../api/axios";
import { useSignals, useSignalEffect } from "@preact/signals-react/runtime";
import { signal } from "@preact/signals-react";
import Loading from "../components/Loading";
import ResultBox from "../components/ResultBox";
import ResultSummary from "../components/ResultSummary";
import { useParams } from "react-router-dom";
import { useEffect } from 'react';

const resultData = signal();
const loading = signal(true);
const port = signal();
const idOfResult = signal();

export default function Result() {
  useSignals();
  const { id } = useParams();
  idOfResult.value = id
  
 
  useSignalEffect(() => {
    
    axiosGetResultByID
      .post(`${idOfResult.value}`)
      .then((response) => {
        if (response.status === 200) {
          resultData.value = JSON.parse(response.data.result);
          console.log(resultData.value);
          port.value = JSON.stringify(
            resultData.value.connection_and_records.url
          );
          loading.value = false;
        }
      })
      .catch((error) => {
        console.error("there was an error in Result page", error);
        loading.value = false;
      });
  });

  return (
    <>
      {loading.value ? (
        <>
          <Loading />
        </>
      ) : (
        <>
          <ResultSummary content={"result summary content"} />
          <ResultBox
            title={port.value}
            content={"result box content "+ idOfResult.value}
            MainTitle={"result main title"}
            MainContent={"main content"}
            good={false}
          />
        </>
      )}
    </>
  );
}
