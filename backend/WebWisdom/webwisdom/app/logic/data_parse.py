import subprocess
from fastapi import FastAPI, HTTPException

import re





def get_vulnerability_report(url):
    

    command = f'ptt -q --nocolor run website_scanner {url}'


    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    print(result.stdout)
    return result.stdout




def parse_vulnerability_report_for_technologies(report_text:str):
    lines = report_text.split('\n')
    in_technology_section = False
    technologies = []
    i = 0  # Line index

    while i < len(lines):
        line = lines[i].strip()
        
        if 'Server software and technology found' in line:
            in_technology_section = True
            i += 1
            continue
        
      
        if in_technology_section and line.startswith('['):

            # Exiting the loop if reached the next section
            break
        
        if in_technology_section and '- Evidence' in line:
            technology = {}
            while True:
                i += 1
                if i >= len(lines):
                    break
                line = lines[i].strip()

                if line.startswith('- Software / Version:'):
                    software_version_full = line.split(':', 1)[1].strip()
                    parts = software_version_full.rsplit(' ', 1)
                    if len(parts) == 2 and any(char.isdigit() for char in parts[1]):
                        technology['software_name'], technology['software_version'] = parts
                    else:
                        technology['software_name'] = software_version_full
                        technology['software_version'] = "Unknown"
                elif line.startswith('- Category:'):
                    technology['category'] = line.split(':', 1)[1].strip()
                elif line.startswith('[') or line.startswith('- Evidence') or line.strip() == '':
                    # Break if another evidence starts or if an unrelated line is reached
                    break

            technologies.append(technology)
            
            continue  # Skip the increment at the end of the loop since we've already moved to the next line
        
        i += 1  # Move to the next line
        
    # Removing any empty dictionaries at the end of the list
    technologies = [technology for technology in technologies if technology]
    return technologies





def parse_vulnerability_report_for_headers(report_text:str):
    # Define the pattern to capture required fields
    pattern = r"Missing security header: (\S.*?)\n\s*- Risk Level: (\d+ \(\w+\))\n.*?Vulnerability Details:\s*(?:- Evidence \d+:\s*\n\s*- URL: (.*?)\n\s*- Evidence: (.*?)\n)?\s*- Description: (.*?)\n\s*- Recommendation: (.*?)\n"
    results = []
    matches = re.finditer(pattern, report_text, re.DOTALL)

    for match in matches:
        header, risk_level, url, evidence, description, recommendation = match.groups()
        result = {
            "MissingSecurityHeader": header.strip(),
            "RiskLevel": risk_level.strip(),
            "Description": description.strip(),
            "Recommendation": recommendation.strip(),
            "Evidence": {
                    "URL": url.strip() if url else "No URL provided",
                    "EvidenceDetail": evidence.strip() if evidence else "No evidence detail provided"
            }
        }
        results.append(result)
    
    
    
    pattern = r"Unsafe security header: (\S.*?)\n\s*- Risk Level: (\d+ \(\w+\))\n.*?Vulnerability Details:\s*(?:- Evidence \d+:\s*\n\s*- URL: (.*?)\n\s*- Evidence: (.*?)\n)?\s*- Description: (.*?)\n\s*- Recommendation: (.*?)\n"
    matches = re.finditer(pattern, report_text, re.DOTALL)

    for match in matches:
        header, risk_level, url, evidence, description, recommendation = match.groups()
        result = {
            "UnsafeSecurityHeader": header.strip(),
            "RiskLevel": risk_level.strip(),
            "Description": description.strip(),
            "Recommendation": recommendation.strip(),
            "Evidence": {
                    "URL": url.strip() if url else "No URL provided",
                    "EvidenceDetail": evidence.strip() if evidence else "No evidence detail provided"
            }
        }
        results.append(result)
    
    
    
    
    # Parsing the provided text
    if not report_text.strip():
        raise HTTPException(status_code=400, detail="No text provided")
    
    return results



def parse_vulnerability_report_for_txt_files(report_text:str):
    security_txt_pattern = r"Security\.txt file.*?\n\s*- Risk Level:\s*(\d+ \(\w+\))\n.*?Description:\s*(.*?)\n\s*- Recommendation:\s*(.*?)\n"
    robots_txt_pattern = r"Robots\.txt file.*?\n\s*- Risk Level:\s*(\d+ \(\w+\))\n.*?Description:\s*(.*?)\n\s*- Recommendation:\s*(.*?)\n"
    
    results = []

    # Search for Security.txt file details
    security_txt_match = re.search(security_txt_pattern, report_text, re.DOTALL)
    if security_txt_match:
        risk_level, description, recommendation = security_txt_match.groups()
        results.append({
            "File": "Security.txt",
            "RiskLevel": risk_level.strip(),
            "Description": description.strip(),
            "Recommendation": recommendation.strip()
        })

    # Search for Robots.txt file details
    robots_txt_match = re.search(robots_txt_pattern, report_text, re.DOTALL)
    if robots_txt_match:
        risk_level, description, recommendation = robots_txt_match.groups()
        results.append({
            "File": "Robots.txt",
            "RiskLevel": risk_level.strip(),
            "Description": description.strip(),
            "Recommendation": recommendation.strip()
        })

    return results


def parse_vulnerability_report_for_insecure_cookie(report_text:str):
    pattern = (
            r"cookie\s*(.*?)\n\s*- Risk Level: (\d+ \(\w+\))\n.*?"
            r"Vulnerability Details:\s*(?:- Evidence \d+:\s*\n"
            r"\s*- URL: (.*?)\n"
            r"\s*- Cookie Name: (.*?)\n"  # Capturing cookie name
            r"\s*- Evidence: (.*?)\n)?"
            r"\s*- Description: (.*?)\n"
            r"\s*- Recommendation: (.*?)\n"
        )

    results = []
    matches = re.finditer(pattern, report_text, re.DOTALL | re.IGNORECASE)

    for match in matches:
        issue_detail, risk_level, url, cookie_name, evidence, description, recommendation = match.groups()
        result = {
            "IssueDetail": issue_detail.strip(),
            "RiskLevel": risk_level.strip(),
            "Description": description.strip(),
            "Recommendation": recommendation.strip(),
            "Evidence": {
                "URL": url.strip() if url else "No URL provided",
                "CookieName": cookie_name.strip() if cookie_name else "No cookie name provided",
                "EvidenceDetail": evidence.strip() if evidence else "No evidence detail provided"
            }
        }
        results.append(result)

    return results


def formate_report(url):
    print("urlhere",url)
    report_text = get_vulnerability_report(url)
    technologies = parse_vulnerability_report_for_technologies(report_text)
    headers = parse_vulnerability_report_for_headers(report_text)
    files = parse_vulnerability_report_for_txt_files(report_text)
    cookies = parse_vulnerability_report_for_insecure_cookie(report_text)
    return [{"technologies":technologies},{"headers":headers},{"files":files},{"cookies":cookies}]



def formate_report_test():
    technologies = parse_vulnerability_report_for_technologies(ReportSample)
    headers = parse_vulnerability_report_for_headers(ReportSample)
    files = parse_vulnerability_report_for_txt_files(ReportSample)
    cookies = parse_vulnerability_report_for_insecure_cookie(ReportSample)
    return [{"technologies":technologies},{"headers":headers},{"files":files},{"cookies":cookies}]























ReportSample = '''
+----------------------------------------------------------+
|                Vulnerability Scan Report                 |
+----------------------------------------------------------+


[1] Insecure cookie setting: domain too loose
        - Risk Level: 2 (Medium)

        Vulnerability Details:
        - Evidence 1:
                - URL: https://www.youtube.com/
                - Cookie Name: YSC
                - Evidence: Set-Cookie: .youtube.com


        - Description: We found that the target application sets cookies with a domain scope that is too broad. Specifically, cookies intended for use within a particular application are configured in such a way that they can be accessed by multiple subdomains of the same primary domain.
        - Recommendation: The `Domain` attribute should be set to the origin host to limit the scope to that particular server. For example if the application resides on server app.mysite.com, then it should be set to `Domain=app.mysite.com`


[2] Missing security header: Referrer-Policy
        - Risk Level: 1 (Low)

        Vulnerability Details:
        - Evidence 1:
                - URL: https://www.youtube.com/
                - Evidence: Response headers do not include the Referrer-Policy HTTP security header as well as the <meta> tag with name 'referrer' is not present in the response.


        - Description: We noticed that the target application's server responses lack the <code>Referrer-Policy</code> HTTP header, which controls how much referrer information the browser will send with each request originated from the current web application.
        - Recommendation: The Referrer-Policy header should be configured on the server side to avoid user tracking and inadvertent information leakage. The value `no-referrer` of this header instructs the browser to omit the Referer header entirely.


[3] Missing security header: Content-Security-Policy
        - Risk Level: 1 (Low)

        Vulnerability Details:
        - Evidence 1:
                - URL: https://www.youtube.com/
                - Evidence: Response does not include the HTTP Content-Security-Policy security header or meta tag


        - Description: We noticed that the target application lacks the Content-Security-Policy (CSP) header in its HTTP responses. The CSP header is a security measure that instructs web browsers to enforce specific security rules, effectively preventing the exploitation of Cross-Site Scripting (XSS) vulnerabilities.
        - Recommendation: Configure the Content-Security-Header to be sent with each HTTP response in order to apply the specific policies needed by the application.


[4] Missing security header: Strict-Transport-Security
        - Risk Level: 1 (Low)

        Vulnerability Details:
        - Evidence 1:
                - URL: https://www.youtube.com/s/desktop/f45068c8/img
                - Evidence: Response headers do not include the HTTP Strict-Transport-Security header


        - Description: We noticed that the target application lacks the HTTP Strict-Transport-Security header in its responses. This security header is crucial as it instructs browsers to only establish secure (HTTPS) connections with the web server and reject any HTTP connections.
        - Recommendation: The Strict-Transport-Security HTTP header should be sent with each HTTPS response. The syntax is as follows: `Strict-Transport-Security: max-age=&lt;seconds>[; includeSubDomains]` The parameter `max-age` gives the time frame for requirement of HTTPS in seconds and should be chosen quite high, e.g. several months. A value below 7776000 is considered as too low by this scanner check. The flag `includeSubDomains` defines that the policy applies also for sub domains of the sender of the response.


[5] Unsafe security header: Content-Security-Policy
        - Risk Level: 1 (Low)

        Vulnerability Details:
        - Evidence 1:
                - URL: https://www.youtube.com/t
                - Evidence: Response headers include the HTTP Content-Security-Policy security header with the following security issues: `report-uri: report-uri is deprecated in CSP3. Please use the report-to directive instead.` `default-src: The default-src directive should be set as a fall-back when other restrictions have not been specified. ` `script-src: ''unsafe-inline'' allows the execution of unsafe in-page scripts and event handlers.` `script-src: Nonces should only use the base64 charset.`


        - Description: We noticed that the Content-Security-Policy (CSP) header configured for the web application includes unsafe directives. The CSP header activates a protection mechanism implemented in web browsers which prevents exploitation of Cross-Site Scripting vulnerabilities (XSS) by restricting the sources from which content can be loaded or executed.
        - Recommendation: Remove the unsafe values from the directives, adopt nonces or hashes for safer inclusion of inline scripts if they are needed, and explicitly define the sources from which scripts, styles, images or other resources can be loaded.


[6] Server software and technology found
        - Risk Level: 1 (Low)

        Vulnerability Details:
        - Evidence 1:
                - Software / Version: YouTube
                - Category: Video players

        - Evidence 2:
                - Software / Version: Google Ads
                - Category: Advertising

        - Evidence 3:
                - Software / Version: HTTP/3
                - Category: Miscellaneous

        - Evidence 4:
                - Software / Version: Google Ads Conversion Tracking
                - Category: Analytics

        - Evidence 5:
                - Software / Version: Webpack
                - Category: Miscellaneous

        - Evidence 6:
                - Software / Version: Module Federation
                - Category: Miscellaneous

        - Evidence 7:
                - Software / Version: reCAPTCHA
                - Category: Security

        - Evidence 8:
                - Software / Version: HSTS
                - Category: Security


        - Description: We noticed that server software and technology details are exposed, potentially aiding attackers in tailoring specific exploits against identified systems and versions.
        - Recommendation: We recommend you to eliminate the information which permits the identification of software platform, technology, server and operating system: HTTP server headers, HTML meta information, etc.


[7] Robots.txt file found
        - Risk Level: 1 (Low)

        Vulnerability Details:
        - Evidence 1:
                - URL: https://www.youtube.com/robots.txt


        - Description: We found the robots.txt on the target server. This file instructs web crawlers what URLs and endpoints of the web application they can visit and crawl. Website administrators often misuse this file while attempting to hide some web pages from the users.
        - Recommendation: We recommend you to manually review the entries from robots.txt and remove the ones which lead to sensitive locations in the website (ex. administration panels, configuration files, etc).


[8] Website is accessible.
[9] Nothing was found for vulnerabilities of server-side software.
[10] Nothing was found for client access policies.
[11] Nothing was found for absence of the security.txt file.
[12] Nothing was found for use of untrusted certificates.
[13] Nothing was found for enabled HTTP debug methods.
[14] Nothing was found for secure communication.
[15] Nothing was found for directory listing.
[16] Nothing was found for missing HTTP header -  X-Content-Type-Options.
[17] Nothing was found for HttpOnly flag of cookie.
[18] Nothing was found for Secure flag of cookie.

+----------------- TEST summary -----------------+
|                                                |
|  URL: https://www.youtube.com/                 |
|  High Risk Findings: 0                         |
|  Medium Risk Findings: 1                       |
|  Low Risk Findings: 6                          |
|  Info Risk Findings: 11                        |
|  Start time: 2024-04-14 22:51:52               |
|  End time: 2024-04-14 22:53:06                 |
|                                                |
+------------------------------------------------+
'''
