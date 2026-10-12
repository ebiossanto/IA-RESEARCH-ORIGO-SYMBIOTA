# Security policy

## Supported version

Security fixes are applied to the latest released version.

## Reporting

Do not open a public issue for a suspected vulnerability. Send a private report
to the repository owner with:

- affected version and Python version;
- minimal reproducer;
- observed and expected hash behavior;
- possible collision or false-equivalence impact;
- whether untrusted source code is involved.

## Security boundaries

This library parses source code with `ast.parse`; it does not execute the source.
It does not prove semantic equivalence. A matching hash means equality under the
versioned normalization profile only. Consumers must preserve the profile,
Python AST schema, and digest algorithm with the digest.
