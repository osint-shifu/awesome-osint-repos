<a id="top"></a>

<div align="center">
  <h1>Awesome OSINT Repositories</h1>
  <p>A catalogue of open-source OSINT tools organized into 12 clear categories and concrete input types.</p>
  <p>
    <a href="EMERGING.md"><img alt="Emerging projects: 92" src="https://img.shields.io/badge/emerging-92-bf8700?style=flat-square"></a>
    <a href="#social-media"><img alt="Social Media projects: 69" src="https://img.shields.io/badge/social_media-69-8250df?style=flat-square"></a>
    <a href="AGENTIC.md"><img alt="Agentic integrations: 125" src="https://img.shields.io/badge/agentic_integrations-125-d1242f?style=flat-square"></a>
    <img alt="Catalogue projects: 442" src="https://img.shields.io/badge/catalogue_projects-442-8250df?style=flat-square">
    <img alt="Last update: 2026-08-24" src="https://img.shields.io/badge/last_update-2026--08--24-1f883d?style=flat-square">
  </p>
  <p><strong><a href="README.md">Awesome OSINT Repositories</a></strong> · <a href="EMERGING.md">Emerging Projects</a> · <a href="AGENTIC.md">Agentic AI OSINT</a> · <a href="TIMELINE.md">Catalogue Timeline</a> · <a href="osint-repositories.csv">Repository Database CSV</a></p>
</div>

## About this catalogue

Awesome OSINT Repositories is a repository-first catalogue of open-source investigative software. Every record represents a public source-code repository containing an identifiable tool or integration with a practical OSINT use case.

Each project has exactly one value in `Categories`. `Target Input` contains only concrete data accepted or investigated by the tool, such as `Username`, `Domain`, `IP Address`, `URL`, `File Hash`, or `Onion Service`. A project may have multiple target inputs.

`Emerging Projects` and `Agentic AI OSINT` are additional generated views selected through `Source Files`; they are not category values.

| File | What it contains |
|---|---|
| [`README.md`](README.md) | Main catalogue with one section for each of the 12 categories. |
| [`EMERGING.md`](EMERGING.md) | Early-stage tools and projects worth monitoring. |
| [`AGENTIC.md`](AGENTIC.md) | Skills, plugins, MCP servers, and AI-agent integrations grouped by main category. |
| [`TIMELINE.md`](TIMELINE.md) | Visual chronology of catalogue additions with descriptions, categories, and current star counts. |
| [`osint-repositories.csv`](osint-repositories.csv) | Canonical repository database in CSV format with all accepted records and current metadata. |

> [!IMPORTANT]
> Only implementation-bearing repositories with publicly accessible source code are included. Closed-source services, link collections, courses, articles, prompt-only lists, datasets without an implemented tool, and repository stubs are excluded.

> <img src=".github/assets/new-dot.svg" width="6" height="6" alt=""> marks projects added to the catalogue within the last 14 days.

<a id="table-of-contents"></a>

## Table of contents

- [Identity](#identity) <sup>30 projects</sup>
- [Social Media](#social-media) <sup>69 projects</sup>
- [Code Repositories](#code-repositories) <sup>14 projects</sup>
- [Infrastructure](#infrastructure) <sup>56 projects</sup>
- [Web](#web) <sup>77 projects</sup>
- [Dark Web](#dark-web) <sup>15 projects</sup>
- [Threat Intelligence](#threat-intelligence) <sup>21 projects</sup>
- [Documents & Records](#documents-records) <sup>44 projects</sup>
- [Media](#media) <sup>46 projects</sup>
- [Geolocation](#geolocation) <sup>34 projects</sup>
- [Cryptocurrency](#cryptocurrency) <sup>8 projects</sup>
- [Investigation](#investigation) <sup>28 projects</sup>
- [Emerging projects](EMERGING.md) <sup>92 projects</sup>
- [Agentic AI OSINT](AGENTIC.md) <sup>125 projects</sup>
- [Catalogue timeline](TIMELINE.md)
- [Complete repository database (CSV)](osint-repositories.csv) <sup>442 unique repositories</sup>

---

<a id="identity"></a>

## 👤 Identity <sup>30 projects</sup>

Tools centered on people, names, contact identifiers, and identity resolution.

| Project | Type | Target Input | Description | Created | Last Update | Stars |
|:---|:---|:---|:---|:---:|:---:|---:|
| [GHunt](https://github.com/mxrch/GHunt) | Python | Name | Collects public information associated with Google accounts and identifiers. | 2020-10-02 | 2026-04-10 | ⭐ 19,407 |
| [PhoneInfoga](https://github.com/sundowndev/phoneinfoga) | Go | Phone Number | Collects and correlates publicly available information about phone numbers. | 2018-10-25 | 2026-01-06 | ⭐ 17,613 |
| [Holehe](https://github.com/megadose/holehe) | Python | Email | Checks whether an email address is registered with supported online services. | 2020-06-25 | 2024-09-10 | ⭐ 14,086 |
| [h8mail](https://github.com/khast3x/h8mail) | Python | Email | Searches breach sources and local datasets for email-related records. | 2018-06-15 | 2022-06-25 | ⭐ 5,270 |
| [pwnedOrNot](https://github.com/thewhiteh4t/pwnedOrNot) | Python | Email | Searches breach data for passwords associated with an email address. | 2018-05-25 | 2026-03-28 | ⭐ 2,628 |
| [SearchPhone](https://github.com/HackUnderway/SearchPhone) | Python | Phone Number | Aggregates phone number searches and produces investigation reports. | 2024-11-12 | 2026-08-23 | ⭐ 1,632 |
| [username-anarchy](https://github.com/urbanadventurer/username-anarchy) | Ruby | Username | Generates likely username permutations from names and naming patterns. | 2012-11-07 | 2024-09-20 | ⭐ 1,454 |
| [Phunter](https://github.com/N0rz3/Phunter) | Python | Phone Number | Aggregates several public phone number investigation methods. | 2023-12-30 | 2024-04-06 | ⭐ 1,172 |
| [Zehef](https://github.com/N0rz3/Zehef) | Python | Email | Aggregates public information associated with an email address. | 2023-06-13 | 2024-11-13 | ⭐ 1,060 |
| [iKy](https://github.com/kennbroorg/iKy) | Python | Email | Builds profiles and timelines from email-based investigation modules. | 2018-12-14 | 2026-07-20 | ⭐ 969 |
| [mailcat](https://github.com/sharsil/mailcat) | Python | Email | Finds existing email addresses derived from a nickname. | 2021-08-20 | 2026-05-24 | ⭐ 932 |
| [GHOST OSINT CRM](https://github.com/elm1nst3r/GHOST-osint-crm) | JavaScript | Name | Manages people, relationships, evidence, and investigation notes locally. | 2025-05-16 | 2026-08-23 | ⭐ 864 |
| [Emora](https://github.com/idefasoft/Emora-Project) | C# | Username | Provides a graphical interface for cross-platform username searches. | 2024-03-11 | 2026-02-07 | ⭐ 714 |
| [MailAccess](https://github.com/KatrielMoses/MailAccess) | Python | Name; Email | Clusters identities and checks service usage and breach references for emails. | 2026-05-18 | 2026-08-05 | ⭐ 652 |
| [Leaker](https://github.com/vflame6/leaker) | Go | Username; Email | Performs passive leak enumeration across multiple breach sources. | 2025-12-25 | 2026-08-19 | ⭐ 584 |
| [Deanonymizer](https://github.com/ni5arga/deanonymizer) | TypeScript | Name | Compares public posting history and behavioral timing patterns. | 2026-06-02 | 2026-06-15 | ⭐ 334 |
| [vesper](https://github.com/krishpranav/vesper) | Rust | Username | Performs lightweight username checks across online services. | 2021-06-20 | 2026-08-17 | ⭐ 327 |
| [Nox Framework](https://github.com/nox-project/nox-framework) | Python | Name; Email | Automates identity pivots and risk analysis across public sources. | 2026-04-07 | 2026-05-06 | ⭐ 321 |
| [FindME](https://github.com/0xSaikat/findme) | HTML | Username | Searches social and online profiles associated with a username. | 2025-01-14 | 2026-07-03 | ⭐ 314 |
| <img src=".github/assets/new-dot.svg" width="6" height="6" alt=""> [sharetrace](https://github.com/soxoj/sharetrace) | Python | URL | Extracts public identity metadata exposed by supported social, document, code, and content-sharing links. | 2026-03-29 | 2026-05-26 | ⭐ 218 |
| [Telespot](https://github.com/thumpersecure/Telespot) | Python | Phone Number | Searches phone-number variations across public engines and correlates identity clues. | 2025-12-28 | 2026-02-26 | ⭐ 138 |
| [OSINT Skill](https://github.com/smixs/osint-skill) | Skill | Name | Runs phased people research with source grading, correlation, and report generation. | 2026-03-10 | 2026-03-10 | ⭐ 110 |
| [Telespotter](https://github.com/thumpersecure/Telespotter) | Rust | Phone Number | Searches phone numbers across public engines and people-search sources in a Rust CLI. | 2026-01-02 | 2026-02-27 | ⭐ 76 |
| [glit](https://github.com/shadawck/glit) | Rust | Email | Extracts contributor email addresses from Git repositories and organizations. | 2022-11-14 | 2024-05-01 | ⭐ 58 |
| [Bellingcat Name Variant Search](https://github.com/bellingcat/name-variant-search) | Python | Name | Generates and searches spelling and transliteration variants of personal names. | 2023-07-18 | 2026-06-25 | ⭐ 53 |
| [Wiwok](https://github.com/Kirozaku/Wiwok) | Python | Username; Email; Phone Number | Investigates usernames, email addresses, phone numbers, and names without mandatory API keys. | 2026-04-26 | 2026-05-22 | ⭐ 40 |
| [odnoklassniki-checker](https://github.com/OSINT-mindset/odnoklassniki-checker) | Python | Phone Number | Looks for public OK.ru account data using a phone number or email. | 2022-10-15 | 2024-10-02 | ⭐ 20 |
| [OSINT AI Agent](https://github.com/sumba101/OSINT-AI-Agent) | Agent + skills | Name; Username; Email | Orchestrates Holehe, Sherlock, and GHunt for person-focused investigations. | 2026-01-11 | 2026-01-11 | ⭐ 10 |
| [Deep Research Ladder](https://github.com/hint-shu/deep-research) | Skills + plugin | Name; URL | Scales from fact checks to long-form research and OSINT entity reconnaissance. | 2026-04-17 | 2026-04-29 | ⭐ 3 |
| [Email Finder Batch](https://github.com/yoitsyoung/email-finder-batch) | Skill | Email | Coordinates public-source email discovery, pattern generation, and verification agents. | 2026-03-22 | 2026-03-22 | ⭐ 2 |

<p align="right"><a href="#table-of-contents">Back to contents ↑</a></p>

<a id="social-media"></a>

## 💬 Social Media <sup>69 projects</sup>

Tools for discovering and analyzing public accounts and content on social platforms.

| Project | Type | Target Input | Description | Created | Last Update | Stars |
|:---|:---|:---|:---|:---:|:---:|---:|
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | Python | Username; Video | Downloads public video, audio, subtitles, comments, and metadata from supported platforms. | 2020-10-26 | 2026-08-20 | ⭐ 186,544 |
| [Sherlock](https://github.com/sherlock-project/sherlock) | Python | Username | Checks a username across many social networks. | 2018-12-24 | 2026-08-01 | ⭐ 90,122 |
| [Agent Reach](https://github.com/Panniantong/Agent-Reach) | CLI + skill | Username; URL | Gives agents collection workflows for public content across multiple social and developer platforms. | 2026-02-24 | 2026-08-12 | ⭐ 74,561 |
| [last30days](https://github.com/mvanhorn/last30days-skill) | Skill + plugin | Username; URL | Researches recent discussion across social platforms, communities, prediction markets, and the web. | 2026-01-23 | 2026-08-21 | ⭐ 59,115 |
| [Maigret](https://github.com/soxoj/maigret) | Python | Username | Builds username-based account reports across thousands of sites. | 2020-06-27 | 2026-08-23 | ⭐ 36,987 |
| [Social Analyzer](https://github.com/qeeqbox/social-analyzer) | JavaScript | Name; Username | Searches and analyzes profiles across numerous social platforms. | 2020-11-30 | 2026-01-12 | ⭐ 23,817 |
| [Osintgram](https://github.com/Datalux/Osintgram) | Python | Name; Username; Image | Provides an interactive interface for collecting information from Instagram profiles. | 2019-06-07 | 2025-08-25 | ⭐ 14,101 |
| [Nitter](https://github.com/zedeus/nitter) | Nim | Username | Provides a privacy-oriented front end for viewing public X content. | 2019-06-20 | 2026-08-22 | ⭐ 13,481 |
| [Instaloader](https://github.com/instaloader/instaloader) | Python | Name; Username; Image | Downloads Instagram posts, captions, profile data, and related metadata. | 2016-06-15 | 2026-07-26 | ⭐ 13,215 |
| [DiscordChatExporter](https://github.com/Tyrrrz/DiscordChatExporter) | C# | Username | Exports accessible Discord message history and rich media to local files. | 2017-07-12 | 2026-08-07 | ⭐ 11,830 |
| [Blackbird](https://github.com/p1ngul1n0/blackbird) | Python | Username | Searches social platforms for accounts linked to a username or email. | 2022-05-06 | 2025-07-13 | ⭐ 7,824 |
| [twikit](https://github.com/d60/twikit) | Python | Username | Provides an alternative Python client for collecting and interacting with public X data. | 2024-01-20 | 2026-03-10 | ⭐ 4,628 |
| [Snoop](https://github.com/snooppr/snoop) | Python | Username | Searches for username usage across a large collection of websites. | 2020-02-14 | 2026-07-30 | ⭐ 4,010 |
| [gosearch](https://github.com/ibnaleem/gosearch) | Go | Username | Searches for a person's digital footprint across hundreds of websites. | 2024-11-09 | 2026-07-08 | ⭐ 3,634 |
| [Aliens Eye](https://github.com/arxhr007/Aliens_eye) | Python | Username | Searches for accounts associated with a username across hundreds of platforms. | 2021-09-22 | 2026-07-16 | ⭐ 3,486 |
| [user-scanner](https://github.com/kaifcodec/user-scanner) | Python | Username; Email | Runs username and email discovery checks across many services. | 2025-10-19 | 2026-08-23 | ⭐ 3,282 |
| [Tookie](https://github.com/Alfredredbird/tookie-osint) | Python | Username | Provides a multi-target information gathering toolkit. | 2023-08-22 | 2026-07-22 | ⭐ 2,827 |
| [WhatsMyName](https://github.com/WebBreacher/WhatsMyName) | Python | Username | Checks usernames using community-maintained site definitions and scripts. | 2015-10-02 | 2026-08-16 | ⭐ 2,796 |
| [twscrape](https://github.com/vladkens/twscrape) | Python | Username | Collects public X data through supported GraphQL endpoints with account-pool rotation. | 2023-05-05 | 2026-08-07 | ⭐ 2,700 |
| [Yark](https://github.com/Owez/yark) | Python | Name; Username; Video | Archives public YouTube channels, videos, and metadata for local analysis. | 2022-08-16 | 2025-12-17 | ⭐ 2,183 |
| [linkedin2username](https://github.com/initstring/linkedin2username) | Python | Name; Organization Name | Generates possible corporate usernames from public LinkedIn employee data. | 2018-02-22 | 2026-05-20 | ⭐ 1,824 |
| [Telegram Phone Number Checker](https://github.com/bellingcat/telegram-phone-number-checker) | Python | Username | Checks whether supplied phone numbers are connected to Telegram accounts. | 2021-02-17 | 2026-08-17 | ⭐ 1,771 |
| [Informer](https://github.com/paulpierre/informer) | Python | Username | Collects and indexes Telegram channel and group activity. | 2019-12-09 | 2025-10-20 | ⭐ 1,659 |
| [CrossLinked](https://github.com/m8sec/CrossLinked) | Python | Name; Organization Name | Extracts employee names from public LinkedIn search results. | 2019-05-16 | 2024-11-26 | ⭐ 1,580 |
| [Arctic Shift](https://github.com/ArthurHeitmann/arctic_shift) | TypeScript | Username | Provides searchable Reddit archives through data dumps, an API, and a web interface. | 2023-08-03 | 2026-08-09 | ⭐ 1,425 |
| [Telerecon](https://github.com/sockysec/Telerecon) | Python | Username | Provides a modular framework for researching Telegram entities. | 2023-08-30 | 2024-04-22 | ⭐ 1,324 |
| [Instagram Monitor](https://github.com/misiektoja/instagram_monitor) | Python | Username; Image | Tracks public Instagram profile changes, activity, and captured content. | 2024-04-25 | 2026-08-23 | ⭐ 1,280 |
| [Telepathy Community](https://github.com/prose-intelligence-ltd/Telepathy-Community) | Python | Username | Collects and analyzes public Telegram chat data. | 2022-01-17 | 2026-08-10 | ⭐ 1,235 |
| [socid-extractor](https://github.com/soxoj/socid-extractor) | Python | Username | Converts profile URLs into structured identity records across many platforms. | 2019-11-17 | 2026-08-18 | ⭐ 1,069 |
| [Universal Reddit Scraper](https://github.com/JosephLai241/URS) | Python | Username | Scrapes and archives Reddit submissions, comments, and user activity. | 2019-03-20 | 2026-07-11 | ⭐ 1,020 |
| [Linkook](https://github.com/JackJuly/linkook) | Python | Username | Discovers linked social accounts and email clues from a username. | 2025-01-30 | 2026-02-28 | ⭐ 1,007 |
| [X Tweet Fetcher](https://github.com/ythx-101/x-tweet-fetcher) | Python | Username | Retrieves public X posts, replies, timelines, and articles without login. | 2026-02-14 | 2026-08-08 | ⭐ 940 |
| [Osintgraph](https://github.com/XD-MHLOO/Osintgraph) | Python | Username; Image | Maps Instagram followers and relationships in Neo4j for network analysis. | 2025-04-30 | 2026-05-10 | ⭐ 930 |
| [Tosint](https://github.com/drego85/tosint) | Python | Username | Extracts Telegram bot, chat, and user information from tokens and identifiers. | 2021-07-26 | 2026-07-29 | ⭐ 847 |
| [LinkedInDumper](https://github.com/l4rm4nd/LinkedInDumper) | Python | Name; Organization Name | Extracts company employee records through LinkedIn endpoints. | 2022-10-17 | 2026-08-21 | ⭐ 608 |
| [Discord History Tracker](https://github.com/chylex/Discord-History-Tracker) | C# | Username | Saves accessible Discord chat history for offline preservation and review. | 2016-10-22 | 2026-01-29 | ⭐ 584 |
| [Maltego Telegram](https://github.com/vognik/maltego-telegram) | Python | Username | Adds Maltego transforms for Telegram channels, groups, users, and messages. | 2024-11-04 | 2026-01-27 | ⭐ 552 |
| [TeleTracker](https://github.com/tsale/TeleTracker) | Python | Username | Collects Telegram channel information and supports repeatable investigation tasks. | 2024-01-15 | 2024-04-29 | ⭐ 540 |
| [tubeup](https://github.com/bibanon/tubeup) | Python | Username; Video | Archives online video and metadata to the Internet Archive through yt-dlp. | 2016-02-05 | 2026-08-12 | ⭐ 514 |
| [SoIG](https://github.com/yezz123/SoIG) | Python | Username; Image | Retrieves selected public information associated with an Instagram account. | 2020-06-08 | 2026-06-28 | ⭐ 409 |
| [telegram-tracker](https://github.com/estebanpdl/telegram-tracker) | Python | Username | Exports channel details and posts from selected Telegram channels. | 2022-04-06 | 2026-04-20 | ⭐ 383 |
| [WhatsOSINT](https://github.com/HackUnderway/WhatsOSINT) | Python | Username; Phone Number | Retrieves public WhatsApp account details associated with a number. | 2024-11-19 | 2026-08-15 | ⭐ 332 |
| [SnapIntel](https://github.com/Kr0wZ/SnapIntel) | Python | Username | Retrieves public account details associated with Snapchat usernames. | 2021-03-02 | 2026-03-24 | ⭐ 329 |
| [Marple](https://github.com/soxoj/marple) | Python | Username | Finds profile links through search engines and extensible analysis plugins. | 2021-11-16 | 2026-08-17 | ⭐ 321 |
| [TeleGraphite](https://github.com/hamodywe/telegram-scraper-TeleGraphite) | Python | Username | Collects Telegram channel posts and exports them as JSON. | 2025-04-12 | 2026-08-11 | ⭐ 275 |
| [MCP Maigret](https://github.com/w0h1v/mcp-maigret) | MCP server | Username | Exposes Maigret username searches and public account discovery through MCP. | 2024-12-13 | 2026-01-27 | ⭐ 258 |
| [xint](https://github.com/0xNyk/xint) | CLI + skill + MCP | Username | Searches, monitors, and exports public X data for agent-assisted investigations. | 2026-02-14 | 2026-08-20 | ⭐ 248 |
| [Reddit Research MCP](https://github.com/dialog-tools/reddit-research-mcp) | MCP server | Username; URL | Supports structured Reddit discovery, thread collection, and community research. | 2025-08-12 | 2026-08-14 | ⭐ 233 |
| [Telegram Similar Channels](https://github.com/SocialLinks-IO/telegram-similar-channels) | Python | Username | Finds related Telegram channels through CLI and Maltego interfaces. | 2023-12-07 | 2024-04-10 | ⭐ 197 |
| [Telegram Archive](https://github.com/GeiserX/Telegram-Archive) | Python | Username | Creates incremental local archives of Telegram chats, media, and message history. | 2025-11-25 | 2026-08-23 | ⭐ 189 |
| [TikSpyder](https://github.com/estebanpdl/tik-spyder) | Python | Username; Video | Collects TikTok search, user, tag, and media data through SerpAPI and Apify. | 2024-07-16 | 2026-02-27 | ⭐ 102 |
| [steam-osint](https://github.com/matiash26/steam-osint) | Python | Username | Finds mutual friends between public Steam profiles. | 2022-03-12 | 2026-08-22 | ⭐ 97 |
| [OWASP Social OSINT Agent](https://github.com/bm-github/owasp-social-osint-agent) | Python | Username | Collects public social activity and uses configurable language models to produce analytical reports. | 2025-10-07 | 2026-04-25 | ⭐ 97 |
| [Social OSINT](https://github.com/krishpranav/socialosint) | Rust | Username; Email | Collects exposed email addresses from supported social platforms and checks related leak data. | 2021-07-02 | 2026-02-10 | ⭐ 95 |
| [insto](https://github.com/subzeroid/insto) | Python | Username; Image | Collects Instagram profile, media, relationship, and timeline data through interchangeable backends. | 2026-04-26 | 2026-06-20 | ⭐ 90 |
| [Telegram OSINT Polo](https://github.com/Ironship/TelegramOSINTPolo) | Python | Username | Downloads Telegram feed posts for local review and assisted analysis. | 2025-03-04 | 2026-03-12 | ⭐ 56 |
| [Steam Monitor](https://github.com/misiektoja/steam_monitor) | Python | Username | Tracks public Steam player activity, game sessions, and status changes. | 2024-04-25 | 2026-08-04 | ⭐ 56 |
| [LinkedIn OSINT Toolkit](https://github.com/michaelelizarov/linkedin-osint-toolkit) | Python | Name; Organization Name | Discovers companies and employees, classifies roles, and builds organization views. | 2026-02-16 | 2026-02-16 | ⭐ 45 |
| [x-scraper](https://github.com/proxidize/x-scraper) | Python | Username | Collects X timelines and search results through Playwright with resume and proxy controls. | 2025-10-30 | 2026-06-22 | ⭐ 33 |
| [SteamReveal](https://github.com/Berchez/SteamReveal) | TypeScript | Username | Analyzes Steam profiles for close contacts and possible location clues. | 2024-02-20 | 2026-08-22 | ⭐ 26 |
| [discord-urls-extractor](https://github.com/TheTechRobo/discord-urls-extractor) | Rust | Username; URL | Extracts URLs and media references from supported Discord archive formats. | 2021-11-21 | 2024-12-19 | ⭐ 21 |
| [YouTube Research MCP](https://github.com/coyaSONG/youtube-mcp-server) | MCP server | Username; Video | Exposes YouTube videos, channels, search results, comments, and transcripts through MCP. | 2025-03-31 | 2026-07-17 | ⭐ 16 |
| [Discord Inspector](https://github.com/Euronymou5/Discord-Inspector) | Python | Username | Retrieves public user, server, and application metadata from Discord identifiers. | 2024-12-03 | 2024-12-05 | ⭐ 6 |
| [Telegram MCP TDLib](https://github.com/tolboy/telegram-mcp-tdlib) | MCP server | Username | Exposes Telegram searches, chats, messages, and public content to MCP clients through TDLib. | 2026-07-04 | 2026-08-22 | ⭐ 2 |
| [OSINT Social](https://github.com/guleguleguru/osint-social) | Skill | Username | Wraps broad username discovery with additional coverage for major Chinese platforms. | 2026-02-28 | 2026-02-28 | ⭐ 1 |
| [LinkedIn Recon Skill](https://github.com/Kewanvk/linkedin-recon-skill) | Skill | Name; Organization Name | Maps public hiring networks and organizational relationships from LinkedIn evidence. | 2026-05-08 | 2026-05-25 | ⭐ 0 |
| [Sherlock Skill](https://github.com/ImL1s/sherlock-skill) | Skill | Username | Wraps Sherlock username searches with a portable skill and structured dossier output. | 2026-04-22 | 2026-04-22 | ⭐ 0 |
| [Chinese OSINT Skills](https://github.com/zomin/chinese-osint-skills) | Skill pack | Username | Supplies Chinese-platform research methods and scripts for cross-platform identity pivots. | 2026-04-30 | 2026-04-30 | ⭐ 0 |
| [X Archive RAG](https://github.com/mameshivaa/x-archive-rag) | RAG system | Username | Indexes exported X data for local semantic search and retrieval-augmented analysis. | 2026-05-26 | 2026-06-18 | ⭐ 0 |

<p align="right"><a href="#table-of-contents">Back to contents ↑</a></p>

<a id="code-repositories"></a>

## 💻 Code Repositories <sup>14 projects</sup>

Tools that investigate public source-code repositories, accounts, and repository metadata.

| Project | Type | Target Input | Description | Created | Last Update | Stars |
|:---|:---|:---|:---|:---:|:---:|---:|
| [Gitleaks](https://github.com/gitleaks/gitleaks) | Go | Username; Repository URL | Scans Git repositories and other inputs for hardcoded secrets and credentials. | 2018-01-27 | 2026-07-22 | ⭐ 28,928 |
| [TruffleHog](https://github.com/trufflesecurity/trufflehog) | Go | Username; Repository URL | Finds, verifies, and analyzes exposed credentials across supported code and storage sources. | 2016-12-31 | 2026-08-21 | ⭐ 27,567 |
| [github-dorks](https://github.com/techgaun/github-dorks) | Python | Username; Repository URL | Runs GitHub search queries intended to locate exposed sensitive data. | 2015-10-11 | 2025-10-05 | ⭐ 3,268 |
| [gitGraber](https://github.com/hisxo/gitGraber) | Python | Username; Repository URL | Monitors public GitHub activity for exposed credentials and service tokens. | 2019-09-04 | 2024-07-19 | ⭐ 2,373 |
| [Bellingcat Octosuite](https://github.com/bellingcat/octosuite) | Python | Username; Repository URL | Collects and analyzes public GitHub repository, user, organization, and activity data. | 2022-02-24 | 2026-02-28 | ⭐ 1,895 |
| [Betterleaks](https://github.com/betterleaks/betterleaks) | Go | Username; Repository URL | Scans supported code and storage sources for secrets with configurable detection and validation. | 2026-02-03 | 2026-08-20 | ⭐ 1,764 |
| [GitGot](https://github.com/BishopFox/GitGot) | Python | Username; Repository URL | Searches public GitHub data for exposed secrets using feedback-driven queries. | 2019-06-14 | 2024-03-07 | ⭐ 1,570 |
| [git-hound](https://github.com/tillson/git-hound) | Go | Username; Repository URL | Searches GitHub at scale for exposed secrets and dork matches. | 2019-07-16 | 2025-11-20 | ⭐ 1,451 |
| [GitFive](https://github.com/mxrch/GitFive) | Python | Name; Username; Repository URL | Correlates public GitHub account data for identity-focused investigations. | 2022-10-05 | 2025-10-04 | ⭐ 1,020 |
| [GitSint](https://github.com/N0rz3/GitSint) | Python | Username; Repository URL | Collects public intelligence about GitHub users and repositories. | 2023-04-26 | 2026-06-28 | ⭐ 253 |
| [Gitxray](https://github.com/kulkansecurity/gitxray) | Python | Username; Repository URL | Uses public GitHub APIs for account, repository, and contribution analysis. | 2024-08-06 | 2026-01-09 | ⭐ 184 |
| [Shotstars](https://github.com/snooppr/shotstars) | Python | Username; Repository URL | Analyzes repository star history and indicators of artificial activity. | 2024-05-25 | 2026-06-04 | ⭐ 115 |
| [GitRecon](https://github.com/atiilla/gitrecon) | JavaScript | Username; Repository URL | Scans a GitHub user's repositories for exposed names and email addresses. | 2023-09-03 | 2025-12-29 | ⭐ 54 |
| [GitHub Monitor](https://github.com/misiektoja/github_monitor) | Python | Username; Repository URL | Tracks GitHub profile and repository activity with change notifications. | 2024-05-11 | 2026-08-04 | ⭐ 53 |

<p align="right"><a href="#table-of-contents">Back to contents ↑</a></p>

<a id="infrastructure"></a>

## 🌐 Infrastructure <sup>56 projects</sup>

Tools for domains, IP addresses, networks, ASNs, and related internet infrastructure.

| Project | Type | Target Input | Description | Created | Last Update | Stars |
|:---|:---|:---|:---|:---:|:---:|---:|
| [SpiderFoot](https://github.com/smicallef/spiderfoot) | Python | Email; Domain; IP Address | Automates multi-source OSINT collection and attack-surface mapping. | 2012-04-28 | 2023-11-05 | ⭐ 21,378 |
| [theHarvester](https://github.com/laramies/theHarvester) | Python | Domain | Collects names, email addresses, subdomains, and hosts from public sources. | 2011-01-01 | 2026-08-22 | ⭐ 17,177 |
| [Amass](https://github.com/owasp-amass/amass) | Go | Domain | Maps external assets and discovers domains from multiple data sources. | 2018-07-10 | 2026-04-07 | ⭐ 15,028 |
| [Subfinder](https://github.com/projectdiscovery/subfinder) | Go | Domain | Enumerates subdomains using passive online sources. | 2018-03-31 | 2026-08-22 | ⭐ 14,283 |
| [HexStrike AI](https://github.com/0x4m4/hexstrike-ai) | MCP server | Domain; IP Address; URL | Connects agents to a large collection of security and reconnaissance tools. | 2025-07-10 | 2026-08-03 | ⭐ 11,320 |
| [BBOT](https://github.com/blacklanternsecurity/bbot) | Python | Domain | Recursively discovers internet-facing assets through modular scan events. | 2022-03-12 | 2026-07-21 | ⭐ 10,489 |
| [OneForAll](https://github.com/shmilylty/OneForAll) | Python | Domain | Combines numerous sources and methods for subdomain discovery. | 2018-12-10 | 2026-05-11 | ⭐ 10,023 |
| [reconFTW](https://github.com/six2dez/reconftw) | Shell | Domain | Orchestrates domain reconnaissance, asset collection, and follow-up checks. | 2020-12-30 | 2026-06-29 | ⭐ 8,019 |
| [Recon-ng](https://github.com/lanmaster53/recon-ng) | Python | Name; Organization Name; Domain | Organizes modular open-source intelligence collection in a command-line framework. | 2019-03-28 | 2024-11-01 | ⭐ 5,866 |
| [dnstwist](https://github.com/elceef/dnstwist) | Python | Domain | Generates and evaluates look-alike domains for phishing and impersonation research. | 2015-06-11 | 2025-04-15 | ⭐ 5,728 |
| [Claude Bug Bounty](https://github.com/Awarexone/claude-bug-bounty) | Skills + agents | Domain; URL | Organizes authorized bug-bounty reconnaissance, testing, validation, and reporting. | 2026-03-08 | 2026-08-23 | ⭐ 4,400 |
| [Knockpy](https://github.com/guelfoweb/knockpy) | Python | Domain | Enumerates subdomains and resolves related DNS information. | 2014-02-11 | 2026-02-19 | ⭐ 4,179 |
| [IVRE](https://github.com/ivre/ivre) | Python | IP Address | Builds searchable network intelligence from active and passive observations. | 2014-09-12 | 2026-07-26 | ⭐ 4,116 |
| [Findomain](https://github.com/Findomain/Findomain) | Rust | Domain | Discovers and monitors domains and subdomains from multiple sources. | 2019-04-14 | 2026-07-28 | ⭐ 3,784 |
| [Claude BugHunter](https://github.com/elementalsouls/Claude-BugHunter) | Skill pack | Domain; URL | Adds structured web reconnaissance and vulnerability-hunting methodology. | 2026-05-05 | 2026-08-24 | ⭐ 3,759 |
| [Uncover](https://github.com/projectdiscovery/uncover) | Go | IP Address | Queries internet search engines for exposed hosts matching a search. | 2022-03-02 | 2026-08-05 | ⭐ 3,040 |
| [FinalRecon](https://github.com/thewhiteh4t/FinalRecon) | Python | Domain | Collects headers, DNS records, subdomains, and related web intelligence. | 2019-03-28 | 2026-06-01 | ⭐ 2,952 |
| [Claude Red](https://github.com/SnailSploit/Claude-Red) | Skill pack | Domain; IP Address; URL | Provides red-team and security research playbooks for Claude-based workflows. | 2026-03-04 | 2026-05-08 | ⭐ 2,952 |
| [VulnClaw](https://github.com/Netw0rkNoob/VulnClaw) | Agent + skills + MCP | Domain; IP Address; URL | Orchestrates information gathering, vulnerability analysis, exploitation, and reporting. | 2026-04-18 | 2026-08-10 | ⭐ 2,946 |
| [dnsx](https://github.com/projectdiscovery/dnsx) | Go | Domain | Runs high-volume DNS queries and filters resolved records. | 2020-11-12 | 2026-08-24 | ⭐ 2,844 |
| [X-osint](https://github.com/TermuxHackz/X-osint) | Python | Name; Email; Phone Number; Domain | Runs phone, email, domain, VIN, and identity-oriented lookup modules. | 2023-03-11 | 2026-07-12 | ⭐ 2,617 |
| <img src=".github/assets/new-dot.svg" width="6" height="6" alt=""> [redamon](https://github.com/samugit83/redamon) | Agentic security framework | Domain; IP Address; URL | Coordinates AI-assisted reconnaissance, validation, remediation, and reporting workflows for authorized security testing. | 2025-12-29 | 2026-08-23 | ⭐ 2,346 |
| [Claude OSINT](https://github.com/elementalsouls/Claude-OSINT) | Skill pack | Domain; URL | Adds structured external reconnaissance methods, dorks, validators, and reporting guidance. | 2026-04-26 | 2026-08-10 | ⭐ 2,329 |
| [Pentest AI Agents](https://github.com/0xSteph/pentest-ai-agents) | Agent pack | Domain; IP Address; URL | Supplies specialized subagents for recon analysis, exploit research, detection, and reporting. | 2026-03-28 | 2026-08-16 | ⭐ 2,153 |
| [CyberStrike](https://github.com/CyberStrikeus/CyberStrike) | Agent + MCP | Domain; IP Address; URL | Runs agent-assisted offensive security with recon, testing, and evidence workflows. | 2026-02-14 | 2026-08-23 | ⭐ 1,948 |
| [SubDomainizer](https://github.com/nsonaniya2010/SubDomainizer) | Python | Domain | Finds subdomains and exposed data referenced in JavaScript files. | 2018-11-19 | 2026-08-11 | ⭐ 1,885 |
| [Hack Skills](https://github.com/yaklang/hack-skills) | Skill library | Domain; IP Address; URL | Covers reconnaissance, web and network security, forensics, reversing, and authorized research. | 2026-04-07 | 2026-06-16 | ⭐ 1,854 |
| [Metabigor](https://github.com/j3ssie/metabigor) | Go | IP Address; ASN | Correlates IP, ASN, domain, and network data without mandatory API keys. | 2019-05-24 | 2026-08-08 | ⭐ 1,732 |
| [Pentest AI](https://github.com/0xSteph/pentest-ai) | CLI + MCP | Domain; IP Address; URL | Exposes security tools, specialist agents, and deterministic probes through CLI and MCP. | 2026-04-04 | 2026-08-17 | ⭐ 1,620 |
| [ScopeSentry](https://github.com/Autumn-27/ScopeSentry) | Go | Domain; IP Address | Manages distributed asset discovery, monitoring, and exposure analysis. | 2024-02-27 | 2026-08-23 | ⭐ 1,582 |
| [domain-digger](https://github.com/wotschofsky/domain-digger) | TypeScript | Domain | Provides a web toolkit for DNS, certificate, hosting, and domain analysis. | 2021-07-29 | 2026-08-05 | ⭐ 1,335 |
| [Recon Skills](https://github.com/uphiago/recon-skills) | Skill pack | Domain; IP Address; URL | Provides field-oriented recon, dorking, secret discovery, asset mapping, and testing playbooks. | 2026-06-24 | 2026-07-31 | ⭐ 1,191 |
| [HostHunter](https://github.com/SpiderLabs/HostHunter) | Python | IP Address | Discovers hostnames associated with supplied IP addresses. | 2018-05-17 | 2023-03-30 | ⭐ 1,169 |
| [asnmap](https://github.com/projectdiscovery/asnmap) | Go | IP Address; CIDR; ASN | Maps organizations and ASNs to their advertised network ranges. | 2022-09-29 | 2026-05-19 | ⭐ 1,119 |
| [dnsgen](https://github.com/AlephNullSK/dnsgen) | Python | Domain | Generates likely DNS name permutations for further discovery. | 2019-09-24 | 2025-01-03 | ⭐ 1,076 |
| [openSquat](https://github.com/atenreiro/opensquat) | Python | Domain | Detects newly registered look-alike domains associated with brands. | 2020-05-04 | 2026-07-27 | ⭐ 983 |
| [subscraper](https://github.com/m8sec/subscraper) | Python | Domain | Enumerates subdomains and related targets from public sources. | 2018-09-27 | 2024-06-19 | ⭐ 973 |
| [Subdominator](https://github.com/RevoltSecurities/Subdominator) | Python | Domain | Performs low-impact subdomain discovery across multiple sources. | 2023-07-24 | 2026-06-21 | ⭐ 804 |
| [Cyberbro](https://github.com/stanfrbd/cyberbro) | Python | Domain; IP Address; URL | Extracts observables from unstructured input and checks them across CTI services. | 2024-10-31 | 2026-08-10 | ⭐ 684 |
| [CloudRip](https://github.com/moscovium-mc/CloudRip) | Python | Domain; IP Address | Looks for origin IP addresses hidden behind Cloudflare. | 2024-10-12 | 2026-07-06 | ⭐ 644 |
| [Transilience Community Tools](https://github.com/transilienceai/communitytools) | Skills + agents | Domain; IP Address; URL | Covers security reconnaissance, bug bounty, AI threat testing, validation, and reporting. | 2025-11-21 | 2026-07-29 | ⭐ 482 |
| <img src=".github/assets/new-dot.svg" width="6" height="6" alt=""> [TORCH](https://github.com/Encod3d-Sec/TORCH) | Skill library + MCP | Domain; IP Address; URL | Provides Claude Code with reconnaissance and authorized security-testing workflows, a searchable technique library, persistent engagement state, and MCP retrieval. | 2026-07-14 | 2026-08-20 | ⭐ 278 |
| [netscout](https://github.com/caio-ishikawa/netscout) | Go | Domain; URL | Crawls from a seed URL to find domains, paths, endpoints, and files. | 2024-03-28 | 2024-04-05 | ⭐ 182 |
| [pygreynoise](https://github.com/GreyNoise-Intelligence/pygreynoise) | Python | IP Address | Queries GreyNoise observations and classifications for internet-scanning IPs. | 2017-12-07 | 2026-07-09 | ⭐ 177 |
| [ThreatSwarm](https://github.com/mukul975/Threatswarm) | Plugin + agents | Domain; IP Address; URL | Coordinates scope-aware agents across recon, exploitation, DFIR, and final reporting. | 2026-04-29 | 2026-04-29 | ⭐ 72 |
| [OSINT AI](https://github.com/dkyazzentwatwa/osint-ai) | Skill pack | Name; Organization Name; Domain | Provides guided people, domain, organization, breach, and evidence-analysis workflows. | 2026-02-27 | 2026-03-07 | ⭐ 52 |
| [MCP dnstwist](https://github.com/w0h1v/mcp-dnstwist) | MCP server | Domain | Exposes look-alike domain discovery for phishing and impersonation investigations. | 2024-12-19 | 2025-03-03 | ⭐ 51 |
| [OSINT MCP Server](https://github.com/badchars/osint-mcp-server) | MCP server | Domain; IP Address; URL | Correlates infrastructure and threat data from Shodan, Censys, DNS, BGP, archives, and more. | 2026-03-17 | 2026-03-17 | ⭐ 46 |
| [Ronin Recon](https://github.com/ronin-rb/ronin-recon) | Ruby | Domain; URL | Provides a modular reconnaissance framework and command-line interface. | 2023-04-11 | 2026-01-15 | ⭐ 42 |
| [Claude Code Pentest](https://github.com/Orizon-eu/claude-code-pentest) | Skill pack | Domain; IP Address; URL | Automates the authorized pentest lifecycle from initial recon to exploit-chain reports. | 2026-03-11 | 2026-03-11 | ⭐ 24 |
| [Shodan MCP by Vorota](https://github.com/Vorota-ai/shodan-mcp) | MCP server | Domain; IP Address | Adds passive asset discovery, DNS analysis, and vulnerability intelligence from Shodan. | 2026-02-12 | 2026-02-12 | ⭐ 22 |
| [Recon](https://github.com/g-baskin/recon) | Skill | Organization Name; Domain; URL | Performs competitive intelligence across products, infrastructure, APIs, and communities. | 2026-02-25 | 2026-04-04 | ⭐ 6 |
| [Outrider Recon](https://github.com/Ap6pack/outrider-recon) | Skills + MCP | Domain; URL | Runs evidence-backed external reconnaissance with policy controls and optional MCP enrichment. | 2026-04-29 | 2026-07-15 | ⭐ 4 |
| [Offensive Recon](https://github.com/mahuttha/offensive-recon) | Plugin + skills | Domain; IP Address; URL | Packages multi-phase reconnaissance skills and agents around common security tools. | 2026-03-01 | 2026-03-01 | ⭐ 4 |
| [LeakIX MCP](https://github.com/LeakIX/leakix-mcp) | MCP server | Domain; IP Address; URL | Exposes LeakIX searches for internet services, leaks, domains, and IP addresses through MCP. | 2026-01-27 | 2026-08-22 | ⭐ 2 |
| [Bounty Recon Pro](https://github.com/synicalkid/bounty-recon-pro) | Skill | Domain; URL | Runs scoped passive OSINT and active bug-bounty recon with evidence-oriented reports. | 2026-07-11 | 2026-07-11 | ⭐ 0 |

<p align="right"><a href="#table-of-contents">Back to contents ↑</a></p>

<a id="web"></a>

## 🔗 Web <sup>77 projects</sup>

Tools that collect, search, analyze, crawl, or preserve public web content.

| Project | Type | Target Input | Description | Created | Last Update | Stars |
|:---|:---|:---|:---|:---:|:---:|---:|
| [Firecrawl](https://github.com/firecrawl/firecrawl) | TypeScript | URL | Provides APIs for web search, scraping, crawling, and structured extraction. | 2024-04-15 | 2026-08-23 | ⭐ 171,484 |
| [Browser Use](https://github.com/browser-use/browser-use) | Agent framework | URL | Lets AI agents navigate websites, interact with pages, and extract information. | 2024-10-31 | 2026-08-19 | ⭐ 110,290 |
| [Crawl4AI](https://github.com/unclecode/crawl4ai) | Python | URL | Crawls websites and produces structured, LLM-ready content and metadata. | 2024-05-09 | 2026-07-15 | ⭐ 79,271 |
| [Scrapling](https://github.com/D4Vinci/Scrapling) | Python | URL | Provides adaptive web scraping, crawling, browser automation, and structured extraction. | 2024-10-13 | 2026-08-23 | ⭐ 76,162 |
| [Scrapy](https://github.com/scrapy/scrapy) | Python | URL | Implements a mature Python framework for crawling and extracting structured web data. | 2010-02-22 | 2026-08-23 | ⭐ 64,008 |
| [TrendRadar](https://github.com/sansan0/TrendRadar) | Monitoring platform + MCP | URL | Monitors news and RSS sources, tracks trends, stores history, and exposes MCP access. | 2025-04-28 | 2026-07-17 | ⭐ 61,697 |
| [EasySpider](https://github.com/NaiboWang/EasySpider) | JavaScript | URL | Creates and runs visual no-code web crawling and data extraction tasks. | 2020-07-18 | 2026-08-19 | ⭐ 44,404 |
| [Vane](https://github.com/ItzCrazyKns/Vane) | Research agent | URL | Provides a self-hosted research interface that answers questions with linked sources. | 2024-04-09 | 2026-04-11 | ⭐ 36,422 |
| [SearXNG](https://github.com/searxng/searxng) | Python | URL | Aggregates results from multiple search services in a self-hosted metasearch engine. | 2021-04-12 | 2026-08-22 | ⭐ 36,007 |
| [Web-Check](https://github.com/lissy93/web-check) | TypeScript | URL | Produces a broad technical and open-source intelligence report for a website. | 2023-06-25 | 2026-08-11 | ⭐ 34,583 |
| [changedetection.io](https://github.com/dgtlmoon/changedetection.io) | Python | URL | Monitors web pages and records content changes over time. | 2021-01-27 | 2026-08-20 | ⭐ 33,316 |
| [ScrapeGraphAI](https://github.com/ScrapeGraphAI/Scrapegraph-ai) | Python | URL | Builds scraping pipelines that use language models to extract structured information. | 2024-01-27 | 2026-08-23 | ⭐ 29,848 |
| [GPT Researcher](https://github.com/assafelovic/gpt-researcher) | Research agent | URL | Runs multi-agent web research and produces source-grounded reports with citations. | 2023-05-12 | 2026-08-23 | ⭐ 29,115 |
| [ArchiveBox](https://github.com/ArchiveBox/ArchiveBox) | Python | URL | Creates self-hosted, durable archives of web pages and linked online material. | 2017-05-05 | 2026-08-19 | ⭐ 28,165 |
| [Crawlee](https://github.com/apify/crawlee) | TypeScript | URL | Provides a scalable SDK for HTTP crawling and browser automation. | 2016-08-26 | 2026-08-21 | ⭐ 25,480 |
| [Stagehand](https://github.com/browserbase/stagehand) | Agent SDK | URL | Provides an SDK for agent-driven browser automation and page extraction. | 2024-03-24 | 2026-08-21 | ⭐ 24,030 |
| [SingleFile](https://github.com/gildas-lormeau/SingleFile) | JavaScript | URL | Saves a complete web page as one file for preservation and later analysis. | 2010-09-12 | 2026-08-05 | ⭐ 22,227 |
| [deep-research](https://github.com/dzhng/deep-research) | Research agent | URL | Runs iterative web searches, evaluates findings, and builds source-grounded research answers. | 2025-02-04 | 2026-04-11 | ⭐ 19,589 |
| [Linkwarden](https://github.com/linkwarden/linkwarden) | TypeScript | URL | Preserves bookmarked pages and stored copies for later reference and collaboration. | 2022-04-09 | 2026-08-17 | ⭐ 19,573 |
| [Maxun](https://github.com/getmaxun/maxun) | TypeScript | URL | Builds reusable web robots and structured data APIs through a visual interface. | 2023-10-23 | 2026-08-23 | ⭐ 17,274 |
| [Photon](https://github.com/s0md3v/Photon) | Python | URL | Crawls a supplied URL to collect links and related open-source data. | 2018-03-30 | 2026-08-07 | ⭐ 13,135 |
| [httpx](https://github.com/projectdiscovery/httpx) | Go | URL | Probes web targets at scale and reports HTTP, TLS, technology, and response metadata. | 2020-05-28 | 2026-08-12 | ⭐ 10,314 |
| [Steel Browser](https://github.com/steel-dev/steel-browser) | TypeScript | URL | Runs a self-hosted browser API and sandbox for automated web operations. | 2024-11-01 | 2026-07-20 | ⭐ 7,533 |
| [Firecrawl MCP Server](https://github.com/firecrawl/firecrawl-mcp-server) | MCP server | URL | Gives agents web search, crawling, scraping, extraction, and structured research tools. | 2024-12-06 | 2026-08-21 | ⭐ 7,307 |
| [Trafilatura](https://github.com/adbar/trafilatura) | Python | URL | Extracts main text, metadata, links, and document structure from web pages. | 2019-04-08 | 2026-08-21 | ⭐ 6,691 |
| [hakrawler](https://github.com/hakluke/hakrawler) | Go | URL | Crawls web applications to discover endpoints, assets, and linked resources. | 2019-12-15 | 2026-08-05 | ⭐ 5,114 |
| [Exa MCP Server](https://github.com/exa-labs/exa-mcp-server) | MCP server | URL | Provides semantic web search, content retrieval, and research discovery through Exa. | 2024-11-27 | 2026-08-21 | ⭐ 4,917 |
| [Apify MCP Server](https://github.com/apify/apify-mcp-server) | MCP server | URL | Makes Apify Actors and public web data collection available to compatible agents. | 2025-01-02 | 2026-08-21 | ⭐ 4,728 |
| [Deep Research](https://github.com/u14app/deep-research) | Research system + MCP | URL | Runs iterative web research and synthesis with configurable models and MCP access. | 2025-02-22 | 2026-06-18 | ⭐ 4,684 |
| [Cariddi](https://github.com/edoardottt/cariddi) | Go | URL | Crawls domains and extracts endpoints, secrets, tokens, and file references. | 2021-04-27 | 2026-07-15 | ⭐ 3,752 |
| [pagodo](https://github.com/opsdisk/pagodo) | Python | URL | Automates Google dork collection and searches against a target. | 2016-08-19 | 2025-08-30 | ⭐ 3,387 |
| [waybackpack](https://github.com/jsvine/waybackpack) | Python | URL | Downloads archived versions of a URL from the Wayback Machine. | 2016-04-11 | 2025-04-21 | ⭐ 3,229 |
| [ParamSpider](https://github.com/devanshbatham/ParamSpider) | Python | URL | Mines web archives for URLs containing useful parameters. | 2020-04-12 | 2026-03-07 | ⭐ 3,159 |
| [waymore](https://github.com/xnl-h4ck3r/waymore) | Python | URL | Collects archived URLs and responses from several public sources. | 2022-06-24 | 2026-06-11 | ⭐ 2,728 |
| [Bright Data MCP](https://github.com/brightdata/brightdata-mcp) | MCP server | URL | Connects agents to search, browsing, scraping, and public web datasets. | 2025-04-15 | 2026-08-12 | ⭐ 2,611 |
| [Tavily MCP](https://github.com/tavily-ai/tavily-mcp) | MCP server | URL | Exposes search, extraction, crawling, mapping, and research functions from Tavily. | 2025-01-27 | 2026-08-20 | ⭐ 2,349 |
| [Mitaka](https://github.com/ninoseki/mitaka) | TypeScript | URL | Adds browser searches for URLs, hashes, IP addresses, and other indicators. | 2018-02-09 | 2026-08-02 | ⭐ 1,843 |
| [BlackWidow](https://github.com/1N3/BlackWidow) | Python | URL | Crawls a web application to collect intelligence and identify reachable paths. | 2018-01-06 | 2026-04-17 | ⭐ 1,821 |
| [urlhunter](https://github.com/utkusen/urlhunter) | Go | URL | Finds URLs exposed through public URL-shortening services. | 2020-11-21 | 2025-01-23 | ⭐ 1,697 |
| [pywb](https://github.com/webrecorder/pywb) | Python | URL | Indexes, serves, and replays WARC web archives. | 2013-12-09 | 2026-04-10 | ⭐ 1,691 |
| [GooFuzz](https://github.com/m3n0sd0n4ld/GooFuzz) | Shell | URL | Uses search-engine results to enumerate web paths, files, and parameters. | 2022-06-17 | 2025-12-21 | ⭐ 1,585 |
| [ArchiveWeb.page](https://github.com/webrecorder/archiveweb.page) | TypeScript | URL | Captures selected web pages and browsing sessions into portable web archives. | 2020-02-10 | 2026-08-12 | ⭐ 1,553 |
| [Brave Search MCP Server](https://github.com/brave/brave-search-mcp-server) | MCP server | URL | Adds Brave web, news, image, video, and local search to MCP clients. | 2025-06-12 | 2026-08-20 | ⭐ 1,397 |
| [FavFreak](https://github.com/devanshbatham/FavFreak) | Python | URL | Creates favicon hashes for finding related websites through internet search engines. | 2020-07-03 | 2023-08-29 | ⭐ 1,298 |
| [Browsertrix Crawler](https://github.com/webrecorder/browsertrix-crawler) | TypeScript | URL | Captures interactive websites as WARC and WACZ archives with replay quality checks. | 2020-11-02 | 2026-08-20 | ⭐ 1,117 |
| [Bellingcat Auto Archiver](https://github.com/bellingcat/auto-archiver) | Python | URL | Archives web pages, social posts, images, and videos from queued URLs. | 2021-01-15 | 2026-08-18 | ⭐ 1,109 |
| [ReplayWeb.page](https://github.com/webrecorder/replayweb.page) | TypeScript | URL | Replays WARC and WACZ web archives locally in a browser. | 2019-12-09 | 2026-08-11 | ⭐ 972 |
| [urlfinder](https://github.com/projectdiscovery/urlfinder) | Go | URL | Passively collects URLs associated with a target. | 2024-04-30 | 2026-08-05 | ⭐ 901 |
| [xurlfind3r](https://github.com/hueristiq/xurlfind3r) | Go | URL | Discovers URLs for a domain through passive public sources. | 2021-05-13 | 2025-11-17 | ⭐ 719 |
| [waybackpy](https://github.com/akamhy/waybackpy) | Python | URL | Provides a command-line and library interface to Wayback Machine APIs. | 2020-05-02 | 2022-11-17 | ⭐ 603 |
| [Browsertrix](https://github.com/webrecorder/browsertrix) | TypeScript | URL | Provides a collaborative platform for browser-based web archiving and replay. | 2021-06-28 | 2026-08-22 | ⭐ 461 |
| [NotebookLM Skill](https://github.com/claude-world/notebooklm-skill) | Skill + MCP | URL | Uses NotebookLM for source-grounded research, synthesis, and content preparation. | 2026-03-13 | 2026-07-18 | ⭐ 435 |
| [De-Anthropocentric Research Engine](https://github.com/yogsoth-ai/de-anthropocentric-research-engine) | Research skill system | URL | Organizes autonomous research into composable campaigns, strategies, tactics, and procedures. | 2026-02-10 | 2026-08-15 | ⭐ 379 |
| [Kindly Web Search MCP](https://github.com/Shelpuk-AI-Technology-Consulting/kindly-web-search-mcp-server) | MCP server | URL | Aggregates web search, extraction, crawling, and browser automation for many clients. | 2026-01-02 | 2026-07-29 | ⭐ 377 |
| [TheScrapper](https://github.com/champmq/TheScrapper) | Python | URL | Crawls websites to extract email addresses, phone numbers, and social profile links. | 2021-05-07 | 2026-05-29 | ⭐ 369 |
| [MCP Omnisearch](https://github.com/spences10/mcp-omnisearch) | MCP server | URL | Combines multiple search, AI search, and content-processing providers behind MCP. | 2025-03-08 | 2026-08-21 | ⭐ 344 |
| [Google Research MCP](https://github.com/mixelpixx/Nimrod) | MCP server | URL | Uses Google Search and browser automation for multi-step cited research. | 2024-12-19 | 2026-08-14 | ⭐ 253 |
| <img src=".github/assets/new-dot.svg" width="6" height="6" alt=""> [agent-pulse](https://github.com/barretlee/agent-pulse) | TypeScript | URL; Document | Turns public AI releases, research, policy, funding, and propagation signals into source-linked events and evolving assessments. | 2026-07-11 | 2026-08-23 | ⭐ 235 |
| [urx](https://github.com/hahwul/urx) | Rust | URL | Extracts URLs from public web archives for later analysis. | 2025-03-28 | 2026-08-21 | ⭐ 190 |
| <img src=".github/assets/new-dot.svg" width="6" height="6" alt=""> [WebCheck-OSINT](https://github.com/mwakidenis/WebCheck-OSINT) | TypeScript | Domain; URL | Collects and presents public DNS, TLS, headers, hosting, network, technology, security, and performance data for a website. | 2025-12-14 | 2026-08-24 | ⭐ 165 |
| [Octagon MCP Server](https://github.com/OctagonAI/octagon-mcp-server) | MCP server | URL | Provides public company, market, investor, private-market, and crypto research data. | 2025-03-12 | 2026-07-09 | ⭐ 147 |
| [RivalSearch MCP](https://github.com/damionrashford/RivalSearchMCP) | MCP server | URL | Unifies web, social, news, academic, and entity-search sources behind MCP. | 2025-08-03 | 2026-05-31 | ⭐ 122 |
| [Deep Research MCP](https://github.com/pminervini/deep-research-mcp) | MCP server | URL | Connects several deep-research agents and model providers through one MCP interface. | 2025-08-07 | 2026-08-05 | ⭐ 103 |
| [Deep Web Research MCP](https://github.com/qpd-v/mcp-DEEPwebresearch) | MCP server | URL | Coordinates recursive web search and page analysis for deeper topic coverage. | 2025-01-13 | 2025-03-05 | ⭐ 86 |
| [Agent Search](https://github.com/brcrusoe72/agent-search) | MCP server | URL | Provides privacy-oriented search and browser retrieval for AI agents. | 2026-02-18 | 2026-07-07 | ⭐ 74 |
| [OpenRouter Deep Research MCP](https://github.com/wheattoast11/openrouter-deep-research-mcp) | MCP server | URL | Orchestrates parallel research agents and consensus-backed synthesis through OpenRouter. | 2025-03-28 | 2026-03-04 | ⭐ 55 |
| [Web Researcher MCP](https://github.com/zoharbabin/web-researcher-mcp) | MCP server | URL | Searches the web, extracts sources, and produces citation-aware research results. | 2026-05-18 | 2026-08-20 | ⭐ 52 |
| [AtDork](https://github.com/amnottdevv/AtDork) | Python | URL | Automates multi-engine search queries with rate and failure controls. | 2026-06-07 | 2026-08-24 | ⭐ 37 |
| [Wayback Archive](https://github.com/GeiserX/Wayback-Archive) | Python | URL | Downloads complete archived websites with their referenced assets. | 2025-12-11 | 2026-08-20 | ⭐ 29 |
| [GiaSip Skills](https://github.com/GiaSip/giasip-skills) | Skills + plugin | URL | Provides quick recon, fact-checking, research orchestration, and multi-model dispatch. | 2026-05-30 | 2026-08-22 | ⭐ 12 |
| [Web Multi Search](https://github.com/soxoj/web-multi-search-skill) | Skill + script | URL | Searches several web engines in parallel and exports deduplicated results. | 2026-02-08 | 2026-02-08 | ⭐ 8 |
| [Digital Research Skills](https://github.com/smarks26/digital-research-skills) | Research skill system | URL | Plans evidence-driven research waves for OSINT, due diligence, trends, and long-form analysis. | 2026-05-29 | 2026-05-16 | ⭐ 3 |
| [Memorious4](https://github.com/dataresearchcenter/memorious) | Python | URL | Runs maintained configurable crawlers for investigative documents and structured public data. | 2025-01-21 | 2026-08-22 | ⭐ 3 |
| [Internet Archive MCP](https://github.com/cyanheads/internet-archive-mcp-server) | MCP server | URL | Provides agent access to Internet Archive search, metadata, files, and preserved resources. | 2026-06-05 | 2026-08-21 | ⭐ 2 |
| [Wayback Diff](https://github.com/GeiserX/Wayback-Diff) | Python | URL | Compares current and archived web pages for content and visual changes. | 2025-12-13 | 2026-08-17 | ⭐ 1 |
| [Agent Toolkit](https://github.com/000001000000/agent-toolkit) | Skill pack | URL | Includes an OSINT dorking workflow with search tooling and evaluation assets. | 2026-04-11 | 2026-06-08 | ⭐ 1 |
| <img src=".github/assets/new-dot.svg" width="6" height="6" alt=""> [monster-search](https://github.com/scaso01/monster-search) | Python | Keyword; URL; Domain; IP Address; CVE ID | Federates web, code, archive, news, WHOIS, security, and research search engines into one ranked result set. | 2026-07-31 | 2026-08-23 | ⭐ 0 |

<p align="right"><a href="#table-of-contents">Back to contents ↑</a></p>

<a id="dark-web"></a>

## 🧅 Dark Web <sup>15 projects</sup>

Tools for discovering, collecting, and analyzing onion services and dark-web content.

| Project | Type | Target Input | Description | Created | Last Update | Stars |
|:---|:---|:---|:---|:---:|:---:|---:|
| [Robin](https://github.com/apurvsinghgautam/robin) | Python | Onion Service | Refines queries, filters dark-web search results, and saves assisted investigation summaries. | 2025-04-08 | 2026-08-07 | ⭐ 6,396 |
| [TorBot](https://github.com/DedSecInside/TorBot) | Python | URL; Onion Service | Crawls a known onion service and exports its link tree for structure mapping. | 2017-05-17 | 2026-07-28 | ⭐ 4,685 |
| [darkdump](https://github.com/josh0xA/darkdump) | Python | Onion Service | Runs first-pass keyword discovery across dark-web search engines and saves result sets for later review. | 2021-02-11 | 2026-04-08 | ⭐ 1,752 |
| [AIL Framework](https://github.com/ail-project/ail-framework) | Python | Onion Service | Collects, crawls, processes, correlates, and analyzes unstructured information from Tor and other sources. | 2020-04-20 | 2026-08-17 | ⭐ 999 |
| [Ahmia](https://github.com/ahmia/ahmia-site) | Python | Onion Service | Provides an open-source search application and interface for indexed onion services. | 2016-05-23 | 2026-08-21 | ⭐ 761 |
| [Darkus](https://github.com/Lucksi/Darkus) | Python | Onion Service | Queries multiple onion search engines for keyword-matched hidden services. | 2023-10-27 | 2026-02-21 | ⭐ 690 |
| [VoidAccess](https://github.com/KatrielMoses/voidaccess) | Python | Onion Service | Runs a self-hosted pipeline for dark-web collection, extraction, correlation, and graph analysis. | 2026-04-29 | 2026-08-04 | ⭐ 648 |
| [Darknet MCP Server](https://github.com/badchars/darknet-mcp-server) | MCP server | Onion Service | Unifies dark-web search, breach, ransomware, malware, and blockchain intelligence tools for MCP clients. | 2026-06-23 | 2026-06-24 | ⭐ 312 |
| [darc](https://github.com/JarryShaw/darc) | Python | Onion Service | Crawls dark-web services, stores link and host data, and supports distributed collection workflows. | 2019-09-28 | 2026-08-22 | ⭐ 227 |
| [onion-lookup](https://github.com/ail-project/onion-lookup) | Python | Onion Service | Checks onion-service availability and retrieves associated metadata from an AIL instance. | 2024-10-03 | 2026-01-05 | ⭐ 66 |
| [OnionClaw](https://github.com/JacobJandon/OnionClaw) | Skill + CLI | Onion Service | Adds Tor search, hidden-service retrieval, crawling, and export workflows to OpenClaw. | 2026-03-14 | 2026-05-28 | ⭐ 64 |
| [DarkSpider](https://github.com/PROxZIMA/DarkSpider) | Python | Onion Service | Crawls onion services through Tor and visualizes extracted link relationships. | 2022-07-31 | 2024-07-27 | ⭐ 45 |
| [Sicry](https://github.com/JacobJandon/Sicry) | Python + MCP | Onion Service | Checks Tor health, rotates identity, searches onion engines, fetches known services, and exposes optional agent-assisted analysis. | 2026-03-14 | 2026-05-28 | ⭐ 19 |
| [PyAhmia](https://github.com/rly0nheart/pyahmia) | Python | Onion Service | Provides programmatic search access to Ahmia-indexed Tor hidden services. | 2025-09-26 | 2026-07-17 | ⭐ 17 |
| [LeakRecon](https://github.com/egnake/LeakRecon) | Python | Onion Service | Runs Tor-routed leak reconnaissance with local history, change tracking, and report export. | 2026-05-18 | 2026-06-04 | ⭐ 11 |

<p align="right"><a href="#table-of-contents">Back to contents ↑</a></p>

<a id="threat-intelligence"></a>

## 🛡️ Threat Intelligence <sup>21 projects</sup>

Tools for threat data, indicators, file hashes, vulnerabilities, and malware analysis.

| Project | Type | Target Input | Description | Created | Last Update | Stars |
|:---|:---|:---|:---|:---:|:---:|---:|
| [Crucix](https://github.com/calesthio/Crucix) | JavaScript | Domain; IP Address; URL; File Hash | Watches multiple public intelligence sources and reports relevant changes. | 2026-03-14 | 2026-05-20 | ⭐ 11,543 |
| [OpenCTI](https://github.com/OpenCTI-Platform/opencti) | TypeScript | Domain; IP Address; URL; File Hash | Organizes cyber threat intelligence in a graph-based analysis platform. | 2018-12-17 | 2026-08-23 | ⭐ 9,841 |
| [MISP](https://github.com/MISP/MISP) | PHP | Domain; IP Address; URL; File Hash | Stores, correlates, analyzes, and shares structured threat intelligence and indicators. | 2013-02-07 | 2026-08-13 | ⭐ 6,485 |
| [gau](https://github.com/lc/gau) | Go | URL | Collects known URLs from public archives and threat intelligence sources. | 2020-02-25 | 2026-03-20 | ⭐ 5,071 |
| [IntelOwl](https://github.com/intelowlproject/IntelOwl) | Python | Domain; IP Address; URL; File Hash | Orchestrates threat intelligence analyzers and connectors at scale. | 2019-12-31 | 2026-07-02 | ⭐ 4,680 |
| [Watcher](https://github.com/thalesgroup-cert/Watcher) | JavaScript | Domain; IP Address; URL; File Hash | Collects, enriches, and searches cyber threat intelligence with assisted analysis. | 2020-09-01 | 2026-07-22 | ⭐ 1,370 |
| [Harpoon](https://github.com/Te-k/harpoon) | Python | IP Address | Provides command-line queries for open-source and threat intelligence indicators. | 2017-09-25 | 2026-05-18 | ⭐ 1,289 |
| [Taranis AI](https://github.com/taranis-ai/taranis-ai) | Python | Domain; IP Address; URL; File Hash | Collects and analyzes open-source information for situational awareness. | 2023-10-05 | 2026-08-21 | ⭐ 1,203 |
| [CVE MCP Server](https://github.com/mukul975/cve-mcp-server) | MCP server | CVE ID | Correlates CVE, EPSS, KEV, Shodan, VirusTotal, and related security intelligence. | 2026-04-14 | 2026-06-22 | ⭐ 1,151 |
| [Mihari](https://github.com/ninoseki/mihari) | Ruby | Domain; IP Address; URL; File Hash | Aggregates search queries across threat intelligence services. | 2019-04-15 | 2026-07-04 | ⭐ 941 |
| [ThreatIngestor](https://github.com/pedramamini/ThreatIngestor) | Python | Domain; IP Address; URL; File Hash | Extracts and routes threat indicators from public information feeds. | 2017-08-31 | 2026-05-26 | ⭐ 924 |
| [MCP Security Hub](https://github.com/FuzzingLabs/mcp-security-hub) | MCP collection | Domain; IP Address; URL; File; File Hash | Exposes containerized security tools for recon, threat intelligence, code, and binary analysis. | 2026-01-06 | 2026-04-08 | ⭐ 766 |
| [CTI Expert](https://github.com/7onez/cti-expert) | Skill | Domain; IP Address; URL; File Hash | Guides structured cyber threat intelligence and OSINT collection with confidence scoring. | 2026-04-06 | 2026-08-23 | ⭐ 547 |
| [Reversecore MCP](https://github.com/sjkim1127/Reversecore_MCP) | MCP server | File; File Hash | Connects agents to reverse engineering, malware, forensics, and vulnerability research tools. | 2025-11-10 | 2026-08-23 | ⭐ 188 |
| [Shodan MCP](https://github.com/w0h1v/mcp-shodan) | MCP server | Domain; IP Address | Provides device search, IP reconnaissance, DNS, CPE, and CVE intelligence. | 2024-12-12 | 2026-03-31 | ⭐ 157 |
| [VirusTotal MCP](https://github.com/w0h1v/mcp-virustotal) | MCP server | Domain; IP Address; URL; File; File Hash | Queries files, URLs, domains, IPs, and related security-analysis records. | 2024-12-13 | 2026-05-24 | ⭐ 147 |
| [MalwareDB](https://github.com/malwaredb/malwaredb-rs) | Rust | File; File Hash | Stores, indexes, and analyzes malware samples and associated metadata. | 2023-02-19 | 2026-08-24 | ⭐ 60 |
| [ZettelForge](https://github.com/ThreatRecall/zettelforge) | CTI system + MCP | Domain; IP Address; URL; File Hash | Extracts IOCs and threat entities into a local STIX knowledge graph with agent access. | 2026-04-06 | 2026-07-10 | ⭐ 58 |
| [Malware Sandbox MCP](https://github.com/mukul975/Malware-Sandbox-mcp) | MCP server | File; File Hash | Normalizes malware sandbox verdicts, IOCs, artifacts, and ATT&CK mappings. | 2026-06-11 | 2026-06-11 | ⭐ 23 |
| [MISP MCP](https://github.com/MISP/misp-mcp) | MCP server | Domain; IP Address; URL; File Hash | Provides read-only access to MISP threat intelligence events and attributes. | 2026-04-01 | 2026-04-05 | ⭐ 9 |
| [OSINT MCP Gateway](https://github.com/bonetrees/osint-mcp-gateway) | MCP server | Domain; IP Address; URL | Routes agent queries across VirusTotal, Shodan, DNS, WHOIS, RIPEstat, and OTX. | 2025-11-23 | 2026-06-10 | ⭐ 0 |

<p align="right"><a href="#table-of-contents">Back to contents ↑</a></p>

<a id="documents-records"></a>

## 📄 Documents & Records <sup>44 projects</sup>

Tools for documents, files, datasets, public records, extraction, and structured review.

| Project | Type | Target Input | Description | Created | Last Update | Stars |
|:---|:---|:---|:---|:---:|:---:|---:|
| [MarkItDown](https://github.com/microsoft/markitdown) | Python | Document | Converts common document and media formats into Markdown for analysis. | 2024-11-13 | 2026-08-19 | ⭐ 175,826 |
| [Docling](https://github.com/docling-project/docling) | Python | Document | Parses PDFs, office files, HTML, images, and audio into structured document representations. | 2024-07-09 | 2026-08-21 | ⭐ 65,453 |
| [Marker](https://github.com/datalab-to/marker) | Python | Document | Converts PDFs and other documents into Markdown, JSON, tables, and structured text. | 2023-10-30 | 2026-08-07 | ⭐ 39,105 |
| [OCRmyPDF](https://github.com/ocrmypdf/OCRmyPDF) | Python | Document | Adds searchable OCR text layers to scanned PDF documents. | 2013-12-20 | 2026-08-21 | ⭐ 34,552 |
| [Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills) | Skill library | Document; Dataset | Provides reusable scientific research workflows and access patterns for public databases. | 2025-10-19 | 2026-08-19 | ⭐ 34,201 |
| [OpenDataLoader PDF](https://github.com/opendataloader-project/opendataloader-pdf) | Java | Document | Extracts text, tables, layout, and structured content from PDF documents. | 2025-05-13 | 2026-08-24 | ⭐ 28,665 |
| [notebooklm-py](https://github.com/teng-lin/notebooklm-py) | Library + skill + MCP | Document | Gives agents programmatic, source-grounded access to NotebookLM research workflows. | 2026-01-07 | 2026-08-17 | ⭐ 18,889 |
| [Unstructured](https://github.com/Unstructured-IO/unstructured) | Python | Document | Normalizes documents and extracts elements for search, analytics, and RAG pipelines. | 2022-09-26 | 2026-08-21 | ⭐ 15,339 |
| [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) | Research skill system | Document | Orchestrates long-running research, cross-model review, experiments, and evidence capture. | 2026-03-10 | 2026-08-21 | ⭐ 15,061 |
| [OpenRefine](https://github.com/OpenRefine/OpenRefine) | Java | Dataset | Cleans, transforms, reconciles, and links inconsistent structured data. | 2012-10-15 | 2026-08-16 | ⭐ 11,951 |
| [NotebookLM CLI and MCP](https://github.com/jacob-bd/gemini-notebook-mcp-cli) | CLI + skill + MCP | Document | Connects AI agents to NotebookLM for cited source ingestion, querying, and synthesis. | 2025-12-23 | 2026-08-20 | ⭐ 5,925 |
| [Apache Tika](https://github.com/apache/tika) | Java | Document | Detects file types and extracts text and metadata from many document formats. | 2009-05-21 | 2026-08-24 | ⭐ 4,001 |
| [GLiNER](https://github.com/urchade/GLiNER) | Python | Text | Recognizes user-defined entity types in unstructured text without task-specific retraining. | 2023-11-14 | 2026-08-10 | ⭐ 3,567 |
| [Aleph](https://github.com/alephdata/aleph) | JavaScript | Organization Name | Lets investigators search documents and structured data for people and companies. | 2014-08-27 | 2025-12-19 | ⭐ 2,417 |
| [Splink](https://github.com/moj-analytical-services/splink) | Python | Name; Organization Name; Dataset | Performs probabilistic entity resolution and deduplication across imperfect records. | 2019-11-22 | 2026-08-20 | ⭐ 2,355 |
| [cloud_enum](https://github.com/initstring/cloud_enum) | Python | Organization Name | Enumerates public cloud resources associated with organization keywords. | 2019-05-31 | 2026-07-09 | ⭐ 2,131 |
| [Agentset](https://github.com/agentset-ai/agentset) | Research system + MCP | Document | Provides document ingestion, agentic search, ranking, citations, RAG, and MCP access. | 2025-03-10 | 2026-07-04 | ⭐ 2,068 |
| [Open Semantic Search](https://github.com/opensemanticsearch/open-semantic-search) | Shell | Document | Searches, extracts, and links entities across large document collections. | 2016-03-30 | 2025-04-19 | ⭐ 1,201 |
| [PDF Reader MCP](https://github.com/SylphxAI/pdf-reader-mcp) | MCP server + CLI | Document | Analyzes PDFs through MCP while retaining page references, visual crops, and OCR provenance. | 2025-04-04 | 2026-08-19 | ⭐ 899 |
| [emploleaks](https://github.com/infobyte/emploleaks) | Python | Organization Name | Identifies company employees appearing in credential leak data. | 2023-04-21 | 2026-05-19 | ⭐ 788 |
| [OpenSanctions](https://github.com/opensanctions/opensanctions) | Python | Organization Name | Builds searchable data on sanctions, entities, and persons of interest. | 2015-12-05 | 2026-08-22 | ⭐ 787 |
| [ICIJ Datashare](https://github.com/ICIJ/datashare) | Java | Document | Indexes investigative documents, runs OCR, and extracts people, organizations, and locations. | 2016-04-20 | 2026-08-20 | ⭐ 752 |
| [Docling MCP](https://github.com/docling-project/docling-mcp) | MCP server | Document | Exposes document conversion and structured extraction from files and URLs through MCP. | 2025-03-14 | 2026-08-19 | ⭐ 714 |
| [ArkhamMirror](https://github.com/mantisfury/ArkhamMirror) | Python | Document | Provides local document intelligence, retrieval, and relationship analysis for investigations. | 2025-11-25 | 2026-01-25 | ⭐ 485 |
| [Claude Skills for Journalism](https://github.com/jamditis/claude-skills-journalism) | Skills + plugins | URL; Document | Covers source verification, public records, FOIA work, scraping, and newsroom research. | 2025-12-25 | 2026-08-21 | ⭐ 369 |
| [ICIJ Extract](https://github.com/ICIJ/extract) | Python | Document | Extracts searchable text and metadata from investigative document collections. | 2015-05-07 | 2026-08-20 | ⭐ 257 |
| [Simple PubMed MCP](https://github.com/andybrandt/mcp-simple-pubmed) | MCP server | Document | Searches PubMed and retrieves biomedical article metadata and abstracts. | 2024-12-11 | 2026-03-19 | ⭐ 171 |
| [mcp.science](https://github.com/pathintegral-institute/mcp.science) | MCP server | Document; Dataset | Connects agents to scientific literature search and research data services. | 2025-03-27 | 2025-09-02 | ⭐ 147 |
| [Data Commons Agent Toolkit](https://github.com/datacommonsorg/agent-toolkit) | MCP toolkit | Dataset | Connects agents and MCP clients to the public Data Commons knowledge graph. | 2025-06-26 | 2026-07-28 | ⭐ 138 |
| [Academia MCP](https://github.com/IlyaGusev/academia_mcp) | MCP server | Document | Searches academic sources and retrieves papers for agent-assisted literature research. | 2025-01-24 | 2026-01-24 | ⭐ 90 |
| [Bellingcat Sugartrail](https://github.com/bellingcat/sugartrail) | Python | Organization Name | Builds relationship graphs from UK companies, officers, and registered addresses. | 2022-09-04 | 2026-02-20 | ⭐ 79 |
| [ZotPilot](https://github.com/xunhe730/ZotPilot) | Skill + MCP | Document | Connects Zotero collections to source-grounded research and agent workflows. | 2026-03-16 | 2026-06-16 | ⭐ 70 |
| [DocumentCloud](https://github.com/MuckRock/documentcloud) | Python | Document | Provides the backend for uploading, processing, searching, and publishing source documents. | 2019-09-09 | 2026-08-19 | ⭐ 51 |
| [OpenAlex Research MCP](https://github.com/oksure/openalex-research-mcp) | MCP server | Document | Queries OpenAlex works, authors, institutions, concepts, and citation relationships. | 2025-10-05 | 2026-06-22 | ⭐ 45 |
| [European Parliament MCP](https://github.com/Hack23/European-Parliament-MCP-Server) | MCP server | Name; Document | Provides agent access to European Parliament members, committees, votes, documents, and questions. | 2026-02-16 | 2026-08-22 | ⭐ 25 |
| [Semantic Scholar Skills](https://github.com/zongmin-yu/semantic-scholar-skills) | Skills + MCP | Document | Supports literature discovery, citation expansion, and structured Semantic Scholar research. | 2026-03-10 | 2026-03-16 | ⭐ 20 |
| [Newsroom Extension](https://github.com/ehurrn/newsroom-extension) | Skill pack | Organization Name; Document | Supports investigative journalism, FOIA work, corporate research, verification, and editorial review. | 2026-04-06 | 2026-06-22 | ⭐ 7 |
| [Hermes OSINT Skill](https://github.com/mtjikuzu/hermes-osint-skill) | Skill | Name; Organization Name | Structures company due diligence, background checks, vendor risk, and privacy review. | 2026-05-22 | 2026-05-22 | ⭐ 7 |
| [Infringement Information Collector](https://github.com/11murmur/infringement-information-collector) | Skill | Organization Name; URL | Collects public leads about counterfeits, private servers, and piracy into auditable reports. | 2026-05-31 | 2026-06-01 | ⭐ 2 |
| [OpenProbe](https://github.com/hxd0818/openprobe) | Skill | Name; Organization Name | Investigates companies, competitors, supply chains, capital links, and key people. | 2026-04-12 | 2026-05-08 | ⭐ 2 |
| [Company Recon Skill](https://github.com/zoharbabin/company-recon-skill) | Skill | Organization Name; URL | Identifies websites using a company's technology and classifies the resulting evidence. | 2026-03-04 | 2026-03-04 | ⭐ 2 |
| [Scout](https://github.com/indigokarasu/scout) | Skill pack | Name; Organization Name | Structures lawful people and company research with provenance, source tiers, and refresh workflows. | 2026-03-10 | 2026-08-23 | ⭐ 1 |
| [openParlData.ch Web Archive](https://gitlab.com/opendata.ch/openparldatach/web-archive) | Web archive pipeline | URL | Archives Swiss parliamentary websites with Browsertrix and serves them through pywb. | 2026-04-02 | 2026-05-04 | ⭐ 0 |
| [ConsentTheater Playbill](https://codeberg.org/ConsentTheater/playbill) | TypeScript | Organization Name; URL | Maintains a queryable knowledge base of trackers, cookies, domains, and responsible companies. | 2026-05-31 | 2026-07-15 | ⭐ 0 |

<p align="right"><a href="#table-of-contents">Back to contents ↑</a></p>

<a id="media"></a>

## 🖼️ Media <sup>46 projects</sup>

Tools for image, video, audio, metadata, verification, and media forensics.

| Project | Type | Target Input | Description | Created | Last Update | Stars |
|:---|:---|:---|:---|:---:|:---:|---:|
| [Whisper](https://github.com/openai/whisper) | Python | Audio | Runs multilingual speech recognition, translation, and language identification locally. | 2022-09-16 | 2026-07-28 | ⭐ 107,841 |
| [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) | Python | Image; Document | Performs multilingual OCR, document layout analysis, and structured text extraction. | 2020-05-08 | 2026-07-22 | ⭐ 88,184 |
| [Tesseract](https://github.com/tesseract-ocr/tesseract) | C++ | Image; Document | Provides a multilingual optical character recognition engine. | 2014-08-12 | 2026-08-22 | ⭐ 76,136 |
| [face_recognition](https://github.com/ageitgey/face_recognition) | Python | Name; Image | Recognizes and compares faces through a Python API and command-line interface. | 2017-03-03 | 2026-06-25 | ⭐ 56,681 |
| [whisper.cpp](https://github.com/ggml-org/whisper.cpp) | C++ | Audio | Provides an efficient C and C++ implementation for local Whisper transcription. | 2022-09-25 | 2026-08-22 | ⭐ 53,123 |
| [Frigate](https://github.com/blakeblackshear/frigate) | TypeScript | Image; Video | Records and analyzes local IP-camera streams with real-time object detection, tracking, and search. | 2019-01-26 | 2026-08-22 | ⭐ 35,337 |
| [InsightFace](https://github.com/deepinsight/insightface) | Python | Name; Image | Performs face detection, alignment, recognition, and embedding analysis across multiple runtimes. | 2017-09-01 | 2026-07-27 | ⭐ 29,562 |
| [WhisperX](https://github.com/m-bain/whisperX) | Python | Audio | Adds word-level timestamps and speaker diarization to speech transcription. | 2022-12-09 | 2026-07-13 | ⭐ 23,707 |
| [DeepFace](https://github.com/serengil/deepface) | Python | Name; Image | Performs face verification, recognition, search, and facial attribute analysis. | 2020-02-08 | 2026-08-23 | ⭐ 23,327 |
| [CompreFace](https://github.com/exadel-inc/CompreFace) | Java | Name; Image | Provides self-hosted face detection, recognition, verification, and similarity search through a REST API. | 2020-07-06 | 2023-11-14 | ⭐ 8,267 |
| [docTR](https://github.com/mindee/doctr) | Python | Image; Document | Detects and recognizes text in document images using deep-learning models. | 2021-01-08 | 2026-08-21 | ⭐ 6,306 |
| [ZoneMinder](https://github.com/ZoneMinder/zoneminder) | PHP | Image; Video | Monitors, records, and reviews IP, USB, and analog camera feeds. | 2013-04-12 | 2026-08-22 | ⭐ 5,918 |
| [ExifTool](https://github.com/exiftool/exiftool) | Perl | Image | Reads and writes metadata embedded in images and other file formats. | 2018-05-09 | 2026-05-27 | ⭐ 4,972 |
| [Torchreid](https://github.com/KaiyangZhou/deep-person-reid) | Python | Name; Video | Re-identifies people across images and camera views with pretrained models and training tools. | 2018-03-11 | 2026-01-09 | ⭐ 4,899 |
| [motionEye](https://github.com/motioneye-project/motioneye) | Python | Image; Video | Provides web-based multi-camera monitoring, motion detection, recording, and review. | 2015-08-30 | 2026-08-12 | ⭐ 4,664 |
| [ImageHash](https://github.com/JohannesBuchner/imagehash) | Python | Image | Calculates perceptual image hashes for similarity and duplicate-image comparison. | 2013-03-02 | 2025-04-17 | ⭐ 3,862 |
| [Search by Image](https://github.com/dessant/search-by-image) | JavaScript | Image | Sends images to multiple reverse-image search engines from Chrome, Edge, and Safari. | 2017-06-17 | 2026-06-27 | ⭐ 3,721 |
| [Viseron](https://github.com/roflcoopter/viseron) | Python | Image; Video | Analyzes local camera feeds with motion, object, face, and license-plate detection. | 2020-08-30 | 2026-08-24 | ⭐ 3,402 |
| [Human](https://github.com/vladmandic/human) | TypeScript | Name; Image | Performs face detection, recognition, matching, and broader human analysis in browsers and Node.js. | 2020-10-11 | 2025-12-13 | ⭐ 3,260 |
| [Sherloq](https://github.com/GuidoBartoli/sherloq) | Python | Image | Combines metadata, error-level, noise, clone, splice, and resampling analysis for images. | 2017-06-24 | 2026-07-16 | ⭐ 3,191 |
| [DeepCamera](https://github.com/SharpAI/DeepCamera) | JavaScript | Image; Video | Analyzes camera feeds with local vision models, face recognition, re-identification, and configurable AI skills. | 2019-03-05 | 2026-04-21 | ⭐ 3,009 |
| [RetinaFace](https://github.com/serengil/retinaface) | Python | Image | Detects, aligns, and extracts faces from images for downstream comparison workflows. | 2021-04-25 | 2026-06-01 | ⭐ 2,024 |
| [MediaInfo](https://github.com/MediaArea/MediaInfo) | C++ | Video; Audio | Extracts technical metadata from audio, video, image, and container formats. | 2014-06-10 | 2026-08-11 | ⭐ 1,997 |
| [Photonix](https://github.com/photonixapp/photonix) | Python | Image | Organizes and searches local photo collections using faces, objects, locations, and visual attributes. | 2017-03-07 | 2026-07-20 | ⭐ 1,955 |
| [unblink](https://github.com/zapdos-labs/unblink) | Go | Image; Video | Uses vision-language models to monitor camera feeds and search recorded frames with natural language. | 2025-11-05 | 2026-03-09 | ⭐ 1,501 |
| [OpenOCR](https://github.com/Topdu/OpenOCR) | Python | Image; Document | Provides an open toolkit for text detection and recognition in images and documents. | 2024-05-31 | 2026-05-20 | ⭐ 1,436 |
| [HomeGallery](https://github.com/xemle/home-gallery) | JavaScript | Image | Indexes local photos and videos for reverse-image lookup, face search, and semantic discovery. | 2020-12-22 | 2026-06-22 | ⭐ 1,173 |
| [Kerberos Agent](https://github.com/kerberos-io/agent) | Go | Image; Video | Runs local video monitoring, recording, motion analysis, and event capture for RTSP camera streams. | 2020-08-12 | 2026-08-22 | ⭐ 1,101 |
| [camera.ui](https://github.com/cameraui/camera.ui) | TypeScript | Image; Video | Records, monitors, and searches local camera feeds with on-device detection workflows. | 2021-10-27 | 2026-08-20 | ⭐ 1,099 |
| [clearcam](https://github.com/roryclear/clearcam) | Python | Image; Video | Adds object detection, tracking, notifications, summaries, and search to security-camera feeds. | 2025-01-04 | 2026-08-19 | ⭐ 981 |
| [Horus](https://github.com/6abd/horus) | Python | Image | Performs local image and digital evidence analysis. | 2024-01-21 | 2026-07-29 | ⭐ 787 |
| [gallery-dl](https://codeberg.org/mikf/gallery-dl) | Python | Image | Downloads image galleries and media collections from supported websites. | 2026-03-24 | 2026-08-10 | ⭐ 426 |
| [VibeNVR](https://github.com/spupuz/VibeNVR) | JavaScript | Image; Video | Provides privacy-focused local camera recording and monitoring without a cloud dependency. | 2026-01-15 | 2026-08-18 | ⭐ 375 |
| [SentryShot](https://github.com/SentryShot/sentryshot) | Rust | Image; Video | Records camera streams and applies local object detection through a web video-management interface. | 2023-10-29 | 2026-04-27 | ⭐ 363 |
| [eye_of_web](https://github.com/MehmetYukselSekeroglu/eye_of_web) | Python | Image | Provides an open-source workflow for face-based image search. | 2025-12-31 | 2026-01-18 | ⭐ 316 |
| [GVision](https://github.com/GONZOsint/gvision) | Python | Image | Uses image analysis to detect landmarks and related web entities. | 2023-03-29 | 2024-12-08 | ⭐ 274 |
| [Project Eyes On](https://github.com/Y0oshi/Project-Eyes-On) | Python | Video | Finds publicly accessible IP-camera streams through public directories and web-search queries. | 2026-01-10 | 2026-01-12 | ⭐ 221 |
| [ExifTool Web](https://github.com/lucasgelfond/exiftool-web) | Svelte | Image | Runs ExifTool metadata inspection in a browser through WebAssembly. | 2025-02-22 | 2026-01-10 | ⭐ 151 |
| [goris](https://github.com/tanaikech/goris) | Go | Image | Runs Google reverse-image searches from the command line. | 2017-04-26 | 2026-07-07 | ⭐ 124 |
| [IntelHub](https://github.com/tomsec8/IntelHub) | JavaScript | URL; Image | Adds local browser tools for metadata, archives, dorking, and OSINT lookups. | 2025-05-15 | 2026-07-09 | ⭐ 120 |
| [EfficientIR](https://github.com/Sg4Dylan/EfficientIR) | Python | Image | Finds similar and duplicate images in local collections using visual embeddings. | 2020-03-30 | 2024-07-22 | ⭐ 112 |
| [lingolens](https://github.com/OSINT-mindset/lingolens) | HTML | Image | Runs multilingual Google Lens searches and exports the results. | 2023-03-10 | 2026-05-29 | ⭐ 87 |
| [PhotOSINT](https://github.com/Haris87/photosint) | JavaScript | Image | Extracts image metadata and adds reverse-image search actions to the browser. | 2019-09-15 | 2021-07-13 | ⭐ 60 |
| [OpenArchive Save](https://github.com/OpenArchive/Save-app-ios) | Swift | File | Captures and preserves mobile media with secure storage and provenance-oriented workflows. | 2018-06-06 | 2026-07-28 | ⭐ 20 |
| [ProofMode](https://gitlab.com/guardianproject/proofmode/proofmode-android) | Kotlin | File | Adds hashes, signatures, sensor data, and C2PA provenance to captured mobile media. | 2022-01-10 | 2026-08-06 | ⭐ 18 |
| [Amanu](https://gitlab.com/varg.alejandro25/amanu) | Python | Audio | Runs local speech transcription and assigns timestamped passages to detected speakers. | 2026-07-09 | 2026-07-20 | ⭐ 1 |

<p align="right"><a href="#table-of-contents">Back to contents ↑</a></p>

<a id="geolocation"></a>

## 📍 Geolocation <sup>34 projects</sup>

Tools for locations, coordinates, maps, wireless identifiers, aircraft, and satellite data.

| Project | Type | Target Input | Description | Created | Last Update | Stars |
|:---|:---|:---|:---|:---:|:---:|---:|
| [World Monitor](https://github.com/koala73/worldmonitor) | TypeScript | Location | Unifies geopolitical news, infrastructure, and event monitoring in one dashboard. | 2026-01-08 | 2026-08-22 | ⭐ 83,971 |
| [QGIS](https://github.com/qgis/QGIS) | C++ | Location | Provides a complete desktop environment for geospatial data analysis and mapping. | 2011-05-02 | 2026-08-24 | ⭐ 14,272 |
| [Shadowbroker](https://github.com/BigBodyCobain/Shadowbroker) | Python | Location | Tracks aircraft, satellites, seismic events, and other global activity. | 2026-03-05 | 2026-08-24 | ⭐ 10,942 |
| [GeoLibre](https://github.com/opengeos/GeoLibre) | Python | Location; Image | Provides open geospatial and remote-sensing analysis workflows. | 2026-05-27 | 2026-08-24 | ⭐ 6,649 |
| [OSMnx](https://github.com/gboeing/osmnx) | Python | Location | Downloads, models, and analyzes street networks and other OpenStreetMap features. | 2016-07-24 | 2026-07-31 | ⭐ 5,827 |
| [Google Maps Scraper by gosom](https://github.com/gosom/google-maps-scraper) | Go | Organization Name; Location | Collects structured place and business information from Google Maps. | 2023-04-22 | 2026-08-22 | ⭐ 5,596 |
| [GeoAI](https://github.com/opengeos/geoai) | Python | Location; Image | Applies machine-learning and computer-vision workflows to geospatial data. | 2023-08-11 | 2026-08-02 | ⭐ 3,319 |
| [Google Maps Scraper by omkarcloud](https://github.com/omkarcloud/google-maps-scraper) | Python | Organization Name; Location | Provides an alternative workflow for extracting business and place data from Google Maps. | 2023-05-19 | 2026-07-27 | ⭐ 3,120 |
| [IPinfo CLI](https://github.com/ipinfo/cli) | Go | IP Address; ASN | Queries IP geolocation, ASN, privacy, and network data from the command line. | 2020-10-23 | 2026-04-28 | ⭐ 2,056 |
| [asn](https://github.com/nitefood/asn) | Shell | IP Address; ASN | Reports ASN, BGP, geolocation, reputation, and routing information for IPs. | 2020-07-22 | 2026-06-22 | ⭐ 1,923 |
| [Global Threat Map](https://github.com/unicodeveloper/globalthreatmap) | TypeScript | Location | Maps conflicts, military bases, and historical geopolitical data. | 2026-01-22 | 2026-07-02 | ⭐ 1,804 |
| [GeoWiFi](https://github.com/GONZOsint/geowifi) | Python | Location; BSSID / SSID | Queries public Wi-Fi geolocation sources using BSSIDs and SSIDs. | 2022-02-05 | 2024-12-21 | ⭐ 1,493 |
| [Satpy](https://github.com/pytroll/satpy) | Python | Location; Image | Loads, transforms, composites, and exports meteorological satellite observations. | 2016-02-09 | 2026-08-21 | ⭐ 1,204 |
| [GeoIntel](https://github.com/atiilla/GeoIntel) | HTML | Location; Image | Uses assisted image analysis to estimate where a photograph was taken. | 2024-01-22 | 2026-03-09 | ⭐ 1,128 |
| [CoastSat](https://github.com/kvos/CoastSat) | Python | Location; Image | Extracts and analyzes shoreline change from public satellite imagery. | 2018-09-28 | 2026-05-29 | ⭐ 885 |
| [OSINT Mapping Tool](https://github.com/anonymousRAID/OSINT-Mapping-Tool) | JavaScript | Location | Organizes investigation data and geographic findings on an interactive map. | 2026-05-18 | 2026-07-05 | ⭐ 643 |
| [ShadowFinder](https://github.com/bellingcat/ShadowFinder) | Python | Location | Estimates possible locations from the geometry of shadows in an image. | 2024-05-01 | 2026-02-13 | ⭐ 602 |
| [Sightline](https://github.com/ni5arga/sightline) | TypeScript | Location | Searches OpenStreetMap data for real-world infrastructure patterns. | 2026-01-25 | 2026-05-10 | ⭐ 558 |
| [ExifLooter](https://github.com/aydinnyunus/exifLooter) | Go | Image | Finds geolocation metadata in local and remote images and maps the results. | 2022-07-30 | 2026-01-16 | ⭐ 496 |
| [EODAG](https://github.com/CS-SI/eodag) | Python | Location; Image | Searches and downloads Earth observation products from multiple data providers. | 2019-08-22 | 2026-08-21 | ⭐ 426 |
| [Refloow Geo Forensics](https://github.com/Refloow/Refloow-Geo-Forensics) | JavaScript | Location; Coordinates; Image | Extracts media metadata, maps coordinates, and reconstructs event timelines. | 2026-02-04 | 2026-07-07 | ⭐ 212 |
| [Bellingcat OSM Search](https://github.com/bellingcat/osm-search) | TypeScript | Location | Finds combinations of OpenStreetMap features based on their geographic proximity. | 2022-10-05 | 2026-07-07 | ⭐ 207 |
| [Bellingcat ADS-B History](https://github.com/bellingcat/adsb-history) | TypeScript | Location; Aircraft ID | Stores historical ADS-B observations and supports spatial, temporal, and aircraft filtering. | 2025-08-22 | 2026-03-05 | ⭐ 89 |
| [Copernicus Browser](https://github.com/eu-cdse/copernicus-browser) | JavaScript | Location; Image | Searches, visualizes, and compares Earth observation data from Copernicus services. | 2023-08-08 | 2026-08-04 | ⭐ 86 |
| [IntellyWeave](https://github.com/vericle/intellyweave) | Python | URL; Location; Document | Combines archive discovery, entity extraction, maps, graphs, and document analysis. | 2025-12-12 | 2026-01-12 | ⭐ 75 |
| [Bellingcat Geoclustering](https://github.com/bellingcat/geoclustering) | Python | Location | Groups and explores geographic observations to identify spatial patterns. | 2022-06-29 | 2026-07-07 | ⭐ 45 |
| [Locus](https://github.com/alpkeskin/locus) | Python | Location; Coordinates; Image | Estimates GPS coordinates from street-level photographs. | 2025-11-22 | 2025-12-01 | ⭐ 33 |
| [Bellingcat CouncilSearcher](https://github.com/bellingcat/CouncilSearcher) | Python | Location | Searches local-government documents and records across supported council websites. | 2025-05-07 | 2026-01-07 | ⭐ 17 |
| [NEXUS](https://github.com/Kit4Some/NEXUsint) | Python | Domain; IP Address; URL; Location; File Hash | Combines live multi-INT feeds, knowledge graphs, maps, and assisted analysis in a desktop platform. | 2026-03-20 | 2026-03-30 | ⭐ 15 |
| [Vantage](https://github.com/thometnanni/vantage) | Elixir | Location; Image | Reconstructs image and video viewpoints inside three-dimensional environments. | 2024-11-15 | 2026-05-13 | ⭐ 14 |
| [Geo Trajectory Analysis](https://github.com/eyal-weiss/geo-trajectory-analysis) | Skill | Location; Video | Applies a documented video-geolocation method to estimate missile launch origins. | 2026-03-23 | 2026-03-23 | ⭐ 3 |
| [Bellingcat OSINT Toolkit Skills](https://github.com/CasualSecurityInc/Bellingcat-OSINT-Toolkit) | Skill pack | - | Packages hundreds of investigation resources by geolocation, media, identity, transport, and conflict use case. | 2026-07-12 | 2026-07-12 | ⭐ 1 |
| [Norteia Lead Recon](https://github.com/Luispitik/norteia-lead-recon) | Skill | Name; Organization Name; Location | Researches Spanish companies and leads through official open registers and geodata. | 2026-04-29 | 2026-04-29 | ⭐ 0 |
| [Geolocation Skill](https://github.com/zuocharles/geolocation-skill) | Skill | Location; Image | Guides photo geolocation with visual clues, map queries, and source references. | 2026-03-30 | 2026-03-31 | ⭐ 0 |

<p align="right"><a href="#table-of-contents">Back to contents ↑</a></p>

<a id="cryptocurrency"></a>

## ₿ Cryptocurrency <sup>8 projects</sup>

Tools for cryptocurrency addresses, blockchain activity, and transaction analysis.

| Project | Type | Target Input | Description | Created | Last Update | Stars |
|:---|:---|:---|:---|:---:|:---:|---:|
| [Manuscript](https://github.com/chainbase-labs/manuscript-core) | Rust | Crypto Address | Streams on-chain and off-chain data into systems prepared for analysis. | 2024-09-24 | 2026-08-09 | ⭐ 690 |
| [Bitcoin ETL](https://github.com/blockchain-etl/bitcoin-etl) | Python | Crypto Address | Exports Bitcoin-family blockchain data into analysis-friendly formats. | 2018-09-13 | 2025-05-02 | ⭐ 460 |
| [all-in-one-bot](https://github.com/uerax/all-in-one-bot) | Go | Crypto Address | Tracks on-chain activity and market signals through a Telegram interface. | 2023-03-28 | 2026-08-13 | ⭐ 180 |
| [GraphSense Dashboard](https://github.com/graphsense/graphsense-dashboard) | Elm | Crypto Address | Provides interactive exploration of cryptocurrency transactions and entities. | 2017-10-18 | 2026-07-17 | ⭐ 137 |
| [GraphSense Library](https://github.com/graphsense/graphsense-lib) | Python | Crypto Address | Supplies CLI and backend utilities for cryptocurrency analytics workflows. | 2022-10-11 | 2026-08-21 | ⭐ 18 |
| [Wash Trade Scanner](https://github.com/Yog-Sotho/Wash-Trade-Scanner) | Python | Crypto Address | Audits blockchain activity for wash trading and artificial volume patterns. | 2026-04-16 | 2026-08-08 | ⭐ 3 |
| [PolyShadow](https://github.com/Ha1o/PolyShadow) | Python | Crypto Address | Monitors new Polymarket wallets for unusual high-value positions. | 2026-01-10 | 2026-02-23 | ⭐ 2 |
| [BitSleuth Analyzer](https://github.com/BitSleuthAI/Analyzer) | TypeScript | Crypto Address | Analyzes Bitcoin wallets, transaction patterns, and mempool activity. | 2025-08-05 | 2026-07-07 | ⭐ 1 |

<p align="right"><a href="#table-of-contents">Back to contents ↑</a></p>

<a id="investigation"></a>

## 🔎 Investigation <sup>28 projects</sup>

Cross-cutting investigation, case-management, correlation, and research workspaces.

| Project | Type | Target Input | Description | Created | Last Update | Stars |
|:---|:---|:---|:---|:---:|:---:|---:|
| [Anthropic Cybersecurity Skills](https://github.com/mukul975/Anthropic-Cybersecurity-Skills) | Skill library | - | Packages extensive offensive, defensive, CTI, forensics, and reconnaissance procedures. | 2026-02-25 | 2026-08-23 | ⭐ 30,863 |
| [Claude Skills](https://github.com/alirezarezvani/claude-skills) | Skills + plugins | - | Includes research, security, market analysis, compliance, and evidence-oriented agent skills. | 2025-10-19 | 2026-08-21 | ⭐ 24,870 |
| <img src=".github/assets/new-dot.svg" width="6" height="6" alt=""> [osiris](https://github.com/simplifaisoul/osiris) | TypeScript | - | Aggregates live aviation, maritime, camera, seismic, wildfire, news, weather, space, cyber, sanctions, and public Telegram data in a real-time situational-awareness dashboard. | 2026-05-12 | 2026-08-23 | ⭐ 7,885 |
| [Flowsint](https://github.com/reconurge/flowsint) | TypeScript | Name; Organization Name | Explores investigation entities and enrichments in a local graph-based workspace. | 2025-01-31 | 2026-08-23 | ⭐ 7,735 |
| [Mr.Holmes](https://github.com/Lucksi/Mr.Holmes) | Python | Name; Username; Phone Number; Domain | Combines multiple identity, domain, phone, and social investigation modules. | 2021-06-23 | 2026-02-21 | ⭐ 4,096 |
| [Argus](https://github.com/jasonxtn/Argus) | Python | Keyword | Combines multiple information gathering modules in a command-line toolkit. | 2024-10-01 | 2025-12-10 | ⭐ 4,076 |
| [Timesketch](https://github.com/google/timesketch) | Python | Event Data | Supports collaborative search, annotation, and analysis across multiple event timelines. | 2014-06-19 | 2026-08-18 | ⭐ 3,392 |
| [CTF Skills](https://github.com/ljagiello/ctf-skills) | Skill pack | - | Supplies agent workflows for CTF categories including OSINT, forensics, and web investigation. | 2026-02-01 | 2026-08-22 | ⭐ 3,065 |
| [sn0int](https://github.com/kpcyrd/sn0int) | Rust | - | Provides a semi-automatic OSINT framework with installable modules. | 2018-10-05 | 2025-01-31 | ⭐ 2,515 |
| [OpenOSINT](https://github.com/OpenOSINT/OpenOSINT) | Agent + CLI + MCP | - | Combines OSINT tools in an interactive agent, command-line interface, and MCP server. | 2026-05-06 | 2026-08-20 | ⭐ 1,457 |
| [Hackingtool Plugin](https://github.com/AKCodez/hackingtool-plugin) | Plugin + skill | - | Makes a large catalogue of pentest and OSINT tools discoverable and runnable by Claude. | 2026-04-23 | 2026-04-25 | ⭐ 1,015 |
| [Seekr](https://github.com/seekr-osint/seekr) | Go | Keyword | Offers a multi-purpose OSINT toolkit through a web interface. | 2022-12-06 | 2026-06-16 | ⭐ 859 |
| [PANO](https://github.com/ALW1EZ/PANO) | Python | Name; Organization Name; Event Data | Combines link graphs, timelines, notes, and assisted investigation features. | 2024-12-30 | 2026-02-13 | ⭐ 590 |
| [LinkScope Client](https://github.com/AccentuSoft/LinkScope_Client) | Python | Name; Organization Name | Represents investigation entities and relationships in an extensible visual workspace. | 2021-09-15 | 2025-02-06 | ⭐ 491 |
| [OGI](https://github.com/khashashin/ogi) | Python | Name; Organization Name | Provides link analysis and open-source intelligence investigation workflows. | 2026-02-28 | 2026-07-24 | ⭐ 288 |
| [FollowTheMoney](https://github.com/alephdata/followthemoney) | Python | Name; Organization Name; Dataset | Defines an investigative data model for entities, assets, documents, and relationships. | 2017-10-20 | 2025-06-27 | ⭐ 285 |
| [PRISM](https://github.com/NovaCode37/Prism-platform) | Python | - | Combines multi-target OSINT modules, OPSEC scoring, entity graphs, and assisted reporting. | 2026-03-30 | 2026-08-17 | ⭐ 185 |
| [Huntkit](https://github.com/assafkip/huntkit) | Skills + MCP | Name; Organization Name; Event Data | Organizes cases, targets, findings, timelines, evidence hashes, and chain-of-custody records. | 2026-04-15 | 2026-07-06 | ⭐ 49 |
| [deep-recon](https://github.com/kvarnelis/deep-recon) | Skill | - | Coordinates multi-agent research and stores reconnaissance findings in Obsidian. | 2026-02-18 | 2026-02-21 | ⭐ 43 |
| [OSINT-NEXUS](https://github.com/Muhib-Mehdi/OSINT-NEXUS) | Python | Name; Organization Name | Combines multi-target collection, entity correlation, graphs, and reporting in a desktop application. | 2025-12-30 | 2026-08-15 | ⭐ 42 |
| [OSINT Agent Skills](https://github.com/frangelbarrera/osint-agent-skills) | Skills + MCP | - | Combines OSINT playbooks, agent instructions, report templates, and MCP tool definitions. | 2026-06-27 | 2026-07-27 | ⭐ 23 |
| <img src=".github/assets/new-dot.svg" width="6" height="6" alt=""> [OSINT Skills](https://github.com/useosint/osint-skills) | Skills + plugin | - | Provides 28 source-grounded skills for agent-led OSINT workflows, evidence grading, and investigative reporting. | 2026-08-02 | 2026-08-03 | ⭐ 21 |
| [Abster Intelligence](https://github.com/frangelbarrera/Abster-Intelligence) | TypeScript | Name; Organization Name; Event Data | Provides a local-first workspace for evidence, relationship graphs, timelines, OSINT lookups, and reports. | 2026-04-10 | 2026-07-21 | ⭐ 16 |
| [OSINT Investigation](https://github.com/reichaves/osint-investigation) | Skill | Name; Username; Location; Image | Guides geolocation, source verification, entity profiling, and social-media investigation. | 2026-05-02 | 2026-05-03 | ⭐ 6 |
| [OSINT Investigator](https://github.com/TNeagle/osint-investigator) | Skill | Name; Organization Name; Location; Coordinates | Coordinates multi-domain investigations, public-record research, geolocation, and intelligence reports. | 2026-03-18 | 2026-03-20 | ⭐ 3 |
| [OSINT Investigator for OpenClaw](https://github.com/Elyasuuuuu/osint-investigator) | Skill | Name; Username; Email; Organization Name; Domain; IP Address | Correlates usernames, emails, domains, IPs, organizations, and public profile evidence. | 2026-03-16 | 2026-03-16 | ⭐ 1 |
| [Claude OSINT Plugin](https://github.com/lawriec/claude-osint-plugin) | Plugin + skills + MCP | URL; Image | Adds an intelligence-cycle methodology and configured search, media, archive, and analysis MCP servers. | 2026-04-09 | 2026-05-10 | ⭐ 1 |
| [OSINT Researcher](https://github.com/MrBridgeHQ/osint-researcher-claude) | Skill | - | Provides scoped OSINT, CTI, due diligence, and evidence-reporting procedures. | 2026-07-01 | 2026-07-06 | ⭐ 1 |

<p align="right"><a href="#table-of-contents">Back to contents ↑</a></p>
