# Security

> **This repository is public.**

The material this documentation was built from contained credentials in
cleartext, internal network configuration, and signed URLs carrying
authentication material. None of that is here, and none of it may be
added.

## Never commit

- passwords, keys, tokens or credentials of any kind;
- SSH keys, in any form (public keys included — they identify a host
  or person even without the private half);
- internal IP addresses, hostnames, or network configuration;
- Wi-Fi names or wireless credentials;
- personal names, personal accounts, or other personal data;
- private access instructions (how to reach a specific machine, VPN,
  or internal service);
- signed or expiring URLs;
- private repository links or internal wiki links;
- competition or infrastructure details not already public;
- the raw source material this site was built from (`.gitignore` blocks
  the usual paths — check before adding a new source export).

## Before pushing

Run a scan over what you are about to commit:

```bash
grep -rniE '(password|passwd|secret|api[_-]?key|token|credential)[[:space:]]*[:=]' \
  --include='*.md' --include='*.py' --include='*.yml' --include='*.yaml' .
grep -rnE '\b(10\.|192\.168\.|172\.(1[6-9]|2[0-9]|3[01])\.)[0-9]{1,3}\.[0-9]{1,3}' \
  --include='*.md' .
grep -rnE 'X-Amz-|Signature=|[?&]jwt=|[?&]token=' .
```

`.github/workflows/pages.yml` runs an equivalent scan over the built
HTML on every push and fails the build on a hit — this is a safety net,
not a substitute for checking before you push.

## If a secret is ever committed

Tell the team immediately so it can be rotated. Deleting the commit
does not remove it from clones that already exist, and GitHub's own
history retains it until a full history rewrite and a coordinated
force-push, which is disruptive to every other clone — rotation is
almost always faster and safer than trying to erase the record.

## Limits of the password gate

The published site is wrapped in a static password gate
([StatiCrypt](https://github.com/robinmoisson/staticrypt)) as an access
hurdle, not real server-side authentication:

- The page and all of its assets are still delivered to any visitor's
  browser; StatiCrypt only prevents the encrypted *content* from being
  readable without the password, via client-side decryption in the
  browser.
- StatiCrypt only wraps `.html` files. Static assets — images, CSS,
  JavaScript — are not encrypted and remain directly fetchable at their
  own URL without the password.
- Do not rely on it to keep anything genuinely confidential. Nothing
  confidential is or should be published on this site regardless — see
  "Never commit" above, which applies independently of whether the gate
  exists.
- The `STATICRYPT_PASSWORD` secret is never written to the repository,
  a workflow file, or a build log — it is read only from the GitHub
  Actions secret at deploy time. If it is missing, the deploy step
  fails rather than publishing an unprotected site.

Report a suspected leak, or a StatiCrypt bypass, the same way as any
other secret exposure: immediately, to the team, rather than attempting
a silent fix first.
