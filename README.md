# IriusRisk Community Edition

<img src="https://www.continuumsecurity.net/wp-content/uploads/2016/11/iriuslogo-notagline.png" width="600"/>

[IriusRisk Community Edition](https://community.iriusrisk.com) is a free version of IriusRisk that allows you to quickly model software security risks using a template based approach, and then manage those risks throughout the rest of the SDLC, including:
* Assigning a risk response: Accept, Mitigate or Expose
* Apply a security standard, such as OWASP ASVS to derive the security requirements in one step
* Automatically upload security controls as requirements to Jira
* Synchronise the current implementation state of the requirements with Jira and automatically adjust the associated risk rating

## An open Threat Model platform
All threat models created in IriusRisk can be exported and imported in an open XML format.  Additionally, you can publish your threat models as Templates, so that other users of the platform can re-use them.
If you have existing threat models in Microsoft Threat Modeller version 4 format, you can import the threats and countermeasures via the "Add Artifact" feature on the Architecture tab.  (Support for the 2016 version is coming soon).

## Getting Started
* Read our [Getting Started Guide](https://continuumsecurity.atlassian.net/wiki/display/ITD/Getting+started)
* Sign up [on the community edition](https://community.iriusrisk.com)
* Submit bugs and feature requests to this github issues tracker

## Try our commercial edition for these extra features
* Manage more than 3 applications. The solution has been tested with 4000+ applications.
* Directly modify questionnaires, risk patterns and rules.
* [Use our API](https://app.swaggerhub.com/api/continuumsecurity/IriusRisk/1) to embed IriusRisk as part of your SecDevOps pipeline and automatically import Cucumber, [BDD-Security](https://github.com/continuumsecurity/bdd-security) and OWASP ZAP scanning results
* Import vulnerabilities from numerous SAST and DAST tools via [ThreadFix](https://www.threadfix.it)
