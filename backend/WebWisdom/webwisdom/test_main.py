from fastapi.testclient import TestClient
from .main import app
from .database.database import Base
from .routers.auth import get_db


from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import pytest


# in memory DB that is deleted when test is done
SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


# when running pytest -v -s add the s flag to see the print statements of tests that pass

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)



# Unit testing

# Unit test imports
from .app.logic import data_parse
from .app.logic import score_calculator

def test_parse_risk_level_in_from_str_to_int_headers():
    assert data_parse.parse_risk_level_in_from_str_to_int_headers(
        "2,2,4,1,10,3") == {'total_risk_headers': [2, 2, 1, 1, 3]}


def test_parse_risk_level_in_from_str_to_int_files():
    assert data_parse.parse_risk_level_in_from_str_to_int_files(
        "2,2,4,1,10,3") == {'total_risk_files': [2, 2, 1, 1, 3]}


def test_parse_risk_level_in_from_str_to_int_cookies():
    assert data_parse.parse_risk_level_in_from_str_to_int_cookies(
        "2,2,4,1,10,3") == {'total_risk_cookies': [2, 2, 1, 1, 3]}


def test_parse_vulnerability_report_for_technologies():
    result = data_parse.parse_vulnerability_report_for_technologies(
        ReportSample)
    expectedResult = [{'software_name': 'YouTube', 'software_version': 'Unknown', 'category': 'Video players'}, {'software_name': 'Google Ads', 'software_version': 'Unknown', 'category': 'Advertising'}, {'software_name': 'HTTP/3', 'software_version': 'Unknown', 'category': 'Miscellaneous'}, {'software_name': 'Google Ads Conversion Tracking', 'software_version': 'Unknown',
                                                                                                                                                                                                                                                                                                     'category': 'Analytics'}, {'software_name': 'Webpack', 'software_version': 'Unknown', 'category': 'Miscellaneous'}, {'software_name': 'Module Federation', 'software_version': 'Unknown', 'category': 'Miscellaneous'}, {'software_name': 'reCAPTCHA', 'software_version': 'Unknown', 'category': 'Security'}, {'software_name': 'HSTS', 'software_version': 'Unknown', 'category': 'Security'}]
    assert result == expectedResult


def test_parse_vulnerability_report_for_headers():
    result = data_parse.parse_vulnerability_report_for_headers(ReportSample)
    expectedResult = [{'data': [{'Header': 'Missing Security Header: Referrer-Policy', 'RiskLevel': '1 (Low)', 'Description': "We noticed that the target application's server responses lack the <code>Referrer-Policy</code> HTTP header, which controls how much referrer information the browser will send with each request originated from the current web application.", 'Recommendation': 'The Referrer-Policy header should be configured on the server side to avoid user tracking and inadvertent information leakage. The value `no-referrer` of this header instructs the browser to omit the Referer header entirely.', 'Evidence': {'URL': 'https://www.youtube.com/', 'EvidenceDetail': "Response headers do not include the Referrer-Policy HTTP security header as well as the <meta> tag with name 'referrer' is not present in the response."}}, {'Header': 'Missing Security Header: Content-Security-Policy', 'RiskLevel': '1 (Low)', 'Description': 'We noticed that the target application lacks the Content-Security-Policy (CSP) header in its HTTP responses. The CSP header is a security measure that instructs web browsers to enforce specific security rules, effectively preventing the exploitation of Cross-Site Scripting (XSS) vulnerabilities.', 'Recommendation': 'Configure the Content-Security-Header to be sent with each HTTP response in order to apply the specific policies needed by the application.', 'Evidence': {'URL': 'https://www.youtube.com/', 'EvidenceDetail': 'Response does not include the HTTP Content-Security-Policy security header or meta tag'}}, {'Header': 'Missing Security Header: Strict-Transport-Security', 'RiskLevel': '1 (Low)', 'Description': 'We noticed that the target application lacks the HTTP Strict-Transport-Security header in its responses. This security header is crucial as it instructs browsers to only establish secure (HTTPS) connections with the web server and reject any HTTP connections.',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       'Recommendation': 'The Strict-Transport-Security HTTP header should be sent with each HTTPS response. The syntax is as follows: `Strict-Transport-Security: max-age=&lt;seconds>[; includeSubDomains]` The parameter `max-age` gives the time frame for requirement of HTTPS in seconds and should be chosen quite high, e.g. several months. A value below 7776000 is considered as too low by this scanner check. The flag `includeSubDomains` defines that the policy applies also for sub domains of the sender of the response.', 'Evidence': {'URL': 'https://www.youtube.com/s/desktop/f45068c8/img', 'EvidenceDetail': 'Response headers do not include the HTTP Strict-Transport-Security header'}}, {'Header': 'Unsafe Security Header: Content-Security-Policy', 'RiskLevel': '1 (Low)', 'Description': 'We noticed that the Content-Security-Policy (CSP) header configured for the web application includes unsafe directives. The CSP header activates a protection mechanism implemented in web browsers which prevents exploitation of Cross-Site Scripting vulnerabilities (XSS) by restricting the sources from which content can be loaded or executed.', 'Recommendation': 'Remove the unsafe values from the directives, adopt nonces or hashes for safer inclusion of inline scripts if they are needed, and explicitly define the sources from which scripts, styles, images or other resources can be loaded.', 'Evidence': {'URL': 'https://www.youtube.com/t', 'EvidenceDetail': "Response headers include the HTTP Content-Security-Policy security header with the following security issues: `report-uri: report-uri is deprecated in CSP3. Please use the report-to directive instead.` `default-src: The default-src directive should be set as a fall-back when other restrictions have not been specified. ` `script-src: ''unsafe-inline'' allows the execution of unsafe in-page scripts and event handlers.` `script-src: Nonces should only use the base64 charset.`"}}]}, {'total_risk_headers': [1, 1, 1, 1]}]
    assert result == expectedResult


def test_parse_vulnerability_report_for_txt_files():
    result = data_parse.parse_vulnerability_report_for_txt_files(ReportSample)
    expectedResult = [{'data': [{'File': 'Robots.txt', 'RiskLevel': '1 (Low)', 'Description': 'We found the robots.txt on the target server. This file instructs web crawlers what URLs and endpoints of the web application they can visit and crawl. Website administrators often misuse this file while attempting to hide some web pages from the users.',
                                 'Recommendation': 'We recommend you to manually review the entries from robots.txt and remove the ones which lead to sensitive locations in the website (ex. administration panels, configuration files, etc).'}]}, {'total_risk_files': [1]}]
    assert result == expectedResult


def test_parse_vulnerability_report_for_insecure_cookie():
    result = data_parse.parse_vulnerability_report_for_insecure_cookie(
        ReportSample)
    expectedResult = [{'data': [{'IssueDetail': 'setting: domain too loose', 'RiskLevel': '2 (Medium)', 'Description': 'We found that the target application sets cookies with a domain scope that is too broad. Specifically, cookies intended for use within a particular application are configured in such a way that they can be accessed by multiple subdomains of the same primary domain.',
                                 'Recommendation': 'The `Domain` attribute should be set to the origin host to limit the scope to that particular server. For example if the application resides on server app.mysite.com, then it should be set to `Domain=app.mysite.com`', 'Evidence': {'URL': 'https://www.youtube.com/', 'CookieName': 'YSC', 'EvidenceDetail': 'Set-Cookie: .youtube.com'}}]}, {'total_risk_cookies': [2]}]
    assert result == expectedResult


def test_parse_server_side_vulnerabilities():
    result = data_parse.parse_server_side_vulnerabilities(SeaViewReportSample)
    expectedResult = {'title': 'Vulnerabilities found for server-side software', 'total_risk_server_side_vulnerabilities': [4, 4, 4, 4, 4, 3, 3, 3, 3], 'cve_list': [{'id': 'CVE-2020-13664', 'CVSS': 9.3, 'summary': 'Arbitrary PHP code execution vulnerability in Drupal Core under certain circumstances. An attacker could trick an administrator into visiting a malicious site that could result in creating a carefully named directory on the file system. With this directory in place, an attacker could attempt to brute force a remote code execution vulnerability. Windows servers are most likely to be affected. This issue affects: Drupal Drupal Core 8.8.x versions prior to 8.8.8; 8.9.x versions prior to 8.9.1; 9.0.1 versions prior to 9.0.1.', 'affected_software': 'drupal 9'}, {'id': 'CVE-2020-13665', 'CVSS': 7.5, 'summary': 'Access bypass vulnerability in Drupal Core allows JSON:API when JSON:API is in read/write mode. Only sites that have the read_only set to FALSE under jsonapi.settings config are vulnerable. This issue affects: Drupal Drupal Core 8.8.x versions prior to 8.8.8; 8.9.x versions prior to 8.9.1; 9.0.x versions prior to 9.0.1.', 'affected_software': 'drupal 9'}, {'id': 'CVE-2022-25273', 'CVSS': 7.5, 'summary': "Drupal core's form API has a vulnerability where certain contributed or custom modules' forms may be vulnerable to improper input validation. This could allow an attacker to inject disallowed values or overwrite data. Affected forms are uncommon, but in certain cases an attacker could alter critical or sensitive data.", 'affected_software': 'drupal 9'}, {'id': 'CVE-2022-25275', 'CVSS': 7.5, 'summary': 'In some situations, the Image module does not correctly check access to image files not stored in the standard public files directory when generating derivative images using the image styles system. Access to a non-public file is checked only if it is stored in the "private" file system. However, some contributed modules provide additional file systems, or schemes, which may lead to this vulnerability. This vulnerability is mitigated by the fact that it only applies when the site sets (Drupal 9) $config[\'image.settings\'][\'allow_insecure_derivatives\'] or (Drupal 7) $conf[\'image_allow_insecure_derivatives\'] to TRUE. The recommended and default setting is FALSE, and Drupal core does not provide a way to change that in the admin UI. Some sites may require configuration changes following this security release. Review the release notes for your Drupal version if you have issues accessing files or image styles after updating.', 'affected_software': 'drupal 9'}, {
        'id': 'CVE-2022-39261', 'CVSS': 7.5, 'summary': "Twig is a template language for PHP. Versions 1.x prior to 1.44.7, 2.x prior to 2.15.3, and 3.x prior to 3.4.3 encounter an issue when the filesystem loader loads templates for which the name is a user input. It is possible to use the `source` or `include` statement to read arbitrary files from outside the templates' directory when using a namespace like `@somewhere/../some.file`. In such a case, validation is bypassed. Versions 1.44.7, 2.15.3, and 3.4.3 contain a fix for validation of such template names. There are no known workarounds aside from upgrading.", 'affected_software': 'drupal 9'}, {'id': 'CVE-2023-2745', 'CVSS': 5.4, 'summary': 'WordPress Core is vulnerable to Directory Traversal in versions up to, and including, 6.2, via the ‘wp_lang’ parameter. This allows unauthenticated attackers to access and load arbitrary translation files. In cases where an attacker is able to upload a crafted translation file onto the site, such as via an upload form, this could be also used to perform a Cross-Site Scripting attack.', 'affected_software': 'wordpress 6.2'}, {'id': 'CVE-2023-38000', 'CVSS': 5.4, 'summary': 'Auth. Stored (contributor+) Cross-Site Scripting (XSS) vulnerability in WordPress core 6.3 through 6.3.1, from 6.2 through 6.2.2, from 6.1 through 6.1.3, from 6.0 through 6.0.5, from 5.9 through 5.9.7 and Gutenberg plugin <= 16.8.0 versions.', 'affected_software': 'wordpress 6.2'}, {'id': 'CVE-2023-5561', 'CVSS': 5.3, 'summary': 'WordPress does not properly restrict which user fields are searchable via the REST API, allowing unauthenticated attackers to discern the email addresses of users who have published public posts on an affected website via an Oracle style attack', 'affected_software': 'wordpress 6.2'}, {'id': 'CVE-2023-39999', 'CVSS': 4.3, 'summary': 'Exposure of Sensitive Information to an Unauthorized Actor in WordPress from 6.3 through 6.3.1, from 6.2 through 6.2.2, from 6.1 through 6.13, from 6.0 through 6.0.5, from 5.9 through 5.9.7, from 5.8 through 5.8.7, from 5.7 through 5.7.9, from 5.6 through 5.6.11, from 5.5 through 5.5.12, from 5.4 through 5.4.13, from 5.3 through 5.3.15, from 5.2 through 5.2.18, from 5.1 through 5.1.16, from 5.0 through 5.0.19, from 4.9 through 4.9.23, from 4.8 through 4.8.22, from 4.7 through 4.7.26, from 4.6 through 4.6.26, from 4.5 through 4.5.29, from 4.4 through 4.4.30, from 4.3 through 4.3.31, from 4.2 through 4.2.35, from 4.1 through 4.1.38.', 'affected_software': 'wordpress 6.2'}]}
    assert result == expectedResult

def test_find_unique_dictionary():
    data = [{"x":1},{"y":3}]
    result = score_calculator.find_unique_list(data,"x")
    assert result == 1

def test_find_unique_list():

    data = [{"x":["s","y","x"]}]
    result = score_calculator.find_unique_list(data,"x")
    assert result == ['s', 'y', "x"]

def test_calculate_security_score_from_list_above_zero():
    result = score_calculator.calculate_security_score_from_list([3,3,3,3,3,3,2,2,5,5,5,5])
    assert result["security_score"] >= 0
    
    
def test_calculate_security_score_from_list_below_ten():
    result = score_calculator.calculate_security_score_from_list([0])
    assert result["security_score"] <= 10
    
    
# Integration testing

def test_create_user():
    create_user = client.post(
        "/auth/register",
        json={"username": "test@test.com",
              "password": "123Rock123???"},
    )
    jwt_token = create_user.cookies.get("jwt_token")
    client.cookies.set(name="jwt_token", value=jwt_token)

    assert create_user.status_code == 200


def test_create_penetration_test_with_user_jwt():

    response = client.get("/api/test-parse")

    response_data = response.content.decode('utf-8')

    assert "testurl.com" in response_data


def test_retrieve_penetration_test_for_user():
    client.get("/api/test-parse")
    response = client.get("/auth/get-all-results")
    response_data = response.content.decode('utf-8')

    assert '"id":1' in response_data and '"id":2' in response_data
    assert '"user_id":1' in response_data
    assert '"user_id":2' not in response_data


# System testing (test the pentest of a site)

def test_fake_site():
    result = client.post("/api/run-tests",
                json={
                    "url": "https://example.coco/"
                })

    result.content.decode("utf-8")
    assert result.content.decode("utf-8") == '{"detail":"Site is down or does not exist please check the url and that the site is accessible and running!"}'


def test_real_pentest_of_a_user():
    result = client.post("/api/run-tests",
                json={
                    "url": "https://yousefqasim.uk/"
                })

    data = result.content.decode("utf-8")
    assert "yousefqasim.uk" in data
    assert "technologies" in data
















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
