# Security Policy

Adiuvare is an early-stage security project. If you believe you have found a
security vulnerability, please do **not** open a public GitHub issue with
exploit details.

## Supported versions

Security fixes are currently handled on a best-effort basis for:

| Version | Supported |
| --- | --- |
| latest `main` branch state | yes |
| latest tagged `0.x` release | yes |
| older snapshots and historical commits | no guarantee |

## How to report a vulnerability

Please use a private disclosure path first.

Preferred route:

- use GitHub private vulnerability reporting for this repository if it is available

Fallback route:

- contact the maintainer through GitHub and ask for a private reporting channel
- do not include full exploit details in a public issue, discussion, or comment

If you are unsure whether something is security-sensitive, err on the side of
private disclosure first.

## What to include

Helpful reports usually include:

- affected version, branch, or commit
- impacted framework or integration path
- clear reproduction steps
- proof-of-concept payload or request shape
- expected behavior vs actual behavior
- impact assessment
- any suggested mitigation if you already have one

If the issue depends on configuration, include the relevant config shape with
secrets removed.

## What happens next

When a report is confirmed, the usual flow is:

1. reproduce and validate the issue
2. assess scope and impact
3. prepare a fix
4. publish the fix and any needed guidance

Response times are best effort. Adiuvare is an early-stage open-source project,
so there is no formal SLA yet.

## Scope notes

Please use normal bug reports for:

- false positives that do not create a security bypass
- docs mistakes
- feature requests
- non-sensitive runtime bugs

Use private disclosure for things like:

- bypasses that defeat a guard path or expected stop/hold behavior
- ways to trigger unauthorized control-plane effects
- trust boundary mistakes
- secrets exposure
- anything that would put a real deployment at risk if disclosed publicly first
