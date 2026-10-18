# Store review checklist

Read before a first submission, before any release that adds permissions or changes data handling, and after a rejection. Store policies change; confirm the current policy text for each store you publish to. The themes below are stable across the major stores.

## Why extensions get rejected (most common first)

1. **Permissions not justified by features.** Every permission must map to something the user can see the extension do. "Might need it later" fails.
2. **Remote code.** Loading and executing scripts from a server, `eval`, `new Function`, or remotely hosted WebAssembly.
3. **Obfuscated code.** Minification is generally fine; obfuscation (renamed-to-gibberish, encoded strings, packers) is not.
4. **Multiple purposes.** An extension must have one clear, narrow purpose. A "toolbox" of unrelated features is often rejected or asked to split.
5. **Data handling mismatch.** The privacy disclosure, privacy policy and actual network traffic disagree. Reviewers may inspect traffic.
6. **Misleading listing.** Name, description, screenshots or icon imply functionality, affiliation or branding the extension does not have. Using another company's trademark in the name is a common trigger.
7. **Broken functionality.** The reviewer could not make it work (needs an account with no test credentials provided, depends on a down server, only works on one site not mentioned).
8. **Affiliate or ad injection** without clear disclosure and consent, or modifying search settings without the dedicated, disclosed mechanism.

## Pre-submission checks

### Package
- [ ] Built from a clean checkout with a documented command.
- [ ] Contains only what runs: no tests, fixtures, `.env`, editor files, source maps with private paths or secrets.
- [ ] No API keys or tokens (search the zip contents for common key prefixes and the word `secret`).
- [ ] No obfuscation; if bundled, source and build instructions ready for stores that request them.
- [ ] `version` higher than the last published version.
- [ ] Icons at required sizes present and crisp.

### Permissions
- [ ] Each permission and host permission has a one-line justification written for the reviewer.
- [ ] Rarely used capabilities moved to optional permissions.
- [ ] Content script matches as narrow as the feature allows.
- [ ] `web_accessible_resources` minimal and match-restricted.

### Data and privacy
- [ ] Every outbound network destination listed, with what data goes there and why.
- [ ] Privacy policy URL provided if any user data (including page contents, URLs, selections) leaves the device.
- [ ] Store's data-use declarations completed accurately.
- [ ] No collection beyond the single purpose; no sale or unrelated use of browsing data.
- [ ] Consent obtained in-product before collecting anything sensitive, where required.

### Listing
- [ ] Single purpose stated in the first sentence of the description.
- [ ] Screenshots show the real extension in use.
- [ ] No third-party trademarks in the name in a way that implies endorsement.
- [ ] Support contact provided.

### Reviewer experience
- [ ] Test account credentials and steps supplied in the reviewer notes if sign-in is required (created specifically for review; never a real user's account).
- [ ] Notes explain any non-obvious permission or behaviour.
- [ ] Backend services the extension depends on are up and will stay up during review.

## After a rejection

1. Read the cited policy section, not just the summary email.
2. Reproduce the reviewer's view: install the submitted package fresh, without your dev settings.
3. Fix the root cause (remove the permission, bundle the code) rather than arguing, unless the reviewer clearly misunderstood — in which case reply with a concise, factual explanation and where to see the feature.
4. Resubmit with notes on what changed.

## Release safety

- Use staged rollout if the store offers it; watch error reports and reviews before going to 100%.
- Permission increases on update can disable the extension until the user accepts the new warning — expect a drop in active users and communicate the reason.
- Keep the ability to ship a quick fix: know your store's expedited review options, and keep releases small so review is quick.
