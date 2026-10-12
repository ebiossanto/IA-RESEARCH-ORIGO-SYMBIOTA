# Origo Alpha AST Hash Profile v1

## Identifier

```text
origo-alpha-ast-v1:python:cpython-ast-X.Y:sha256:<digest>
```

## Normative pipeline

1. Parse source with the CPython `ast` parser.
2. Resolve exactly one function selector.
3. Build lexical scopes and stable binding slots.
4. Replace bound parameter and local names with depth, kind and slot references.
5. Preserve free names, attributes, literals, operators, control flow and sequence order.
6. Remove source positions, formatting and ordinary comments.
7. Serialize the normalized tree as deterministic UTF-8 JSON.
8. Prefix profile metadata and the domain separator `ORIGO\0ALPHA_AST\0V1\0`.
9. Compute SHA-256 and emit the versioned identifier.

## Equivalence boundary

The profile recognizes alpha-structural equivalence. It does not prove behavioral
or semantic equivalence. Captures and references external to the selected
function remain significant by default.

## Compatibility

The Python language version and CPython AST schema are part of the identifier.
A consumer must not compare bare digests produced for different schema versions.
Any incompatible normalization change requires a new profile identifier.

## Determinism requirements

- map serialization uses sorted keys;
- lists retain source/AST order;
- node fields retain explicit names;
- numeric values use deterministic encodings;
- source coordinates never enter the digest;
- errors must not fall back to approximate hashing.
