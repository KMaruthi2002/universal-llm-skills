# Contributing

Thanks for improving the library. Skills are only useful if they are deep, correct and style-neutral, so please:

1. **Read [docs/SKILL_STANDARD.md](docs/SKILL_STANDARD.md)** and [skills/write-new-skill](skills/write-new-skill/SKILL.md).
2. **Search [CATALOG.md](CATALOG.md) first.** Improving an existing skill beats adding a near-duplicate.
3. **Keep it neutral.** No house styles, mandatory templates, or vendor lock-in. Name tools as examples.
4. **Explain the why.** Rules without reasons don't transfer to new situations.
5. **Validate and regenerate** before committing:

   ```bash
   python3 scripts/validate.py
   python3 scripts/build_catalog.py
   ```

6. Commit the skill together with the regenerated `CATALOG.md`, `catalog.json` and `llms.txt`.

Pull requests that fix factual errors, outdated guidance, or missing pitfalls are especially welcome.
