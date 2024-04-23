/* eslint-disable react/prop-types */
/* eslint-disable no-unused-vars */
import StateOfBox from "./StateOfBox";
import { useSignals, useSignalEffect } from "@preact/signals-react/runtime";
import { signal } from "@preact/signals-react";
import Loading from "./Loading";

const nmap = signal();
const nmapMysql = signal();

const loading = signal(true);

const ResultBoxWithIP = ({
  MainTitle,
  MainContent,
  title,
  content,
  good,
  data,
  ipKeys,
  subHeading,
}) => {
  useSignals();

  useSignalEffect(() => {
    if (
      data.value.data[4]?.nmap !== null &&
      !isEmptyObject(data.value.data[4]?.nmap)
    ) {
      nmap.value = data.value.data[4];
    } else {
      nmap.value = false;
    }

   
    const isThereMysql = data.value.data[4].nmap[1] === undefined;
    if (!isThereMysql) {
      nmapMysql.value = nmap.value.nmap[1].VulnerabilityFound;
    } else {
    
      nmapMysql.value = false;
    }

    
    loading.value = false;
  });
  function isEmptyObject(obj) {
    return Object.keys(obj).length === 0 && obj.constructor === Object;
  }
  return loading.value ? (
    <Loading />
  ) : (
    <>
      <div className="bg-base-200 container grid mx-auto mt-10">
        <div className=" text-4xl text-center bg-primary/95 rounded-lg h-16">
          <div className="object-center mt-2">
            Basic Website Information - {data.value.connection_and_records.url}
          </div>
        </div>
        <div className="my-5 px-4 text-base ">{MainContent}</div>

        {/* Displaying the A record IPs */}
        {ipKeys.value.map((key, index) => (
          <div key={index}>
            <div className="text-accent px-4 text-xl grid gap-1">
              A record IPs
              <div className="border-b-2 border-base-content" />
              <StateOfBox
                content={String(data.value.connection_and_records[key])}
                good={good}
                subHeading={
                  "This is the IP address of the website, It can have other IPs especially if behind a proxy."
                }
              />
            </div>
          </div>
        ))}

        <div className="text-accent px-4 text-xl grid gap-1">
          Secure Socket Layer SSL
          <div className="border-b-2 border-base-content" />
          {data.value.connection_and_records.ssl ? (
            <StateOfBox
              content={
                "SSL is enabled and communication was established on port 443, this means that communication is encrypted and resilient to man in the middle (MitM) attacks"
              }
              good={good}
              subHeading={""}
            />
          ) : (
            <StateOfBox
              content={
                "SSL is disabled and communication cloud not be established on port 443, this means that communication is NOT encrypted and is vulnerable to man in the middle (MitM) attacks!"
              }
              good={"bad"}
              subHeading={""}
            />
          )}
        </div>

        {nmap.value ? (
          <>
            <div className="text-accent px-4 text-xl grid gap-1">
              Open Ports - These ports are used to communicate with the server,
              if there is a service port that does not represent the required
              public functionality of the webserver, then it must be
              investigated and closed if deemed malicious.
              {nmap.value.nmap[0].data?.map((key, index) => (
                <div key={index}>
                  <div className="border-b-2 border-base-content" />
                  <StateOfBox
                    content={key.port + "/" + key.protocol}
                    good={good}
                    subHeading={key.service}
                  />
                </div>
              ))}
              {nmapMysql.value ? (
                <>
                  <div className="border-b-2 border-base-content" />
                  <StateOfBox
                    content={nmapMysql.value.detail}
                    good={"warning"}
                    subHeading={nmapMysql.value.RiskLevel}
                  />
                </>
              ) : (
                <></>
              )}
            </div>
          </>
        ) : (
          <></>
        )}
      </div>
    </>
  );
};

export default ResultBoxWithIP;
