<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/header-dark.svg" />
  <img src="./assets/header-light.svg" width="100%" alt="Hanahira 花平 — HanahiraNetwork · small, fast, self-hosted" />
</picture>

<br />

<a href="https://hanahira.dev/"><img src="https://img.shields.io/badge/hanahira.dev-E4739B?style=for-the-badge&logo=hey&logoColor=FFF5F7" alt="Website" /></a>
<a href="https://x.com/HanahiraDev"><img src="https://img.shields.io/badge/@HanahiraDev-B5838D?style=for-the-badge&logo=x&logoColor=FFF5F7" alt="X" /></a>
<a href="https://discord.hanahira.dev/"><img src="https://img.shields.io/badge/Discord-B5838D?style=for-the-badge&logo=discord&logoColor=FFF5F7" alt="Discord" /></a>
<a href="https://github.com/KBYSHanahira?tab=repositories"><img src="https://img.shields.io/badge/Repositories-8C5162?style=for-the-badge&logo=github&logoColor=FFF5F7" alt="Repositories" /></a>
<img src="https://api.visitorbadge.io/api/visitors?path=github.com%2FKBYSHanahira&label=VISITORS&labelColor=%238c5162&countColor=%23e4739b&style=for-the-badge" alt="Profile views" />

<br /><br />

**`Super Junior Programmer :)`** — I build the whole stack myself, from the DNS resolver up to the page you land on.

</div>

<br />

## 🌸 私について · About me

I'm **Hanahira** (花平, *はなひら* — "a blooming flower"), and **HanahiraNetwork** is my corner of the internet.

Most of what I make is the same shape: **small, fast services that run on my own hardware** — Bun or Go,
packed into **Docker**, sitting behind a reverse proxy I wrote myself. Lately that also means tooling around
**Claude Code** and **VRChat**, and I still keep a soft spot for **ComfyUI** extensions and **C++ on microcontrollers**.

```ts
const hanahira = {
  handle:   "KBYSHanahira",
  network:  "https://hanahira.dev",
  builds:   ["DNS", "VPN", "cloud storage", "status pages", "a reverse proxy / WAF"],
  stack:    ["Bun", "Hono", "Go", "TypeScript", "Preact", "MySQL", "PostgreSQL", "Docker"],
  sideQuests: ["Claude Code mods", "VRChat tools", "ComfyUI", "Arduino"],
  motto:    "Ship it small, ship it self-hosted. 🌸",
} as const;
```

<br />

## 🌐 ネットワーク · HanahiraNetwork

<sub>Everything below is self-hosted on my own machines and built from scratch. Source is private — the services are live.</sub>

| | Service | What it does | Built with |
| :---: | --- | --- | --- |
| 🧭 | **[DNS](https://dns.hanahira.dev/)** | Recursive / forwarding resolver over UDP, TCP, DoT and DoH — filtering, rewrites, monitoring, leader + hot-standby HA | `Bun` `React` `PostgreSQL` |
| 🔐 | **[VPN](https://vpn.hanahira.dev/)** | WireGuard access management — approval sign-up, self-service devices with QR codes, traffic history, TOTP 2FA, 25 languages | `Bun` `Hono` `Vite` |
| ☁️ | **[Cloud](https://cloud.hanahira.dev/)** | Private cloud storage — nested folders, password / expiring share links, video & audio streaming, quotas, audit log | `Bun` `Hono` `Preact` `MySQL` |
| 📈 | **[Status](https://status.hanahira.dev/)** | Public status page and ops panel for servers, Docker and databases in one | `Bun` `Hono` `Preact` |
| 🛡️ | **Web Security** | The gateway in front of it all — single Go binary: routing, TLS/ACME, HTTP/3, WAF, rate limits, OIDC login | `Go` |
| 🧰 | **[Tools](https://hanahira.dev/)** | [Speed test](https://speed.hanahira.dev/) · [JLPT practice](https://hanahira.dev/JLPT) · [QR generator](https://hanahira.dev/qr) · [Portfolio](https://hanahira.dev/portfolio/) | `Hono` `Vite` |

<br />

## 📦 作品 · Open source

| Project | What it is | |
| --- | --- | --- |
| 🌸 **[ClaudeHanahiraUI](https://github.com/KBYSHanahira/ClaudeHanahiraUI)** | Interface mod for Claude Code — a status band above the prompt with ring gauges for context and 5h / 7d limits, cost / token / time cards, live agent cards and styled conversation logs | ![TypeScript](https://img.shields.io/badge/TypeScript-E4739B?style=flat-square&logo=typescript&logoColor=FFF5F7) |
| 🩹 **[HanahiraVRCTools](https://github.com/KBYSHanahira/HanahiraVRCTools)** | One-click Windows repair kit for VRChat — crashes, EAC, cache, IME, Discord hook, network and audio. One `.bat`, nothing to install | ![Batch](https://img.shields.io/badge/Batch-E4739B?style=flat-square&logo=windowsterminal&logoColor=FFF5F7) |
| 🗣️ **[kikitan-translator](https://github.com/KBYSHanahira/kikitan-translator)** | Real-time speech translation for VRChat — voice to chatbox over OSC, desktop-audio subtitles and a VR overlay. <sub>fork of YusufOzmen01/kikitan-translator</sub> | ![C#](https://img.shields.io/badge/C%23-C2637F?style=flat-square&logo=dotnet&logoColor=FFF5F7) |
| ⬇️ **[Civicomfy](https://github.com/KBYSHanahira/Civicomfy)** | Civitai model downloader for ComfyUI. <sub>fork of MoonGoblinDev/Civicomfy</sub> | ![stars](https://img.shields.io/github/stars/KBYSHanahira/Civicomfy?style=flat-square&logo=github&label=%E2%98%85&color=C2637F&labelColor=8C5162) |
| 🔎 **[sd-civitai-browser-plus](https://github.com/KBYSHanahira/sd-civitai-browser-plus)** | Browse, download and update Civitai models from inside the SD WebUI. <sub>fork of BlafKing/sd-civitai-browser-plus</sub> | ![Python](https://img.shields.io/badge/Python-C2637F?style=flat-square&logo=python&logoColor=FFF5F7) |

<sub>Older, from the learning days: [Data-Structure](https://github.com/KBYSHanahira/Data-Structure) (C++) · [Arduino](https://github.com/KBYSHanahira/Arduino) (C++)</sub>

<br />

## 🌿 技術スタック · Tech stack

<div align="center">

<img src="https://img.shields.io/badge/TypeScript-E4739B?style=flat-square&logo=typescript&logoColor=FFF5F7" alt="TypeScript" />
<img src="https://img.shields.io/badge/Go-E4739B?style=flat-square&logo=go&logoColor=FFF5F7" alt="Go" />
<img src="https://img.shields.io/badge/JavaScript-E4739B?style=flat-square&logo=javascript&logoColor=FFF5F7" alt="JavaScript" />
<img src="https://img.shields.io/badge/C%23-E4739B?style=flat-square&logo=dotnet&logoColor=FFF5F7" alt="C#" />
<img src="https://img.shields.io/badge/C++-E4739B?style=flat-square&logo=cplusplus&logoColor=FFF5F7" alt="C++" />
<img src="https://img.shields.io/badge/Python-E4739B?style=flat-square&logo=python&logoColor=FFF5F7" alt="Python" />
<img src="https://img.shields.io/badge/SQL-E4739B?style=flat-square&logo=mysql&logoColor=FFF5F7" alt="SQL" />
<br />
<img src="https://img.shields.io/badge/Bun-C2637F?style=flat-square&logo=bun&logoColor=FFF5F7" alt="Bun" />
<img src="https://img.shields.io/badge/Hono-C2637F?style=flat-square&logo=hono&logoColor=FFF5F7" alt="Hono" />
<img src="https://img.shields.io/badge/Vite-C2637F?style=flat-square&logo=vite&logoColor=FFF5F7" alt="Vite" />
<img src="https://img.shields.io/badge/Preact-C2637F?style=flat-square&logo=preact&logoColor=FFF5F7" alt="Preact" />
<img src="https://img.shields.io/badge/React-C2637F?style=flat-square&logo=react&logoColor=FFF5F7" alt="React" />
<img src="https://img.shields.io/badge/Node.js-C2637F?style=flat-square&logo=nodedotjs&logoColor=FFF5F7" alt="Node.js" />
<br />
<img src="https://img.shields.io/badge/Docker-8C5162?style=flat-square&logo=docker&logoColor=FFF5F7" alt="Docker" />
<img src="https://img.shields.io/badge/Linux-8C5162?style=flat-square&logo=linux&logoColor=FFF5F7" alt="Linux" />
<img src="https://img.shields.io/badge/MySQL-8C5162?style=flat-square&logo=mysql&logoColor=FFF5F7" alt="MySQL" />
<img src="https://img.shields.io/badge/PostgreSQL-8C5162?style=flat-square&logo=postgresql&logoColor=FFF5F7" alt="PostgreSQL" />
<img src="https://img.shields.io/badge/WireGuard-8C5162?style=flat-square&logo=wireguard&logoColor=FFF5F7" alt="WireGuard" />
<img src="https://img.shields.io/badge/Nginx-8C5162?style=flat-square&logo=nginx&logoColor=FFF5F7" alt="Nginx" />
<img src="https://img.shields.io/badge/Git-8C5162?style=flat-square&logo=git&logoColor=FFF5F7" alt="Git" />
<br />
<img src="https://img.shields.io/badge/Claude_Code-F0A8BC?style=flat-square&logo=anthropic&logoColor=5C2E3E" alt="Claude Code" />
<img src="https://img.shields.io/badge/VRChat-F0A8BC?style=flat-square&logo=vrchat&logoColor=5C2E3E" alt="VRChat" />
<img src="https://img.shields.io/badge/ComfyUI-F0A8BC?style=flat-square&logo=nodedotjs&logoColor=5C2E3E" alt="ComfyUI" />
<img src="https://img.shields.io/badge/Arduino-F0A8BC?style=flat-square&logo=arduino&logoColor=5C2E3E" alt="Arduino" />

</div>

<br />

## 📊 統計 · GitHub in numbers

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./profile-summary-card-output/github_dark/0-profile-details.svg" />
  <img src="./profile-summary-card-output/default/0-profile-details.svg" width="100%" alt="Profile details" />
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./profile-summary-card-output/github_dark/3-stats.svg" />
  <img src="./profile-summary-card-output/default/3-stats.svg" width="49%" alt="Stats" />
</picture>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./profile-summary-card-output/github_dark/2-most-commit-language.svg" />
  <img src="./profile-summary-card-output/default/2-most-commit-language.svg" width="49%" alt="Most commit language" />
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./profile-summary-card-output/github_dark/1-repos-per-language.svg" />
  <img src="./profile-summary-card-output/default/1-repos-per-language.svg" width="49%" alt="Repos per language" />
</picture>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./profile-summary-card-output/github_dark/4-productive-time.svg" />
  <img src="./profile-summary-card-output/default/4-productive-time.svg" width="49%" alt="Productive time (UTC+7)" />
</picture>

</div>

<br />

## 🐍 貢献グラフ · Contribution graph

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/KBYSHanahira/KBYSHanahira/output/github-contribution-grid-snake-dark.svg" />
  <img src="https://raw.githubusercontent.com/KBYSHanahira/KBYSHanahira/output/github-contribution-grid-snake.svg" alt="Contribution snake" />
</picture>

<sub>🌸 the petals fall as the snake passes</sub>

<br /><br />

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/footer-dark.svg" />
  <img src="./assets/footer-light.svg" width="100%" alt="ご覧いただきありがとうございます — Thanks for stopping by" />
</picture>

</div>
