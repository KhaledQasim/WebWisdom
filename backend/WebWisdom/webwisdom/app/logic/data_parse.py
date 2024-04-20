import subprocess
from fastapi import FastAPI, HTTPException
from . import nmap
import re


def get_vulnerability_report(url):

    command = f'ptt -q --nocolor run website_scanner {url}'

    result = subprocess.run(
        command, capture_output=True, text=True, shell=True)
    print(result.stdout)
    return result.stdout


def parse_vulnerability_report_for_technologies(report_text: str):
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


def parse_vulnerability_report_for_headers(report_text: str):
    # Define the pattern to capture required fields
    pattern = r"Missing security header: (\S.*?)\n\s*- Risk Level: (\d+ \(\w+\))\n.*?Vulnerability Details:\s*(?:- Evidence \d+:\s*\n\s*- URL: (.*?)\n\s*- Evidence: (.*?)\n)?\s*- Description: (.*?)\n\s*- Recommendation: (.*?)\n"
    results = []
    matches = re.finditer(pattern, report_text, re.DOTALL)

    for match in matches:
        header, risk_level, url, evidence, description, recommendation = match.groups()
        result = {
            "Header": "Missing Security Header: "+header.strip(),
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
            "Header": "Unsafe Security Header: "+header.strip(),
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


def parse_vulnerability_report_for_txt_files(report_text: str):
    security_txt_pattern = r"Security\.txt file.*?\n\s*- Risk Level:\s*(\d+ \(\w+\))\n.*?Description:\s*(.*?)\n\s*- Recommendation:\s*(.*?)\n"
    robots_txt_pattern = r"Robots\.txt file.*?\n\s*- Risk Level:\s*(\d+ \(\w+\))\n.*?Description:\s*(.*?)\n\s*- Recommendation:\s*(.*?)\n"

    results = []

    # Search for Security.txt file details
    security_txt_match = re.search(
        security_txt_pattern, report_text, re.DOTALL)
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


def parse_vulnerability_report_for_insecure_cookie(report_text: str):

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


def parse_server_side_vulnerabilities(report_text: str):

    vulnerabilities = []

    # Start extracting from the specific section title
    vulnerability_section_start = re.search(
        r"Vulnerabilities found for server-side software\s*-\s*Risk Level: \d+ \((\w+)\)", report_text)

    if vulnerability_section_start:
        risk_level = vulnerability_section_start.group(1)

        # Start capturing after "Vulnerability Details:"
        vulnerability_details_section = report_text[vulnerability_section_start.end(
        ):]
        vulnerability_details_start = vulnerability_details_section.find(
            "Vulnerability Details:")
        vulnerability_details_text = vulnerability_details_section[vulnerability_details_start:]

        # Regular expression to capture each CVE detail
        cve_pattern = re.compile(
            r"- (CVE-\d+-\d+):\s*?\n\s*?-\s*?Risk Level:.*?\n\s*?-\s*?CVSS: (\d+\.\d+)\n\s*?-\s*?Summary: (.*?)\n\s*?-\s*?Affected software: (.+?)(?=\n\s*?-|$)", re.DOTALL)

        matches = cve_pattern.finditer(vulnerability_details_text)
        for match in matches:
            cve_id, cvss, summary, affected_software = match.groups()
            vulnerabilities.append({
                "id": cve_id,
                "CVSS": float(cvss),
                "summary": summary.strip(),
                "affected_software": affected_software.strip()
            })

        return {
            "title": "Vulnerabilities found for server-side software",
            "risk_level": risk_level,
            "cve_list": vulnerabilities
        }


def formate_report(url):
    print("urlhere", url)
    report_text = get_vulnerability_report(url)
    technologies = parse_vulnerability_report_for_technologies(report_text)
    headers = parse_vulnerability_report_for_headers(report_text)
    files = parse_vulnerability_report_for_txt_files(report_text)
    cookies = parse_vulnerability_report_for_insecure_cookie(report_text)
    nmap_object = nmap.nmap(str(url))
    nmap_scan_result = nmap_object.nmap_scan()
    server_side_vulnerabilities = parse_server_side_vulnerabilities(
        report_text)
    return [{"technologies": technologies}, {"headers": headers}, {"files": files}, {"cookies": cookies}, {"nmap": nmap_scan_result}, {"serverVulnerabilities": server_side_vulnerabilities}]


def formate_report_test():
    technologies = parse_vulnerability_report_for_technologies(ReportSample)
    headers = parse_vulnerability_report_for_headers(ReportSample)
    files = parse_vulnerability_report_for_txt_files(ReportSample)
    cookies = parse_vulnerability_report_for_insecure_cookie(ReportSample)
    nmap_object = nmap.nmap("url")
    nmap_scan_result = nmap_object.nmap_scan_test()
    server_side_vulnerabilities = parse_server_side_vulnerabilities(
        SeaViewReportSample)
    return [{"technologies": technologies}, {"headers": headers}, {"files": files}, {"cookies": cookies}, {"nmap": nmap_scan_result}, {"serverVulnerabilities": server_side_vulnerabilities}]


SeaViewReportSample = '''
+----------------------------------------------------------+
|                Vulnerability Scan Report                 |
+----------------------------------------------------------+


[1] Vulnerabilities found for server-side software
        - Risk Level: 3 (High)

        Vulnerability Details:
        - CVE-2020-13664:
                - Risk Level: 
                - CVSS: 9.3
                - Summary: Arbitrary PHP code execution vulnerability in Drupal Core under certain circumstances. An attacker could trick an administrator into visiting a malicious site that could result in creating a carefully named directory on the file system. With this directory in place, an attacker could attempt to brute force a remote code execution vulnerability. Windows servers are most likely to be affected. This issue affects: Drupal Drupal Core 8.8.x versions prior to 8.8.8; 8.9.x versions prior to 8.9.1; 9.0.1 versions prior to 9.0.1.
                - Affected software: drupal 9

        - CVE-2020-13665:
                - Risk Level: 
                - CVSS: 7.5
                - Summary: Access bypass vulnerability in Drupal Core allows JSON:API when JSON:API is in read/write mode. Only sites that have the read_only set to FALSE under jsonapi.settings config are vulnerable. This issue affects: Drupal Drupal Core 8.8.x versions prior to 8.8.8; 8.9.x versions prior to 8.9.1; 9.0.x versions prior to 9.0.1.
                - Affected software: drupal 9

        - CVE-2022-25273:
                - Risk Level: 
                - CVSS: 7.5
                - Summary: Drupal core's form API has a vulnerability where certain contributed or custom modules' forms may be vulnerable to improper input validation. This could allow an attacker to inject disallowed values or overwrite data. Affected forms are uncommon, but in certain cases an attacker could alter critical or sensitive data.
                - Affected software: drupal 9

        - CVE-2022-25275:
                - Risk Level: 
                - CVSS: 7.5
                - Summary: In some situations, the Image module does not correctly check access to image files not stored in the standard public files directory when generating derivative images using the image styles system. Access to a non-public file is checked only if it is stored in the "private" file system. However, some contributed modules provide additional file systems, or schemes, which may lead to this vulnerability. This vulnerability is mitigated by the fact that it only applies when the site sets (Drupal 9) $config['image.settings']['allow_insecure_derivatives'] or (Drupal 7) $conf['image_allow_insecure_derivatives'] to TRUE. The recommended and default setting is FALSE, and Drupal core does not provide a way to change that in the admin UI. Some sites may require configuration changes following this security release. Review the release notes for your Drupal version if you have issues accessing files or image styles after updating.
                - Affected software: drupal 9

        - CVE-2022-39261:
                - Risk Level: 
                - CVSS: 7.5
                - Summary: Twig is a template language for PHP. Versions 1.x prior to 1.44.7, 2.x prior to 2.15.3, and 3.x prior to 3.4.3 encounter an issue when the filesystem loader loads templates for which the name is a user input. It is possible to use the `source` or `include` statement to read arbitrary files from outside the templates' directory when using a namespace like `@somewhere/../some.file`. In such a case, validation is bypassed. Versions 1.44.7, 2.15.3, and 3.4.3 contain a fix for validation of such template names. There are no known workarounds aside from upgrading.
                - Affected software: drupal 9


        - Description: We noticed known vulnerabilities in the target application. They are usually related to outdated systems and expose the affected applications to the risk of unauthorized access to confidential data and possibly denial of service attacks.
        - Recommendation: We recommend you to upgrade the affected software to the latest version in order to eliminate the risk of these vulnerabilities.

        - Risk Level: 2 (Medium)

        Vulnerability Details:
        - CVE-2023-2745:
                - Risk Level: 
                - CVSS: 5.4
                - Summary: WordPress Core is vulnerable to Directory Traversal in versions up to, and including, 6.2, via the ‘wp_lang’ parameter. This allows unauthenticated attackers to access and load arbitrary translation files. In cases where an attacker is able to upload a crafted translation file onto the site, such as via an upload form, this could be also used to perform a Cross-Site Scripting attack.
                - Affected software: wordpress 6.2

        - CVE-2023-38000:
                - Risk Level: 
                - CVSS: 5.4
                - Summary: Auth. Stored (contributor+) Cross-Site Scripting (XSS) vulnerability in WordPress core 6.3 through 6.3.1, from 6.2 through 6.2.2, from 6.1 through 6.1.3, from 6.0 through 6.0.5, from 5.9 through 5.9.7 and Gutenberg plugin <= 16.8.0 versions.
                - Affected software: wordpress 6.2

        - CVE-2023-5561:
                - Risk Level: 
                - CVSS: 5.3
                - Summary: WordPress does not properly restrict which user fields are searchable via the REST API, allowing unauthenticated attackers to discern the email addresses of users who have published public posts on an affected website via an Oracle style attack
                - Affected software: wordpress 6.2

        - CVE-2023-39999:
                - Risk Level: 
                - CVSS: 4.3
                - Summary: Exposure of Sensitive Information to an Unauthorized Actor in WordPress from 6.3 through 6.3.1, from 6.2 through 6.2.2, from 6.1 through 6.13, from 6.0 through 6.0.5, from 5.9 through 5.9.7, from 5.8 through 5.8.7, from 5.7 through 5.7.9, from 5.6 through 5.6.11, from 5.5 through 5.5.12, from 5.4 through 5.4.13, from 5.3 through 5.3.15, from 5.2 through 5.2.18, from 5.1 through 5.1.16, from 5.0 through 5.0.19, from 4.9 through 4.9.23, from 4.8 through 4.8.22, from 4.7 through 4.7.26, from 4.6 through 4.6.26, from 4.5 through 4.5.29, from 4.4 through 4.4.30, from 4.3 through 4.3.31, from 4.2 through 4.2.35, from 4.1 through 4.1.38.
                - Affected software: wordpress 6.2


        - Description: We noticed known vulnerabilities in the target application. They are usually related to outdated systems and expose the affected applications to the risk of unauthorized access to confidential data and possibly denial of service attacks.
        - Recommendation: We recommend you to upgrade the affected software to the latest version in order to eliminate the risk of these vulnerabilities.


[2] Missing security header: Content-Security-Policy
        - Risk Level: 1 (Low)

        Vulnerability Details:
        - Evidence 1:
                - URL: https://seaview.gr/
                - Evidence: Response does not include the HTTP Content-Security-Policy security header or meta tag


        - Description: We noticed that the target application lacks the Content-Security-Policy (CSP) header in its HTTP responses. The CSP header is a security measure that instructs web browsers to enforce specific security rules, effectively preventing the exploitation of Cross-Site Scripting (XSS) vulnerabilities.
        - Recommendation: Configure the Content-Security-Header to be sent with each HTTP response in order to apply the specific policies needed by the application.


[3] Missing security header: Strict-Transport-Security
        - Risk Level: 1 (Low)

        Vulnerability Details:
        - Evidence 1:
                - URL: https://seaview.gr/
                - Evidence: Response headers do not include the HTTP Strict-Transport-Security header


        - Description: We noticed that the target application lacks the HTTP Strict-Transport-Security header in its responses. This security header is crucial as it instructs browsers to only establish secure (HTTPS) connections with the web server and reject any HTTP connections.
        - Recommendation: The Strict-Transport-Security HTTP header should be sent with each HTTPS response. The syntax is as follows: `Strict-Transport-Security: max-age=&lt;seconds>[; includeSubDomains]` The parameter `max-age` gives the time frame for requirement of HTTPS in seconds and should be chosen quite high, e.g. several months. A value below 7776000 is considered as too low by this scanner check. The flag `includeSubDomains` defines that the policy applies also for sub domains of the sender of the response.


[4] Missing security header: Referrer-Policy
        - Risk Level: 1 (Low)

        Vulnerability Details:
        - Evidence 1:
                - URL: https://seaview.gr/
                - Evidence: Response headers do not include the Referrer-Policy HTTP security header as well as the <meta> tag with name 'referrer' is not present in the response.


        - Description: We noticed that the target application's server responses lack the <code>Referrer-Policy</code> HTTP header, which controls how much referrer information the browser will send with each request originated from the current web application.
        - Recommendation: The Referrer-Policy header should be configured on the server side to avoid user tracking and inadvertent information leakage. The value `no-referrer` of this header instructs the browser to omit the Referer header entirely.


[5] Missing security header: X-Content-Type-Options
        - Risk Level: 1 (Low)

        Vulnerability Details:
        - Evidence 1:
                - URL: https://seaview.gr/
                - Evidence: Response headers do not include the X-Content-Type-Options HTTP security header


        - Description: We noticed that the target application's server responses lack the <code>X-Content-Type-Options</code> header. This header is particularly important for preventing Internet Explorer from reinterpreting the content of a web page (MIME-sniffing) and thus overriding the value of the Content-Type header.
        - Recommendation: We recommend setting the X-Content-Type-Options header such as `X-Content-Type-Options: nosniff`.


[6] Server software and technology found
        - Risk Level: 1 (Low)

        Vulnerability Details:
        - Evidence 1:
                - Software / Version: Facebook Pixel 2.9.154
                - Category: Analytics

        - Evidence 2:
                - Software / Version: FancyBox 3.5.7
                - Category: JavaScript libraries

        - Evidence 3:
                - Software / Version: Google Analytics
                - Category: Analytics

        - Evidence 4:
                - Software / Version: Google Font API
                - Category: Font scripts

        - Evidence 5:
                - Software / Version: jQuery UI 1.11.1
                - Category: JavaScript libraries

        - Evidence 6:
                - Software / Version: MySQL
                - Category: Databases

        - Evidence 7:
                - Software / Version: Nginx
                - Category: Web servers, Reverse proxies

        - Evidence 8:
                - Software / Version: PHP
                - Category: Programming languages

        - Evidence 9:
                - Software / Version: Google Tag Manager
                - Category: Tag managers

        - Evidence 10:
                - Software / Version: jQuery CDN
                - Category: CDN

        - Evidence 11:
                - Software / Version: Contact Form 7 5.8.3
                - Category: WordPress plugins

        - Evidence 12:
                - Software / Version: jQuery Migrate 3.4.0
                - Category: JavaScript libraries

        - Evidence 13:
                - Software / Version: core-js 3.19.1
                - Category: JavaScript libraries

        - Evidence 14:
                - Software / Version: Isotope
                - Category: JavaScript libraries

        - Evidence 15:
                - Software / Version: jQuery 3.5.1
                - Category: JavaScript libraries

        - Evidence 16:
                - Software / Version: Open Graph
                - Category: Miscellaneous

        - Evidence 17:
                - Software / Version: Polyfill 3
                - Category: JavaScript libraries

        - Evidence 18:
                - Software / Version: Webpack
                - Category: Miscellaneous

        - Evidence 19:
                - Software / Version: Module Federation
                - Category: Miscellaneous

        - Evidence 20:
                - Software / Version: FlexSlider
                - Category: Widgets

        - Evidence 21:
                - Software / Version: WordPress 6.2
                - Category: CMS, Blogs

        - Evidence 22:
                - Software / Version: reCAPTCHA
                - Category: Security

        - Evidence 23:
                - Software / Version: jsDelivr
                - Category: CDN

        - Evidence 24:
                - Software / Version: Osano
                - Category: Cookie compliance

        - Evidence 25:
                - Software / Version: Plesk
                - Category: Hosting panels

        - Evidence 26:
                - Software / Version: RateParity
                - Category: Widgets

        - Evidence 27:
                - Software / Version: RSS
                - Category: Miscellaneous


        - Description: We noticed that server software and technology details are exposed, potentially aiding attackers in tailoring specific exploits against identified systems and versions.
        - Recommendation: We recommend you to eliminate the information which permits the identification of software platform, technology, server and operating system: HTTP server headers, HTML meta information, etc.


[7] Robots.txt file found
        - Risk Level: 1 (Low)

        Vulnerability Details:
        - Evidence 1:
                - URL: https://seaview.gr/robots.txt


        - Description: We found the robots.txt on the target server. This file instructs web crawlers what URLs and endpoints of the web application they can visit and crawl. Website administrators often misuse this file while attempting to hide some web pages from the users.
        - Recommendation: We recommend you to manually review the entries from robots.txt and remove the ones which lead to sensitive locations in the website (ex. administration panels, configuration files, etc).


[8] Security.txt file is missing
        - Risk Level: 0 (Info)

        Vulnerability Details:
        - Evidence 1:
                - URL: Missing: https://seaview.gr/.well-known/security.txt


        - Description: We have noticed that the server is missing the security.txt file, which is considered a good practice for web security. It provides a standardized way for security researchers and the public to report security vulnerabilities or concerns by outlining the preferred method of contact and reporting procedures.
        - Recommendation: We recommend you to implement the security.txt file according to the standard, in order to allow researchers or users report any security issues they find, improving the defensive mechanisms of your server.


[9] Website is accessible.
[10] Nothing was found for client access policies.
[11] Nothing was found for use of untrusted certificates.
[12] Nothing was found for enabled HTTP debug methods.
[13] Nothing was found for secure communication.
[14] Nothing was found for directory listing.
[15] Nothing was found for domain too loose set for cookies.
[16] Nothing was found for HttpOnly flag of cookie.
[17] Nothing was found for Secure flag of cookie.
[18] Nothing was found for unsafe HTTP header Content Security Policy.

+----------------- TEST summary -----------------+
|                                                |
|  URL: https://seaview.gr/                      |
|  High Risk Findings: 0                         |
|  Medium Risk Findings: 1                       |
|  Low Risk Findings: 6                          |
|  Info Risk Findings: 11                        |
|  Start time: 2024-04-20 22:27:39               |
|  End time: 2024-04-20 22:28:20                 |
|                                                |
+------------------------------------------------+


[{'port': 21, 'protocol': 'tcp', 'service': 'ftp'}, {'port': 25, 'protocol': 'tcp', 'service': 'smtp'}, {'port': 53, 'protocol': 'tcp', 'service': 'domain'}, {'port': 80, 'protocol': 'tcp', 'service': 'http'}, {'port': 106, 'protocol': 'tcp', 'service': 'pop3pw'}, {'port': 110, 'protocol': 'tcp', 'service': 'pop3'}, {'port': 135, 'protocol': 'tcp', 'service': 'msrpc'}, {'port': 143, 'protocol': 'tcp', 'service': 'imap'}, {'port': 443, 'protocol': 'tcp', 'service': 'https'}, {'port': 465, 'protocol': 'tcp', 'service': 'smtps'}, {'port': 587, 'protocol': 'tcp', 'service': 'submission'}, {'port': 993, 'protocol': 'tcp', 'service': 'imaps'}, {'port': 995, 'protocol': 'tcp', 'service': 'pop3s'}, {'port': 2000, 'protocol': 'tcp', 'service': 'cisco-sccp'}, {'port': 3306, 'protocol': 'tcp', 'service': 'mysql'}, {'port': 5060, 'protocol': 'tcp', 'service': 'sip'}, {'port': 5555, 'protocol': 'tcp', 'service': 'freeciv'}, {'port': 8010, 'protocol': 'tcp', 'service': 'xmpp'}, {'port': 8443, 'protocol': 'tcp', 'service': 'https-alt'}]'''


ReportSampleWithCVE = '''
+----------------------------------------------------------+
|                Vulnerability Scan Report                 |
+----------------------------------------------------------+


[1] Vulnerabilities found for server-side software
        - Risk Level: 3 (High)

        Vulnerability Details:
        - CVE-2020-13664:
                - Risk Level: 
                - CVSS: 9.3
                - Summary: Arbitrary PHP code execution vulnerability in Drupal Core under certain circumstances. An attacker could trick an administrator into visiting a malicious site that could result in creating a carefully named directory on the file system. With this directory in place, an attacker could attempt to brute force a remote code execution vulnerability. Windows servers are most likely to be affected. This issue affects: Drupal Drupal Core 8.8.x versions prior to 8.8.8; 8.9.x versions prior to 8.9.1; 9.0.1 versions prior to 9.0.1.
                - Affected software: drupal 9

        - CVE-2020-13665:
                - Risk Level: 
                - CVSS: 7.5
                - Summary: Access bypass vulnerability in Drupal Core allows JSON:API when JSON:API is in read/write mode. Only sites that have the read_only set to FALSE under jsonapi.settings config are vulnerable. This issue affects: Drupal Drupal Core 8.8.x versions prior to 8.8.8; 8.9.x versions prior to 8.9.1; 9.0.x versions prior to 9.0.1.
                - Affected software: drupal 9

        - CVE-2022-25273:
                - Risk Level: 
                - CVSS: 7.5
                - Summary: Drupal core's form API has a vulnerability where certain contributed or custom modules' forms may be vulnerable to improper input validation. This could allow an attacker to inject disallowed values or overwrite data. Affected forms are uncommon, but in certain cases an attacker could alter critical or sensitive data.
                - Affected software: drupal 9

        - CVE-2022-25275:
                - Risk Level: 
                - CVSS: 7.5
                - Summary: In some situations, the Image module does not correctly check access to image files not stored in the standard public files directory when generating derivative images using the image styles system. Access to a non-public file is checked only if it is stored in the "private" file system. However, some contributed modules provide additional file systems, or schemes, which may lead to this vulnerability. This vulnerability is mitigated by the fact that it only applies when the site sets (Drupal 9) $config['image.settings']['allow_insecure_derivatives'] or (Drupal 7) $conf['image_allow_insecure_derivatives'] to TRUE. The recommended and default setting is FALSE, and Drupal core does not provide a way to change that in the admin UI. Some sites may require configuration changes following this security release. Review the release notes for your Drupal version if you have issues accessing files or image styles after updating.
                - Affected software: drupal 9

        - CVE-2022-39261:
                - Risk Level: 
                - CVSS: 7.5
                - Summary: Twig is a template language for PHP. Versions 1.x prior to 1.44.7, 2.x prior to 2.15.3, and 3.x prior to 3.4.3 encounter an issue when the filesystem loader loads templates for which the name is a user input. It is possible to use the `source` or `include` statement to read arbitrary files from outside the templates' directory when using a namespace like `@somewhere/../some.file`. In such a case, validation is bypassed. Versions 1.44.7, 2.15.3, and 3.4.3 contain a fix for validation of such template names. There are no known workarounds aside from upgrading.
                - Affected software: drupal 9


        - Description: We noticed known vulnerabilities in the target application. They are usually related to outdated systems and expose the affected applications to the risk of unauthorized access to confidential data and possibly denial of service attacks.
        - Recommendation: We recommend you to upgrade the affected software to the latest version in order to eliminate the risk of these vulnerabilities.


[2] Missing security header: Content-Security-Policy
        - Risk Level: 1 (Low)

        Vulnerability Details:
        - Evidence 1:
                - URL: https://www.aston.ac.uk/
                - Evidence: Response does not include the HTTP Content-Security-Policy security header or meta tag


        - Description: We noticed that the target application lacks the Content-Security-Policy (CSP) header in its HTTP responses. The CSP header is a security measure that instructs web browsers to enforce specific security rules, effectively preventing the exploitation of Cross-Site Scripting (XSS) vulnerabilities.
        - Recommendation: Configure the Content-Security-Header to be sent with each HTTP response in order to apply the specific policies needed by the application.


[3] Server software and technology found
        - Risk Level: 1 (Low)

        Vulnerability Details:
        - Evidence 1:
                - Software / Version: AppNexus
                - Category: Advertising

        - Evidence 2:
                - Software / Version: Amazon Cloudfront
                - Category: CDN

        - Evidence 3:
                - Software / Version: Crazy Egg
                - Category: Analytics

        - Evidence 4:
                - Software / Version: Facebook Pixel 2.9.153
                - Category: Analytics

        - Evidence 5:
                - Software / Version: Google Analytics
                - Category: Analytics

        - Evidence 6:
                - Software / Version: jQuery UI 1.13.2
                - Category: JavaScript libraries

        - Evidence 7:
                - Software / Version: Nginx
                - Category: Web servers, Reverse proxies

        - Evidence 8:
                - Software / Version: PHP
                - Category: Programming languages

        - Evidence 9:
                - Software / Version: Cloudflare
                - Category: CDN

        - Evidence 10:
                - Software / Version: Google Tag Manager
                - Category: Tag managers

        - Evidence 11:
                - Software / Version: Lodash 1.13.6
                - Category: JavaScript libraries

        - Evidence 12:
                - Software / Version: YouTube
                - Category: Video players

        - Evidence 13:
                - Software / Version: TikTok Pixel
                - Category: Analytics

        - Evidence 14:
                - Software / Version: Amazon Web Services
                - Category: PaaS

        - Evidence 15:
                - Software / Version: Linkedin Ads
                - Category: Advertising

        - Evidence 16:
                - Software / Version: Linkedin Insight Tag
                - Category: Analytics

        - Evidence 17:
                - Software / Version: cdnjs
                - Category: CDN

        - Evidence 18:
                - Software / Version: Bootstrap 3.4.1
                - Category: UI frameworks

        - Evidence 19:
                - Software / Version: LazySizes
                - Category: JavaScript libraries, Performance

        - Evidence 20:
                - Software / Version: core-js 3.20.3
                - Category: JavaScript libraries

        - Evidence 21:
                - Software / Version: jQuery 3.6.3
                - Category: JavaScript libraries

        - Evidence 22:
                - Software / Version: Select2
                - Category: JavaScript libraries

        - Evidence 23:
                - Software / Version: Swiper
                - Category: JavaScript libraries

        - Evidence 24:
                - Software / Version: UserWay
                - Category: Accessibility

        - Evidence 25:
                - Software / Version: Webpack
                - Category: Miscellaneous

        - Evidence 26:
                - Software / Version: Module Federation
                - Category: Miscellaneous

        - Evidence 27:
                - Software / Version: Drupal 9
                - Category: CMS

        - Evidence 28:
                - Software / Version: Hotjar
                - Category: Analytics

        - Evidence 29:
                - Software / Version: jsDelivr
                - Category: CDN

        - Evidence 30:
                - Software / Version: HSTS
                - Category: Security

        - Evidence 31:
                - Software / Version: Site Search 360
                - Category: Search engines


        - Description: We noticed that server software and technology details are exposed, potentially aiding attackers in tailoring specific exploits against identified systems and versions.
        - Recommendation: We recommend you to eliminate the information which permits the identification of software platform, technology, server and operating system: HTTP server headers, HTML meta information, etc.


[4] Robots.txt file found
        - Risk Level: 1 (Low)

        Vulnerability Details:
        - Evidence 1:
                - URL: https://www.aston.ac.uk/robots.txt


        - Description: We found the robots.txt on the target server. This file instructs web crawlers what URLs and endpoints of the web application they can visit and crawl. Website administrators often misuse this file while attempting to hide some web pages from the users.
        - Recommendation: We recommend you to manually review the entries from robots.txt and remove the ones which lead to sensitive locations in the website (ex. administration panels, configuration files, etc).


[5] Website is accessible.
[6] Nothing was found for client access policies.
[7] Nothing was found for absence of the security.txt file.
[8] Nothing was found for use of untrusted certificates.
[9] Nothing was found for enabled HTTP debug methods.
[10] Nothing was found for secure communication.
[11] Nothing was found for directory listing.
[12] Nothing was found for missing HTTP header - Strict-Transport-Security.
[13] Nothing was found for missing HTTP header -  X-Content-Type-Options.
[14] Nothing was found for missing HTTP header - Referrer.
[15] Nothing was found for domain too loose set for cookies.
[16] Nothing was found for HttpOnly flag of cookie.
[17] Nothing was found for Secure flag of cookie.
[18] Nothing was found for unsafe HTTP header Content Security Policy.

+----------------- TEST summary -----------------+
|                                                |
|  URL: https://www.aston.ac.uk/                 |
|  High Risk Findings: 1                         |
|  Medium Risk Findings: 0                       |
|  Low Risk Findings: 3                          |
|  Info Risk Findings: 14                        |
|  Start time: 2024-04-16 03:40:06               |
|  End time: 2024-04-16 03:40:30                 |
|                                                |
+------------------------------------------------+

'''


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
