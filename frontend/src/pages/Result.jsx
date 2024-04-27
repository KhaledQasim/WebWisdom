import { axiosGetResultByID } from "../api/axios";
import { useSignals, useSignalEffect } from "@preact/signals-react/runtime";
import { signal } from "@preact/signals-react";
import Loading from "../components/Loading";
import ResultSummary from "../components/ResultSummary";
import ResultBoxWithIP from "../components/ResultBoxWithIP";
import ResultBoxTechnologies from "../components/ResultBoxTechnologies";
import ResultBoxHeaders from "../components/ResultBoxHeaders";
import { useParams } from "react-router-dom";
import ResultBoxFiles from "../components/ResultBoxFiles";
import ResultBoxCookies from "../components/ResultBoxCookies";
import ResultBoxServerVulnerabilities from "../components/ResultBoxServerVulnerabilities";
import ResultZAP from "../components/ResultZAP";

const resultData = signal();
const loading = signal(true);
const idOfResult = signal();
const ipKeys = signal();
const isPttError = signal(true);


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
          console.log("result data: ", resultData.value);
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
    const indexIpKeys = resultData.value.findIndex(
      (item) => item.test === "connection_and_records"
    );
    const indexPTT = resultData.value.findIndex((item) => item.test === "PTT");
    if (
      String(resultData.value[indexPTT]?.report) ===
      "Error in generating base scan!"
    ) {
      isPttError.value = false;
    }



    ipKeys.value = Object.keys(resultData.value[indexIpKeys]?.report).filter(
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
          <ResultSummary data={resultData} />
          {isPttError.value ? (
            <>
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

              <ResultBoxTechnologies
                // array of objects that contain the technologies used on the website, including name version and category
                data={resultData}
                content={"result box content "}
                MainTitle={"Technologies"}
                MainContent={"List of the technologies used on the website"}
                good={"neutral"}
              />

              {/* Box for displaying headers information */}
              <ResultBoxHeaders
                data={resultData}
                MainTitle={"HTTP Headers"}
                MainContent={
                  "Information about the headers of the webserver, headers are information passed between a web browser and a website when it's visited"
                }
                good={"neutral"}
              />

              {/* Box for displaying configuration files found on webserver*/}
              <ResultBoxFiles
                data={resultData}
                MainTitle={"Files Found on WebServer"}
                MainContent={
                  "Information about some default files found on the webserver that can leak data about the inner workings of the webserver"
                }
                good={"neutral"}
              />

              {/* Box for displaying miss configured or insecure cookies*/}
              <ResultBoxCookies
                data={resultData}
                MainTitle={"Misconfigured or Insecure Cookies"}
                MainContent={
                  "Information about misconfigured or insecure Cookies found"
                }
                good={"neutral"}
              />

              {/* Box for displaying server side software vulnerabilities*/}
              <ResultBoxServerVulnerabilities
                data={resultData}
                MainTitle={"Server Side Vulnerabilities"}
                MainContent={
                  "Finds Server Side Vulnerabilities by identifying the server software that is running and which version it is, the security tool then checks the CVE (Common Vulnerabilities and Exposures) databases for vulnerabilities associated with this specific software. This can be a major vulnerability depending on the risk severity of the CVE"
                }
                good={"neutral"}
              />
            </>
          ) : (
            <>
              <div className="container mx-auto text-5xl text-primary">
                Error in generating base report!
              </div>
            </>
          )}

          <ResultZAP
            data={resultData}
            MainTitle={"ZAP Penetration Test Content"}
            MainContent={"This is the html report of the ZAP penetration test"}
            good={"neutral"}
          />
        </>
      )}
    </>
  );
}
