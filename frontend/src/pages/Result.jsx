import { axiosStartScan } from "../api/axios";
import { useSignals, useSignalEffect } from "@preact/signals-react/runtime";
import { signal } from "@preact/signals-react";

import ResultBox from "../components/ResultBox";
import ResultSummary from "../components/ResultSummary";
import { useEffect } from "react";

const resultData = signal();
let port = ""


export default function Result() {

  useSignals();
  useSignalEffect(()=>{
    resultData.value = JSON.parse(localStorage.getItem("resultData"))
    console.log(resultData.value.connection_and_records.port_80)
    port = JSON.stringify(resultData.value.connection_and_records.port_80)
  })

  return (
    <>
      <ResultSummary content={"result summary content"}/>
      <ResultBox title={port} content={"result box content"} MainTitle={"result main title"} MainContent={"main content"} good={false}/>
    </>
  );
}
