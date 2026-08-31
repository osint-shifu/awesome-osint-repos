<a id="top"></a>

<div align="center">
  <h1>Agentic AI OSINT</h1>
  <p>Open-source skills, plugins, MCP servers, and AI-agent integrations for investigative work.</p>
  <p>
    <img alt="Total projects: 135" src="https://img.shields.io/badge/total_projects-135-bf8700?style=flat-square">
    <img alt="MCP integrations: 64" src="https://img.shields.io/badge/MCP_integrations-64-0969da?style=flat-square">
    <img alt="Skill integrations: 55" src="https://img.shields.io/badge/skill_integrations-55-8250df?style=flat-square">
    <img alt="Last update: 2026-08-31" src="https://img.shields.io/badge/last_update-2026--08--31-1f883d?style=flat-square">
  </p>
  <p><a href="README.md">Awesome OSINT Repositories</a> · <a href="EMERGING.md">Emerging Projects</a> · <strong><a href="AGENTIC.md">Agentic AI OSINT</a></strong> · <a href="TIMELINE.md">Catalogue Timeline</a> · <a href="osint-repositories.csv">Repository Database CSV</a></p>
</div>

## About this catalogue

This view contains implementation-bearing repositories that expose investigative workflows or data access to AI agents. Membership is stored in `Source Files`, while the same single main category used by the primary catalogue determines the sections below.

`Target Input` describes the concrete data accepted by a tool. `AI Agent` records the documented agent runtime or integration surface, such as Claude Code, an Agent Skills-compatible client, or any MCP-compatible agent.

> [!IMPORTANT]
> Only public source-code implementations are included. Prompt lists, link collections, closed services, courses, articles, and repository stubs are excluded.

> [!NOTE]
> Low or zero star counts do not disqualify a young project with a meaningful implementation.

> <img src=".github/assets/new-dot.svg" width="6" height="6" alt=""> marks projects added to the catalogue within the last 14 days.

<a id="contents"></a>

## Contents

- [Identity](#identity) <sup>5 projects</sup>
- [Social Media](#social-media) <sup>12 projects</sup>
- [Infrastructure](#infrastructure) <sup>25 projects</sup>
- [Web](#web) <sup>34 projects</sup>
- [Dark Web](#dark-web) <sup>3 projects</sup>
- [Threat Intelligence](#threat-intelligence) <sup>11 projects</sup>
- [Documents & Records](#documents-records) <sup>22 projects</sup>
- [Geolocation](#geolocation) <sup>6 projects</sup>
- [Investigation](#investigation) <sup>17 projects</sup>
- [Catalogue timeline](TIMELINE.md)
- [Complete repository database (CSV)](osint-repositories.csv) <sup>487 unique repositories</sup>

---

<a id="identity"></a>

## 👤 Identity <sup>5 projects</sup>

Tools centered on people, names, contact identifiers, and identity resolution.

| Project | Target Input | AI Agent | Description | Created | Last Update | Stars |
|:---|:---|:---|:---|:---:|:---:|---:|
| [OSINT Skill](https://github.com/smixs/osint-skill) | Name | Multiple / configurable agents | Runs phased people research with source grading, correlation, and report generation. | 2026-03-10 | 2026-03-10 | ⭐ 117 |
| [OSINT AI Agent](https://github.com/sumba101/OSINT-AI-Agent) | Name; Username; Email | Claude (agent unspecified) | Orchestrates Holehe, Sherlock, and GHunt for person-focused investigations. | 2026-01-11 | 2026-01-11 | ⭐ 10 |
| <img src=".github/assets/new-dot.svg" width="6" height="6" alt=""> [Clearfront](https://github.com/scottmartinanderson/clearfront) | Name; Username; Email | Claude Code | Agent that maps a digital footprint across public data sources and reports the collected identifiers. | 2026-07-08 | 2026-08-19 | ⭐ 8 |
| [Deep Research Ladder](https://github.com/hint-shu/deep-research) | Name; URL | Claude Code | Scales from fact checks to long-form research and OSINT entity reconnaissance. | 2026-04-17 | 2026-04-29 | ⭐ 3 |
| [Email Finder Batch](https://github.com/yoitsyoung/email-finder-batch) | Email | Claude Code | Coordinates public-source email discovery, pattern generation, and verification agents. | 2026-03-22 | 2026-03-22 | ⭐ 2 |

<p align="right"><a href="#contents">Back to contents ↑</a></p>

<a id="social-media"></a>

## 💬 Social Media <sup>12 projects</sup>

Tools for discovering and analyzing public accounts and content on social platforms.

| Project | Target Input | AI Agent | Description | Created | Last Update | Stars |
|:---|:---|:---|:---|:---:|:---:|---:|
| [Agent Reach](https://github.com/Panniantong/Agent-Reach) | Username; URL | Multiple / configurable agents | Gives agents collection workflows for public content across multiple social and developer platforms. | 2026-02-24 | 2026-08-25 | ⭐ 76,945 |
| [last30days](https://github.com/mvanhorn/last30days-skill) | Username; URL | Multiple / configurable agents | Researches recent discussion across social platforms, communities, prediction markets, and the web. | 2026-01-23 | 2026-08-26 | ⭐ 60,746 |
| [MCP Maigret](https://github.com/w0h1v/mcp-maigret) | Username | Any MCP-compatible agent | Exposes Maigret username searches and public account discovery through MCP. | 2024-12-13 | 2026-01-27 | ⭐ 259 |
| [xint](https://github.com/0xNyk/xint) | Username | Multiple / configurable agents | Searches, monitors, and exports public X data for agent-assisted investigations. | 2026-02-14 | 2026-08-28 | ⭐ 248 |
| [Reddit Research MCP](https://github.com/dialog-tools/reddit-research-mcp) | Username; URL | Any MCP-compatible agent | Supports structured Reddit discovery, thread collection, and community research. | 2025-08-12 | 2026-08-14 | ⭐ 234 |
| [YouTube Research MCP](https://github.com/coyaSONG/youtube-mcp-server) | Username; Video | Any MCP-compatible agent | Exposes YouTube videos, channels, search results, comments, and transcripts through MCP. | 2025-03-31 | 2026-07-17 | ⭐ 19 |
| [Telegram MCP TDLib](https://github.com/tolboy/telegram-mcp-tdlib) | Username | Any MCP-compatible agent | Exposes Telegram searches, chats, messages, and public content to MCP clients through TDLib. | 2026-07-04 | 2026-08-22 | ⭐ 5 |
| [OSINT Social](https://github.com/guleguleguru/osint-social) | Username | OpenClaw | Wraps broad username discovery with additional coverage for major Chinese platforms. | 2026-02-28 | 2026-02-28 | ⭐ 1 |
| [LinkedIn Recon Skill](https://github.com/Kewanvk/linkedin-recon-skill) | Name; Organization Name | Claude Code; OpenAI Codex | Maps public hiring networks and organizational relationships from LinkedIn evidence. | 2026-05-08 | 2026-05-25 | ⭐ 0 |
| [Sherlock Skill](https://github.com/ImL1s/sherlock-skill) | Username | Multiple / configurable agents | Wraps Sherlock username searches with a portable skill and structured dossier output. | 2026-04-22 | 2026-04-22 | ⭐ 0 |
| [Chinese OSINT Skills](https://github.com/zomin/chinese-osint-skills) | Username | Multiple / configurable agents | Supplies Chinese-platform research methods and scripts for cross-platform identity pivots. | 2026-04-30 | 2026-04-30 | ⭐ 0 |
| [X Archive RAG](https://github.com/mameshivaa/x-archive-rag) | Username | Generic AI agent | Indexes exported X data for local semantic search and retrieval-augmented analysis. | 2026-05-26 | 2026-06-18 | ⭐ 0 |

<p align="right"><a href="#contents">Back to contents ↑</a></p>

<a id="infrastructure"></a>

## 🌐 Infrastructure <sup>25 projects</sup>

Tools for domains, IP addresses, networks, ASNs, and related internet infrastructure.

| Project | Target Input | AI Agent | Description | Created | Last Update | Stars |
|:---|:---|:---|:---|:---:|:---:|---:|
| [HexStrike AI](https://github.com/0x4m4/hexstrike-ai) | Domain; IP Address; URL | Any MCP-compatible agent | Connects agents to a large collection of security and reconnaissance tools. | 2025-07-10 | 2026-08-03 | ⭐ 11,462 |
| [Claude Bug Bounty](https://github.com/Awarexone/Agentic-Bug-Hunter) | Domain; URL | Claude Code | Organizes authorized bug-bounty reconnaissance, testing, validation, and reporting. | 2026-03-08 | 2026-08-25 | ⭐ 4,633 |
| [Claude BugHunter](https://github.com/elementalsouls/Claude-BugHunter) | Domain; URL | Claude Code | Adds structured web reconnaissance and vulnerability-hunting methodology. | 2026-05-05 | 2026-08-31 | ⭐ 3,924 |
| [VulnClaw](https://github.com/Netw0rkNoob/VulnClaw) | Domain; IP Address; URL | Multiple / configurable agents | Orchestrates information gathering, vulnerability analysis, exploitation, and reporting. | 2026-04-18 | 2026-08-10 | ⭐ 3,050 |
| [Claude Red](https://github.com/SnailSploit/Claude-Red) | Domain; IP Address; URL | Claude Code | Provides red-team and security research playbooks for Claude-based workflows. | 2026-03-04 | 2026-08-29 | ⭐ 3,003 |
| [redamon](https://github.com/samugit83/redamon) | Domain; IP Address; URL | Multiple / configurable agents | Coordinates AI-assisted reconnaissance, validation, remediation, and reporting workflows for authorized security testing. | 2025-12-29 | 2026-08-29 | ⭐ 2,370 |
| [Claude OSINT](https://github.com/elementalsouls/Claude-OSINT) | Domain; URL | Claude Code | Adds structured external reconnaissance methods, dorks, validators, and reporting guidance. | 2026-04-26 | 2026-08-30 | ⭐ 2,357 |
| [Pentest AI Agents](https://github.com/0xSteph/pentest-ai-agents) | Domain; IP Address; URL | Claude Code | Supplies specialized subagents for recon analysis, exploit research, detection, and reporting. | 2026-03-28 | 2026-08-16 | ⭐ 2,180 |
| [CyberStrike](https://github.com/CyberStrikeus/CyberStrike) | Domain; IP Address; URL | Multiple / configurable agents | Runs agent-assisted offensive security with recon, testing, and evidence workflows. | 2026-02-14 | 2026-08-30 | ⭐ 2,160 |
| [Hack Skills](https://github.com/yaklang/hack-skills) | Domain; IP Address; URL | Any Agent Skills-compatible agent | Covers reconnaissance, web and network security, forensics, reversing, and authorized research. | 2026-04-07 | 2026-06-16 | ⭐ 1,941 |
| [Pentest AI](https://github.com/0xSteph/pentest-ai) | Domain; IP Address; URL | Multiple / configurable agents | Exposes security tools, specialist agents, and deterministic probes through CLI and MCP. | 2026-04-04 | 2026-08-17 | ⭐ 1,637 |
| [Recon Skills](https://github.com/uphiago/recon-skills) | Domain; IP Address; URL | Any Agent Skills-compatible agent | Provides field-oriented recon, dorking, secret discovery, asset mapping, and testing playbooks. | 2026-06-24 | 2026-08-24 | ⭐ 1,214 |
| [Transilience Community Tools](https://github.com/transilienceai/communitytools) | Domain; IP Address; URL | Claude Code | Covers security reconnaissance, bug bounty, AI threat testing, validation, and reporting. | 2025-11-21 | 2026-07-29 | ⭐ 497 |
| [TORCH](https://github.com/Encod3d-Sec/TORCH) | Domain; IP Address; URL | Claude Code | Provides Claude Code with reconnaissance and authorized security-testing workflows, a searchable technique library, persistent engagement state, and MCP retrieval. | 2026-07-14 | 2026-08-28 | ⭐ 283 |
| [ThreatSwarm](https://github.com/mukul975/Threatswarm) | Domain; IP Address; URL | Claude Code | Coordinates scope-aware agents across recon, exploitation, DFIR, and final reporting. | 2026-04-29 | 2026-04-29 | ⭐ 76 |
| [OSINT AI](https://github.com/dkyazzentwatwa/osint-ai) | Name; Organization Name; Domain | Generic AI agent | Provides guided people, domain, organization, breach, and evidence-analysis workflows. | 2026-02-27 | 2026-03-07 | ⭐ 52 |
| [MCP dnstwist](https://github.com/w0h1v/mcp-dnstwist) | Domain | Any MCP-compatible agent | Exposes look-alike domain discovery for phishing and impersonation investigations. | 2024-12-19 | 2025-03-03 | ⭐ 51 |
| [OSINT MCP Server](https://github.com/badchars/osint-mcp-server) | Domain; IP Address; URL | Any MCP-compatible agent | Correlates infrastructure and threat data from Shodan, Censys, DNS, BGP, archives, and more. | 2026-03-17 | 2026-03-17 | ⭐ 48 |
| [Claude Code Pentest](https://github.com/Orizon-eu/claude-code-pentest) | Domain; IP Address; URL | Claude Code | Automates the authorized pentest lifecycle from initial recon to exploit-chain reports. | 2026-03-11 | 2026-03-11 | ⭐ 24 |
| [Shodan MCP by Vorota](https://github.com/Vorota-ai/shodan-mcp) | Domain; IP Address | Any MCP-compatible agent | Adds passive asset discovery, DNS analysis, and vulnerability intelligence from Shodan. | 2026-02-12 | 2026-02-12 | ⭐ 22 |
| [Recon](https://github.com/g-baskin/recon) | Organization Name; Domain; URL | Claude Code | Performs competitive intelligence across products, infrastructure, APIs, and communities. | 2026-02-25 | 2026-04-04 | ⭐ 6 |
| [Outrider Recon](https://github.com/Ap6pack/outrider-recon) | Domain; URL | Claude Code | Runs evidence-backed external reconnaissance with policy controls and optional MCP enrichment. | 2026-04-29 | 2026-07-15 | ⭐ 4 |
| [Offensive Recon](https://github.com/mahuttha/offensive-recon) | Domain; IP Address; URL | Claude Code | Packages multi-phase reconnaissance skills and agents around common security tools. | 2026-03-01 | 2026-03-01 | ⭐ 4 |
| [LeakIX MCP](https://github.com/LeakIX/leakix-mcp) | Domain; IP Address; URL | Any MCP-compatible agent | Exposes LeakIX searches for internet services, leaks, domains, and IP addresses through MCP. | 2026-01-27 | 2026-08-24 | ⭐ 2 |
| [Bounty Recon Pro](https://github.com/synicalkid/bounty-recon-pro) | Domain; URL | Claude Code | Runs scoped passive OSINT and active bug-bounty recon with evidence-oriented reports. | 2026-07-11 | 2026-07-11 | ⭐ 0 |

<p align="right"><a href="#contents">Back to contents ↑</a></p>

<a id="web"></a>

## 🔗 Web <sup>34 projects</sup>

Tools that collect, search, analyze, crawl, or preserve public web content.

| Project | Target Input | AI Agent | Description | Created | Last Update | Stars |
|:---|:---|:---|:---|:---:|:---:|---:|
| [Browser Use](https://github.com/browser-use/browser-use) | URL | Multiple / configurable agents | Lets AI agents navigate websites, interact with pages, and extract information. | 2024-10-31 | 2026-08-31 | ⭐ 111,811 |
| <img src=".github/assets/new-dot.svg" width="6" height="6" alt=""> [DeerFlow](https://github.com/bytedance/deer-flow) | URL | Multiple / configurable agents | Orchestrates deep research with subagents, memory, optional web search, tools, and sandboxing. | 2025-05-07 | 2026-08-31 | ⭐ 81,168 |
| [Scrapling](https://github.com/D4Vinci/Scrapling) | URL | Any Agent Skills-compatible agent; Any MCP-compatible agent | Provides adaptive web scraping, crawling, browser automation, and structured extraction. | 2024-10-13 | 2026-08-25 | ⭐ 77,457 |
| [TrendRadar](https://github.com/sansan0/TrendRadar) | URL | Any MCP-compatible agent | Monitors news and RSS sources, tracks trends, stores history, and exposes MCP access. | 2025-04-28 | 2026-07-17 | ⭐ 61,960 |
| <img src=".github/assets/new-dot.svg" width="6" height="6" alt=""> [OpenHuman](https://github.com/tinyhumansai/openhuman) | URL; Document | Multiple / configurable agents | Builds local context and runs deep research across personal data and the web with browser tooling and durable agent workflows. | 2026-02-18 | 2026-08-30 | ⭐ 39,130 |
| [Vane](https://github.com/ItzCrazyKns/Vane) | URL | Multiple / configurable agents | Provides a self-hosted research interface that answers questions with linked sources. | 2024-04-09 | 2026-04-11 | ⭐ 36,557 |
| [GPT Researcher](https://github.com/assafelovic/gpt-researcher) | URL | Multiple / configurable agents | Runs multi-agent web research and produces source-grounded reports with citations. | 2023-05-12 | 2026-08-23 | ⭐ 29,214 |
| [Stagehand](https://github.com/browserbase/stagehand) | URL | Multiple / configurable agents | Provides an SDK for agent-driven browser automation and page extraction. | 2024-03-24 | 2026-08-30 | ⭐ 24,108 |
| [deep-research](https://github.com/dzhng/deep-research) | URL | Multiple / configurable agents | Runs iterative web searches, evaluates findings, and builds source-grounded research answers. | 2025-02-04 | 2026-04-11 | ⭐ 19,619 |
| <img src=".github/assets/new-dot.svg" width="6" height="6" alt=""> [OpenJarvis](https://github.com/open-jarvis/OpenJarvis) | URL; Document | Multiple / configurable agents | Runs local-first deep research across the web and indexed documents with citations and scheduled monitoring. | 2026-02-15 | 2026-08-31 | ⭐ 9,236 |
| [Firecrawl MCP Server](https://github.com/firecrawl/firecrawl-mcp-server) | URL | Any MCP-compatible agent | Gives agents web search, crawling, scraping, extraction, and structured research tools. | 2024-12-06 | 2026-08-31 | ⭐ 7,356 |
| [Apify MCP Server](https://github.com/apify/apify-mcp-server) | URL | Any MCP-compatible agent | Makes Apify Actors and public web data collection available to compatible agents. | 2025-01-02 | 2026-08-26 | ⭐ 5,469 |
| [Exa MCP Server](https://github.com/exa-labs/exa-mcp-server) | URL | Any MCP-compatible agent | Provides semantic web search, content retrieval, and research discovery through Exa. | 2024-11-27 | 2026-08-21 | ⭐ 4,947 |
| [Deep Research](https://github.com/u14app/deep-research) | URL | Multiple / configurable agents | Runs iterative web research and synthesis with configurable models and MCP access. | 2025-02-22 | 2026-06-18 | ⭐ 4,684 |
| [Bright Data MCP](https://github.com/brightdata/brightdata-mcp) | URL | Any MCP-compatible agent | Connects agents to search, browsing, scraping, and public web datasets. | 2025-04-15 | 2026-08-12 | ⭐ 2,618 |
| [Tavily MCP](https://github.com/tavily-ai/tavily-mcp) | URL | Any MCP-compatible agent | Exposes search, extraction, crawling, mapping, and research functions from Tavily. | 2025-01-27 | 2026-08-20 | ⭐ 2,363 |
| [Brave Search MCP Server](https://github.com/brave/brave-search-mcp-server) | URL | Any MCP-compatible agent | Adds Brave web, news, image, video, and local search to MCP clients. | 2025-06-12 | 2026-08-20 | ⭐ 1,409 |
| [NotebookLM Skill](https://github.com/claude-world/notebooklm-skill) | URL | Claude Code | Uses NotebookLM for source-grounded research, synthesis, and content preparation. | 2026-03-13 | 2026-07-18 | ⭐ 444 |
| [De-Anthropocentric Research Engine](https://github.com/yogsoth-ai/de-anthropocentric-research-engine) | URL | Multiple / configurable agents | Organizes autonomous research into composable campaigns, strategies, tactics, and procedures. | 2026-02-10 | 2026-08-25 | ⭐ 407 |
| [Kindly Web Search MCP](https://github.com/Shelpuk-AI-Technology-Consulting/kindly-web-search-mcp-server) | URL | Any MCP-compatible agent | Aggregates web search, extraction, crawling, and browser automation for many clients. | 2026-01-02 | 2026-08-31 | ⭐ 380 |
| [MCP Omnisearch](https://github.com/spences10/mcp-omnisearch) | URL | Any MCP-compatible agent | Combines multiple search, AI search, and content-processing providers behind MCP. | 2025-03-08 | 2026-08-29 | ⭐ 347 |
| [Google Research MCP](https://github.com/mixelpixx/Nimrod) | URL | Any MCP-compatible agent | Uses Google Search and browser automation for multi-step cited research. | 2024-12-19 | 2026-08-14 | ⭐ 256 |
| [Octagon MCP Server](https://github.com/OctagonAI/octagon-mcp-server) | URL | Any MCP-compatible agent | Provides public company, market, investor, private-market, and crypto research data. | 2025-03-12 | 2026-07-09 | ⭐ 147 |
| [RivalSearch MCP](https://github.com/damionrashford/RivalSearchMCP) | URL | Any MCP-compatible agent | Unifies web, social, news, academic, and entity-search sources behind MCP. | 2025-08-03 | 2026-05-31 | ⭐ 125 |
| [Deep Research MCP](https://github.com/pminervini/deep-research-mcp) | URL | Multiple / configurable agents | Connects several deep-research agents and model providers through one MCP interface. | 2025-08-07 | 2026-08-05 | ⭐ 108 |
| [Deep Web Research MCP](https://github.com/qpd-v/mcp-DEEPwebresearch) | URL | Any MCP-compatible agent | Coordinates recursive web search and page analysis for deeper topic coverage. | 2025-01-13 | 2025-03-05 | ⭐ 86 |
| [Agent Search](https://github.com/brcrusoe72/agent-search) | URL | Any MCP-compatible agent | Provides privacy-oriented search and browser retrieval for AI agents. | 2026-02-18 | 2026-07-07 | ⭐ 78 |
| [OpenRouter Deep Research MCP](https://github.com/wheattoast11/openrouter-deep-research-mcp) | URL | Any MCP-compatible agent | Orchestrates parallel research agents and consensus-backed synthesis through OpenRouter. | 2025-03-28 | 2026-03-04 | ⭐ 55 |
| [Web Researcher MCP](https://github.com/zoharbabin/web-researcher-mcp) | URL | Any MCP-compatible agent | Searches the web, extracts sources, and produces citation-aware research results. | 2026-05-18 | 2026-08-25 | ⭐ 53 |
| [GiaSip Skills](https://github.com/GiaSip/giasip-skills) | URL | Claude Code; OpenAI Codex | Provides quick recon, fact-checking, research orchestration, and multi-model dispatch. | 2026-05-30 | 2026-08-25 | ⭐ 12 |
| [Web Multi Search](https://github.com/soxoj/web-multi-search-skill) | URL | OpenClaw | Searches several web engines in parallel and exports deduplicated results. | 2026-02-08 | 2026-02-08 | ⭐ 8 |
| [Digital Research Skills](https://github.com/smarks26/digital-research-skills) | URL | Multiple / configurable agents | Plans evidence-driven research waves for OSINT, due diligence, trends, and long-form analysis. | 2026-05-29 | 2026-05-16 | ⭐ 6 |
| [Internet Archive MCP](https://github.com/cyanheads/internet-archive-mcp-server) | URL | Any MCP-compatible agent | Provides agent access to Internet Archive search, metadata, files, and preserved resources. | 2026-06-05 | 2026-08-21 | ⭐ 2 |
| [Agent Toolkit](https://github.com/000001000000/agent-toolkit) | URL | Any Agent Skills-compatible agent | Includes an OSINT dorking workflow with search tooling and evaluation assets. | 2026-04-11 | 2026-06-08 | ⭐ 1 |

<p align="right"><a href="#contents">Back to contents ↑</a></p>

<a id="dark-web"></a>

## 🧅 Dark Web <sup>3 projects</sup>

Tools for discovering, collecting, and analyzing onion services and dark-web content.

| Project | Target Input | AI Agent | Description | Created | Last Update | Stars |
|:---|:---|:---|:---|:---:|:---:|---:|
| [Darknet MCP Server](https://github.com/badchars/darknet-mcp-server) | Onion Service | Any MCP-compatible agent | Unifies dark-web search, breach, ransomware, malware, and blockchain intelligence tools for MCP clients. | 2026-06-23 | 2026-06-24 | ⭐ 316 |
| [OnionClaw](https://github.com/JacobJandon/OnionClaw) | Onion Service | OpenClaw | Adds Tor search, hidden-service retrieval, crawling, and export workflows to OpenClaw. | 2026-03-14 | 2026-05-28 | ⭐ 63 |
| [Sicry](https://github.com/JacobJandon/Sicry) | Onion Service | Any MCP-compatible agent; Generic AI agent | Checks Tor health, rotates identity, searches onion engines, fetches known services, and exposes optional agent-assisted analysis. | 2026-03-14 | 2026-05-28 | ⭐ 19 |

<p align="right"><a href="#contents">Back to contents ↑</a></p>

<a id="threat-intelligence"></a>

## 🛡️ Threat Intelligence <sup>11 projects</sup>

Tools for threat data, indicators, file hashes, vulnerabilities, and malware analysis.

| Project | Target Input | AI Agent | Description | Created | Last Update | Stars |
|:---|:---|:---|:---|:---:|:---:|---:|
| [CVE MCP Server](https://github.com/mukul975/cve-mcp-server) | CVE ID | Any MCP-compatible agent | Correlates CVE, EPSS, KEV, Shodan, VirusTotal, and related security intelligence. | 2026-04-14 | 2026-06-22 | ⭐ 1,318 |
| <img src=".github/assets/new-dot.svg" width="6" height="6" alt=""> [MCP Scanner](https://github.com/cisco-ai-defense/mcp-scanner) | URL; File | Claude Code | Scans remote and local Model Context Protocol servers for unsafe tools, prompts, resources, and instructions. | 2025-09-24 | 2026-08-28 | ⭐ 1,056 |
| [MCP Security Hub](https://github.com/FuzzingLabs/mcp-security-hub) | Domain; IP Address; URL; File; File Hash | Any MCP-compatible agent | Exposes containerized security tools for recon, threat intelligence, code, and binary analysis. | 2026-01-06 | 2026-04-08 | ⭐ 772 |
| [CTI Expert](https://github.com/7onez/cti-expert) | Domain; IP Address; URL; File Hash | Claude Code; OpenAI Codex | Guides structured cyber threat intelligence and OSINT collection with confidence scoring. | 2026-04-06 | 2026-08-28 | ⭐ 584 |
| [Reversecore MCP](https://github.com/sjkim1127/Reversecore_MCP) | File; File Hash | Any MCP-compatible agent | Connects agents to reverse engineering, malware, forensics, and vulnerability research tools. | 2025-11-10 | 2026-08-27 | ⭐ 194 |
| [Shodan MCP](https://github.com/w0h1v/mcp-shodan) | Domain; IP Address | Any MCP-compatible agent | Provides device search, IP reconnaissance, DNS, CPE, and CVE intelligence. | 2024-12-12 | 2026-03-31 | ⭐ 160 |
| [VirusTotal MCP](https://github.com/w0h1v/mcp-virustotal) | Domain; IP Address; URL; File; File Hash | Any MCP-compatible agent | Queries files, URLs, domains, IPs, and related security-analysis records. | 2024-12-13 | 2026-05-24 | ⭐ 149 |
| [ZettelForge](https://github.com/ThreatRecall/zettelforge) | Domain; IP Address; URL; File Hash | Multiple / configurable agents | Extracts IOCs and threat entities into a local STIX knowledge graph with agent access. | 2026-04-06 | 2026-07-10 | ⭐ 58 |
| [Malware Sandbox MCP](https://github.com/mukul975/Malware-Sandbox-mcp) | File; File Hash | Any MCP-compatible agent | Normalizes malware sandbox verdicts, IOCs, artifacts, and ATT&CK mappings. | 2026-06-11 | 2026-06-11 | ⭐ 27 |
| [MISP MCP](https://github.com/MISP/misp-mcp) | Domain; IP Address; URL; File Hash | Any MCP-compatible agent | Provides read-only access to MISP threat intelligence events and attributes. | 2026-04-01 | 2026-04-05 | ⭐ 9 |
| [OSINT MCP Gateway](https://github.com/bonetrees/osint-mcp-gateway) | Domain; IP Address; URL | Any MCP-compatible agent | Routes agent queries across VirusTotal, Shodan, DNS, WHOIS, RIPEstat, and OTX. | 2025-11-23 | 2026-06-10 | ⭐ 0 |

<p align="right"><a href="#contents">Back to contents ↑</a></p>

<a id="documents-records"></a>

## 📄 Documents & Records <sup>22 projects</sup>

Tools for documents, files, datasets, public records, extraction, and structured review.

| Project | Target Input | AI Agent | Description | Created | Last Update | Stars |
|:---|:---|:---|:---|:---:|:---:|---:|
| [Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills) | Document; Dataset | Multiple / configurable agents | Provides reusable scientific research workflows and access patterns for public databases. | 2025-10-19 | 2026-08-31 | ⭐ 40,325 |
| [notebooklm-py](https://github.com/teng-lin/notebooklm-py) | Document | Multiple / configurable agents | Gives agents programmatic, source-grounded access to NotebookLM research workflows. | 2026-01-07 | 2026-08-31 | ⭐ 19,029 |
| [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) | Document | Multiple / configurable agents | Orchestrates long-running research, cross-model review, experiments, and evidence capture. | 2026-03-10 | 2026-08-26 | ⭐ 15,493 |
| [NotebookLM CLI and MCP](https://github.com/jacob-bd/gemini-notebook-mcp-cli) | Document | Multiple / configurable agents | Connects AI agents to NotebookLM for cited source ingestion, querying, and synthesis. | 2025-12-23 | 2026-08-27 | ⭐ 5,982 |
| [Agentset](https://github.com/agentset-ai/agentset) | Document | Any MCP-compatible agent | Provides document ingestion, agentic search, ranking, citations, RAG, and MCP access. | 2025-03-10 | 2026-07-04 | ⭐ 2,077 |
| [PDF Reader MCP](https://github.com/SylphxAI/pdf-reader-mcp) | Document | Any MCP-compatible agent | Analyzes PDFs through MCP while retaining page references, visual crops, and OCR provenance. | 2025-04-04 | 2026-08-29 | ⭐ 907 |
| [Docling MCP](https://github.com/docling-project/docling-mcp) | Document | Any MCP-compatible agent | Exposes document conversion and structured extraction from files and URLs through MCP. | 2025-03-14 | 2026-08-24 | ⭐ 727 |
| [Claude Skills for Journalism](https://github.com/jamditis/claude-skills-journalism) | URL; Document | Claude Code | Covers source verification, public records, FOIA work, scraping, and newsroom research. | 2025-12-25 | 2026-08-29 | ⭐ 379 |
| [Simple PubMed MCP](https://github.com/andybrandt/mcp-simple-pubmed) | Document | Any MCP-compatible agent | Searches PubMed and retrieves biomedical article metadata and abstracts. | 2024-12-11 | 2026-03-19 | ⭐ 171 |
| [mcp.science](https://github.com/pathintegral-institute/mcp.science) | Document; Dataset | Any MCP-compatible agent | Connects agents to scientific literature search and research data services. | 2025-03-27 | 2025-09-02 | ⭐ 148 |
| [Data Commons Agent Toolkit](https://github.com/datacommonsorg/agent-toolkit) | Dataset | Any MCP-compatible agent | Connects agents and MCP clients to the public Data Commons knowledge graph. | 2025-06-26 | 2026-08-25 | ⭐ 139 |
| [Academia MCP](https://github.com/IlyaGusev/academia_mcp) | Document | Any MCP-compatible agent | Searches academic sources and retrieves papers for agent-assisted literature research. | 2025-01-24 | 2026-01-24 | ⭐ 90 |
| [ZotPilot](https://github.com/xunhe730/ZotPilot) | Document | Any MCP-compatible agent | Connects Zotero collections to source-grounded research and agent workflows. | 2026-03-16 | 2026-06-16 | ⭐ 71 |
| [OpenAlex Research MCP](https://github.com/oksure/openalex-research-mcp) | Document | Any MCP-compatible agent | Queries OpenAlex works, authors, institutions, concepts, and citation relationships. | 2025-10-05 | 2026-06-22 | ⭐ 47 |
| [European Parliament MCP](https://github.com/Hack23/European-Parliament-MCP-Server) | Name; Document | Any MCP-compatible agent | Provides agent access to European Parliament members, committees, votes, documents, and questions. | 2026-02-16 | 2026-08-31 | ⭐ 27 |
| [Semantic Scholar Skills](https://github.com/zongmin-yu/semantic-scholar-skills) | Document | Claude Code | Supports literature discovery, citation expansion, and structured Semantic Scholar research. | 2026-03-10 | 2026-03-16 | ⭐ 21 |
| [Newsroom Extension](https://github.com/ehurrn/newsroom-extension) | Organization Name; Document | Multiple / configurable agents | Supports investigative journalism, FOIA work, corporate research, verification, and editorial review. | 2026-04-06 | 2026-06-22 | ⭐ 7 |
| [Hermes OSINT Skill](https://github.com/mtjikuzu/hermes-osint-skill) | Name; Organization Name | Hermes Agent | Structures company due diligence, background checks, vendor risk, and privacy review. | 2026-05-22 | 2026-05-22 | ⭐ 7 |
| [Company Recon Skill](https://github.com/zoharbabin/company-recon-skill) | Organization Name; URL | Claude Code | Identifies websites using a company's technology and classifies the resulting evidence. | 2026-03-04 | 2026-03-04 | ⭐ 3 |
| [Infringement Information Collector](https://github.com/11murmur/infringement-information-collector) | Organization Name; URL | Claude Code | Collects public leads about counterfeits, private servers, and piracy into auditable reports. | 2026-05-31 | 2026-06-01 | ⭐ 2 |
| [OpenProbe](https://github.com/hxd0818/openprobe) | Name; Organization Name | OpenClaw | Investigates companies, competitors, supply chains, capital links, and key people. | 2026-04-12 | 2026-05-08 | ⭐ 2 |
| [Scout](https://github.com/indigokarasu/scout) | Name; Organization Name | Any Agent Skills-compatible agent | Structures lawful people and company research with provenance, source tiers, and refresh workflows. | 2026-03-10 | 2026-08-31 | ⭐ 1 |

<p align="right"><a href="#contents">Back to contents ↑</a></p>

<a id="geolocation"></a>

## 📍 Geolocation <sup>6 projects</sup>

Tools for locations, coordinates, maps, wireless identifiers, aircraft, and satellite data.

| Project | Target Input | AI Agent | Description | Created | Last Update | Stars |
|:---|:---|:---|:---|:---:|:---:|---:|
| <img src=".github/assets/new-dot.svg" width="6" height="6" alt=""> [Velocity](https://github.com/AndrewCTF/velocity) | Location; Aircraft ID; Event Data | Any MCP-compatible agent | Self-hosted situation console that fuses public aircraft, maritime, satellite, hazard, and conflict feeds with provenance, replay, and evidence capture. | 2026-06-12 | 2026-08-20 | ⭐ 82 |
| [Geo Trajectory Analysis](https://github.com/eyal-weiss/geo-trajectory-analysis) | Location; Video | Claude (agent unspecified) | Applies a documented video-geolocation method to estimate missile launch origins. | 2026-03-23 | 2026-03-23 | ⭐ 3 |
| <img src=".github/assets/new-dot.svg" width="6" height="6" alt=""> [Aircraft Research Skill](https://github.com/WPTK/aircraft-research-claude-skill) | Aircraft ID | Claude Code | Agent skill that traces an airframe registration through public records to its owning entities. | 2026-06-08 | 2026-06-17 | ⭐ 2 |
| [Bellingcat OSINT Toolkit Skills](https://github.com/CasualSecurityInc/Bellingcat-OSINT-Toolkit) | - | Any Agent Skills-compatible agent | Packages hundreds of investigation resources by geolocation, media, identity, transport, and conflict use case. | 2026-07-12 | 2026-07-12 | ⭐ 1 |
| [Norteia Lead Recon](https://github.com/Luispitik/norteia-lead-recon) | Name; Organization Name; Location | Claude Code | Researches Spanish companies and leads through official open registers and geodata. | 2026-04-29 | 2026-04-29 | ⭐ 0 |
| [Geolocation Skill](https://github.com/zuocharles/geolocation-skill) | Location; Image | Any Agent Skills-compatible agent | Guides photo geolocation with visual clues, map queries, and source references. | 2026-03-30 | 2026-03-31 | ⭐ 0 |

<p align="right"><a href="#contents">Back to contents ↑</a></p>

<a id="investigation"></a>

## 🔎 Investigation <sup>17 projects</sup>

Cross-cutting investigation, case-management, correlation, and research workspaces.

| Project | Target Input | AI Agent | Description | Created | Last Update | Stars |
|:---|:---|:---|:---|:---:|:---:|---:|
| [Anthropic Cybersecurity Skills](https://github.com/mukul975/Anthropic-Cybersecurity-Skills) | - | Multiple / configurable agents | Packages extensive offensive, defensive, CTI, forensics, and reconnaissance procedures. | 2026-02-25 | 2026-08-31 | ⭐ 31,771 |
| [Claude Skills](https://github.com/alirezarezvani/claude-skills) | - | Multiple / configurable agents | Includes research, security, market analysis, compliance, and evidence-oriented agent skills. | 2025-10-19 | 2026-08-26 | ⭐ 25,293 |
| [CTF Skills](https://github.com/ljagiello/ctf-skills) | - | Any Agent Skills-compatible agent | Supplies agent workflows for CTF categories including OSINT, forensics, and web investigation. | 2026-02-01 | 2026-08-25 | ⭐ 3,143 |
| [OpenOSINT](https://github.com/OpenOSINT/OpenOSINT) | - | Multiple / configurable agents | Combines OSINT tools in an interactive agent, command-line interface, and MCP server. | 2026-05-06 | 2026-08-26 | ⭐ 1,500 |
| [Hackingtool Plugin](https://github.com/AKCodez/hackingtool-plugin) | - | Claude Code | Makes a large catalogue of pentest and OSINT tools discoverable and runnable by Claude. | 2026-04-23 | 2026-04-25 | ⭐ 1,024 |
| <img src=".github/assets/new-dot.svg" width="6" height="6" alt=""> [World Intel MCP](https://github.com/marc-shade/world-intel-mcp) | Keyword; Location; Event Data | Any MCP-compatible agent | Provides an MCP server, CLI, and dashboard for cited multi-source global intelligence, geofenced monitoring, alerts, and situation briefs. | 2025-11-29 | 2026-08-16 | ⭐ 596 |
| [Huntkit](https://github.com/assafkip/huntkit) | Name; Organization Name; Event Data | Claude Code | Organizes cases, targets, findings, timelines, evidence hashes, and chain-of-custody records. | 2026-04-15 | 2026-07-06 | ⭐ 51 |
| [deep-recon](https://github.com/kvarnelis/deep-recon) | - | Claude Code | Coordinates multi-agent research and stores reconnaissance findings in Obsidian. | 2026-02-18 | 2026-02-21 | ⭐ 43 |
| [OSINT Skills](https://github.com/UseOSINT/Skills) | - | Cursor; Claude Code; compatible coding agents | Provides 28 source-grounded skills for agent-led OSINT workflows, evidence grading, and investigative reporting. | 2026-08-02 | 2026-08-03 | ⭐ 29 |
| [OSINT Agent Skills](https://github.com/frangelbarrera/osint-agent-skills) | - | Multiple / configurable agents | Combines OSINT playbooks, agent instructions, report templates, and MCP tool definitions. | 2026-06-27 | 2026-08-30 | ⭐ 25 |
| <img src=".github/assets/new-dot.svg" width="6" height="6" alt=""> [Claudii Exploratores](https://github.com/SOsintOps/claudii-exploratores) | - | Claude Code | Exposes a classified OSINT tool index, query builders, and identifier validators as a skill and MCP server. | 2026-07-10 | 2026-07-10 | ⭐ 13 |
| [OSINT Investigation](https://github.com/reichaves/osint-investigation) | Name; Username; Location; Image | Claude Code | Guides geolocation, source verification, entity profiling, and social-media investigation. | 2026-05-02 | 2026-05-03 | ⭐ 6 |
| <img src=".github/assets/new-dot.svg" width="6" height="6" alt=""> [Claude OSINT Deploy](https://github.com/soxoj/claude-osint-deploy) | - | Claude Code | Installs, runs, and verifies OSINT tools from public repositories inside an agent session. | 2026-08-25 | 2026-08-28 | ⭐ 5 |
| [OSINT Investigator](https://github.com/TNeagle/osint-investigator) | Name; Organization Name; Location; Coordinates | Claude Code | Coordinates multi-domain investigations, public-record research, geolocation, and intelligence reports. | 2026-03-18 | 2026-03-20 | ⭐ 3 |
| [OSINT Investigator for OpenClaw](https://github.com/Elyasuuuuu/osint-investigator) | Name; Username; Email; Organization Name; Domain; IP Address | OpenClaw | Correlates usernames, emails, domains, IPs, organizations, and public profile evidence. | 2026-03-16 | 2026-03-16 | ⭐ 1 |
| [Claude OSINT Plugin](https://github.com/lawriec/claude-osint-plugin) | URL; Image | Claude Code | Adds an intelligence-cycle methodology and configured search, media, archive, and analysis MCP servers. | 2026-04-09 | 2026-05-10 | ⭐ 1 |
| [OSINT Researcher](https://github.com/MrBridgeHQ/osint-researcher-claude) | - | Claude Code | Provides scoped OSINT, CTI, due diligence, and evidence-reporting procedures. | 2026-07-01 | 2026-07-06 | ⭐ 1 |

<p align="right"><a href="#contents">Back to contents ↑</a></p>
