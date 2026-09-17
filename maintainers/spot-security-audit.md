# Spot Tutorial security audit

**Not part of the published website.** Internal working document for
Entwicklungsauftrag 9. Excluded from the Sphinx build (source root is
`docs/`; `maintainers/` is outside it) and not linked from any published
toctree. No secret value is reproduced anywhere in this file — category
and location only, per the task's explicit rule.

## Method

Read-only scan of the old Spot tutorial (`00-02 Quelle 2 Spot Tutorial`),
the current Spot code (`Backup Ansible/workspaces`), and the Ansible/
deployment bestand (`Backup Ansible/ansible` + `configs`). No file that
looked like an Ansible Vault, `.env`, private key, or certificate was
opened for its contents — only its path and category were recorded. No
code, playbook, launch file, or deployment script was executed.

## Findings

### A. Current Spot code (`Backup Ansible/workspaces`)

| Category | Location | Action taken |
| --- | --- | --- |
| Plaintext robot login credentials | `configs/spot_login.yaml`, `workspaces/spot_ws/spot_login.yaml` (identical) | Not opened beyond confirming presence; excluded from any migration; not referenced by path in public docs |
| Plaintext credential env vars (`BOSDYN_CLIENT_USERNAME`/`PASSWORD`) | `configs/.bashrc` | Value not read (the backup's own `docs/system_extras.md` already redacts the password value); excluded from migration |
| Private IP addresses, a private network's gateway config, internal hostnames, WiFi SSID names | `Backup Ansible/docs/system_extras.md` | Not reproduced; any network diagram in the public docs uses the neutral placeholders `<SPOT_IP>`, `<COMPUTE_HOST>`, `<OPERATOR_HOST>`, `<ROBOT_NETWORK>` instead of real values |
| Environment/secrets file for an unrelated dashboard tool | `Backup Ansible/other_code/vsting/webui/.env` | Not opened; unrelated to the Spot robot stack; excluded entirely, no reference in any docs |
| TLS test certificates (`.pem`/`.crt`) | `workspaces/spot_ws/src/spot_ros2/spot_wrapper/spot_wrapper/testing/credentials/` | Identified as vendored upstream unit-test fixtures for the `spot_ros2` driver's auth-flow tests (path and filenames indicate mock certs, not this team's real device secrets); not opened, not referenced |
| SSH keys, GitHub CLI token, GPG keys, WiFi passwords | Explicitly stated as **excluded from the backup itself** by `Backup Ansible/docs/nicht_kopiert.md` | Nothing to find locally; no action needed |
| Unrelated operational note (not a secret, but security-relevant) | Boston Dynamics Spot software license recorded as expired 2024-08-24, per `Backup Ansible/README.md` | Noted here for the maintainers/robot owner; not published, as it is an account/licensing matter, not tutorial content |
| Maintainers' own acknowledgement that a credential needs rotation | `Backup Ansible/scripts/restore.sh` ends with an operator reminder, verbatim in German: "BOSDYN-Passwort in .bashrc rotieren" ("rotate the BOSDYN password in .bashrc") | Confirms `configs/.bashrc`'s `BOSDYN_CLIENT_PASSWORD` is a live credential the team itself flagged as needing rotation; not reproduced here; recommend the robot owner actually rotate it, independent of this documentation task |

### B. Old Spot tutorial (`00-02 Quelle 2 Spot Tutorial`)

| Category | Location | Action taken |
| --- | --- | --- |
| Internal WiFi network name (text) | `Spot Documentation/08 Spot Startup` page: "Connect to the Wi-Fi network named 'Alert'" | Not migrated; rewritten safety/operating pages describe connecting to the robot's operator network generically, without naming it |
| Informal credential reference + personal first-name credit (text) | Same page: "(The credentials are saved. Thanks to Max.)" | Not migrated; excluded per the task's explicit instruction to drop this exact line |
| Private IP address visible in a screenshot | `.../08 Spot Startup/..._files/kinova_web.png` and `kinova_faults.png` (manipulator web UI, IP visible in the browser address bar) | **Image excluded from migration entirely** — not on the task's requested image list, and shows real internal network information |
| List of real local WiFi network names visible in a screenshot (including a third-party team's SSID) | `.../08 Spot Startup/..._files/wifi.png` | **Image excluded from migration entirely** — same reasoning as above |
| Third-party organisation's network name appearing incidentally in a screenshot | Same `wifi.png` (one SSID in the visible list references an unrelated team's network) | No action needed beyond excluding the image — this is not this team's content and is not reproduced anywhere |
| Personal names visible (no captions/contact info) | Faces in `award_ceremony.jpg`, `rrl_eindhoven_group.png` | Faces are visible but no names are attached in the HTML (no alt text, no captions naming individuals) in the source; new alt text/captions for these two images will describe the scene (award ceremony, team group photo) without naming individuals, since no name attribution exists in the source to be accurate about |

Text-level scan (password/WiFi/SSID/credential/API-key/token/secret/email
patterns) across every old-tutorial HTML page found **no** additional
hits beyond the two listed above (item confirmed: one version-number
string, "2.1.5.0", was a false positive for an IP address, not a real
finding).

### C. Ansible / deployment bestand (`Backup Ansible/ansible`, `configs`)

No Ansible Vault file exists in the local Ansible content (confirmed by
directory listing; none opened regardless). No `group_vars`/`host_vars`
directory structure exists at all (see `spot-source-audit.md` §5) — the
single playbook targets `localhost` and carries no per-host secrets of its
own. Real network values referenced by other configs (udev rules, RViz
layout, middleware config) were reviewed for structure only; no secret
values were found embedded in those particular files.

### D. This repository (`Learning-Robotics-Crash-Course`)

Already covered by the prior `SECURITY_REVIEW.md` at repo root
(Entwicklungsauftrag 8, dated 2026-09-01): all Carologistics-sourced
secrets/PII were excluded at that time and confirmed to have never
entered this repository. No new scan of already-published `docs/`
content was needed for this pass beyond the residual-term grep already
covered in the migration plan; this audit adds only the two new source
trees (current Spot code, old Spot tutorial images) introduced by this
task.

## Summary

No secret value, password, key, token, or certificate content is
reproduced in this file, in any commit on `feat/alert-spot-tutorial`, or
in any published page. Every category above with real sensitive content
(A: credentials, network config; B: WiFi SSIDs and a manipulator IP
visible in screenshots) is either excluded from migration entirely or
replaced with neutral placeholders before anything reaches `docs/`.
