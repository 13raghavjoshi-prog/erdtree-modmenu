# Security Policy

erdtree-modmenu is an **offline-only** Elden Ring memory toolkit. It is not
intended for use in online sessions and will get you banned if you try.

## Reporting

Open a private advisory via GitHub Security Advisories. Do not file public
issues for anything that could be weaponized against other players' saves.

## Scope

In scope:
- Save-file corruption caused by handlers writing out of bounds
- RCE in the native sidecar (`erdtree_native/`)
- Signature scanner crashes on malformed patterns

Out of scope:
- EasyAntiCheat bypass discussions
- Anything requiring a live online session
- "It doesn't work after patch X" — patches land constantly, PRs welcome

## Save backups

`config/default.toml` enables `auto_backup_save = true` by default. Do not
disable it unless you enjoy restarting Limgrave runs.