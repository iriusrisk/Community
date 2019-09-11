<p align="center">
<img src="https://pbs.twimg.com/profile_banners/3092406029/1562586842/1080x360"/>
</p>

[IriusRisk Community Edition](https://community.iriusrisk.com) is a free version of IriusRisk that allows you to quickly model software security risks using a template based approach, and then manage those risks throughout the rest of the SDLC, including:
* Assigning a risk response: Accept, Mitigate or Expose
* Apply a security standard, such as OWASP ASVS to derive the security requirements in one step
* Automatically upload security controls as requirements to Jira
* Synchronise the current implementation state of the requirements with Jira and automatically adjust the associated risk rating

## An open Threat Model platform
All threat models created in IriusRisk can be published as Templates that are visible to other users of the platform.
If you have existing threat models in Microsoft Threat Modeller version 4 format, you can import the threats and countermeasures via the "Add Artifact" feature on the Architecture tab.  (Threat and Countermeasures are imported, but not dataflows).

## Getting Started
* Registration for the Community Edition is suspended until 27 August 2019.  Follow [@IriusRisk](https://twitter.com/IriusRisk) for updates
* Submit bugs and feature requests to github

## Publishing Templates
* One of the goals of the Community edition is to start sharing a common set of threat models for typical (or not) architectures.  If you've modeled a system that you believe would benefit the wider Community please publish it as a Template!  This will make it visible to other users of Community who will be able to import it into their own models. The submitted templates will go through a review process and if accepted, be published here on the github site in raw XML format so that non-community users can also take advantage of it.
* NOTE: When you publish a model, it will be removed from the Product table, you'll need to create a new product and import your template into it, to work on it again.

## Try our commercial edition for these extra features
* Manage more than 1 application. The solution has been tested with 4000+ applications.
* Directly modify questionnaires, risk patterns and rules.
* Access to expanded risk patterns libraries such as PCI DSS v3.2
* [Use our API](https://app.swaggerhub.com/api/continuumsecurity/IriusRisk/1) to embed IriusRisk as part of your SecDevOps pipeline and automatically import Cucumber, [BDD-Security](https://github.com/continuumsecurity/bdd-security) and OWASP ZAP scanning results
* Import vulnerabilities from numerous SAST and DAST tools via [ThreadFix](https://www.threadfix.it)
* See our [website for more details](https://www.iriusrisk.com/threat-modeling-tool/)
