
# Web of Science notes
- Some citations in the `wos_reference` table have a `.` in the name. these are not valid identifiers

- Some citations in the `wos_reference` table use `MEDLINE:` and `BCI:` prefixes instead of `WOS:`.

- It is unclear whether journals are listed by print or online ISSNs

- some citation identifiers appear to have return characters or there is an 80-char truncation in `psql` output