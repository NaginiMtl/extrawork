# Kiwili redesign: project handoff

This file carries the context of the original Claude Code session so a new session (for example in a team Claude account) can continue without the chat. Read it first.

## 1. Goal

Redesign kiwili.com (French, Québec ERP for project-based service businesses) to look modern and consistent with current SaaS sites. The first pass covers the homepage, a design system page and one help article. Output is static HTML, CSS and JS with no build step.

## 2. Versions, branches, links

| What | Branch | Commit | Preview (private to the original account) |
|---|---|---|---|
| v1 homepage (frozen) | `claude/keen-fermat-ommrjd` | `9d42cb5` | https://claude.ai/artifact/VYVvemnqGtgAPAjANSJhQX |
| v2 homepage | `claude/kiwili-v2` | see `git log` | https://claude.ai/artifact/2r7wuzz47oKt5FXeB4J7jR |
| Tutorial: gestion des droits d'accès | `claude/kiwili-v2` | `2a74e04` and later | https://claude.ai/artifact/MMLfnzVhemmqxTesmmuSyB |

- Final home: the company repository `Kiwili-com/website` (https://github.com/Kiwili-com/website). The work was built in a personal working repository, `NaginiMtl/extrawork`, because the cloud session had no access to the company repo. Branch names above refer to `NaginiMtl/extrawork`. The steps to copy them to the company repo are in section 12.
- Never push new work to the v1 branch.
- Git tags could not be pushed from the cloud session (the push failed three times). Branches and commits are the saved copies. See `VERSIONS.md`.
- The preview links belong to the original account. Share them from each page's Share menu, or republish from the new account (see section 9).

## 3. Design decisions (the client's words in quotes)

- Fonts: Bricolage Grotesque for titles (real Google Fonts name; the client said "Bricolage Sans"), Inter for text.
- Reference: Linear. Dark first, hairline borders, tight type. A light theme exists with a toggle (it follows the system by default).
- Keep the Kiwili logo. Palette is built from the logo's three bars: blue (lead), green, orange. Each module and feature gets one of the three colours. Buttons use a slightly darker blue so white text stays readable.
- "It does not look like AI generated but a HIGH QUALITY website. Same with the content. Nothing that could tell it is AI generated." So: no pill with a glowing dot, no generic gradient blobs, no emoji, no invented marketing claims, no em dashes in the copy, Québec French, real numbers only.
- Hero headline: "Gérez votre entreprise sur une seule plateforme". The word "seule" has no accent colour: "put it white like the rest".
- No card around the centralisation diagram. The closing sections (demo, trial, footer) are dark bands in both themes. A light FAQ section sits between the demo band and the trial band.
- Photos must be professional people. The client wanted human faces, like HubSpot's homepage.
- The Claude section must not say "il lit votre compte Kiwili". People may fear for their security. Title is now "Posez vos questions en français. Claude vous répond."
- Mention Claude only, not ChatGPT/GPT, for now.
- Working agreement: for larger changes, tell the client the plan before building. Small requests can be done directly.

## 4. Homepage v2: section order and behaviour

1. Nav (dropdown under "Fonctionnalités", mobile menu, theme toggle). No language switch.
2. Hero: headline with word-by-word reveal, audio player top right with a hand-drawn orange arrow and "Écoutez-nous" (`assets/audio/presentation-kiwili.mp3`, 16 s, ElevenLabs voice, waveform drawn from the real file), a tabbed interactive dashboard (Tableau de bord, Facturation, Projets, Budgets, Temps) that plays once then stops, with a pause button.
3. Press names (text placeholders).
4. "Votre métier": five expanding photo cards (Architectes, Ingénieurs, OBNL, Construction, Designers).
5. Module cards (Comptabilité, Devis, Facturation, Bons de commande, Dépenses, Suivi du temps).
6. "Demandez à Claude": clickable example conversations with confirmation cards (sample data).
7. "Du devis à la comptabilité, sans changer d'outil": scroll-pinned story where one document changes from quote to purchase order to project to invoice to accounting entries. On phones or reduced motion it becomes tappable chips.
8. Four feature rows (projects, resource planning, budgeting, centralisation diagram with moving data dots).
9. "Kiwili travaille avec vos autres outils": Zapier column and API column (real request example).
10. Demo band (client's own photo), FAQ, trial band with the animated logo mark, footer.

Motion is off for visitors who prefer reduced motion.

## 5. Facts and sources used (do not invent beyond these)

- Homepage copy comes from the live site. "150 000 clients", "4,9 sur Google" and "14 jours d'essai sans carte de crédit" are taken from it.
- Claude connection (from the client's PDF "La connexion Claude AI à Kiwili"): MCP connector at `https://mcp.kiwili.com/mcp`. Reads invoices, quotes, expenses, purchase orders, accounting, projects, tasks, timesheets. Creates or changes things only after confirmation. No API token needed. The connector keeps no business data. Access can be removed by the user or an administrator. All plans include API access, including the free trial. Conditions of connectors in Claude depend on the Claude subscription.
- API: https://api.kiwili.com/api/openapi/ (OpenAPI 3.1, server `https://{account}.kiwili.com/api`, bearer token, webhooks, daily call limits by plan). The example `GET /invoice/` exists in the spec.
- Zapier: https://zapier.com/apps/kiwili/integrations lists instant triggers (for example invoice updated, invoice payment created, contact created) and actions (create invoice, contact, project, task, time entry, payment). "9 000+ applications" is Zapier's own figure.
- Tutorial text comes from https://www.kiwili.com/fr/Blog/post/gestion-des-droits-dacces-dans-kiwili/ (rewritten for layout, meaning unchanged). The five screenshots are Kiwili's own images, resized to WebP in `assets/tuto/`.
- Real Kiwili URLs for métiers pages, help articles, the signup page and others were read from the live site's navigation. They are used in the tutorial sidebar and "Aller plus loin".

## 6. Photos

All from Unsplash (free commercial use, no attribution needed). They are stock photos, never labelled as customers. Photo IDs:

- Architectes `1503387762-592deb58ef4e`
- Ingénieurs `1581091226825-a6a2a5aee158`
- OBNL `1517486808906-6ca8b3f04846`
- Construction `1621905251189-08b45d6a269e`
- Designers `1552664730-d307ca884978`

The demo photo (`assets/photos/demo-expert.*`) was supplied by the client. If the client has real customer photos, swap them in.

## 7. Tutorial page (`tutoriel.html`)

Layout follows Asana's help article: global nav plus a "Centre d'aide" bar, left "Sujets" tree with the current article highlighted, breadcrumb, title, "Dans cet article" list, a "Qui peut utiliser cette fonctionnalité ?" box, sections, related articles, helpful/not helpful question. Added: a filterable accordion of the 24 access rights grouped by domain, deep links per right, restricted-versus-admin screenshot tabs, a reading-progress line. The generator is `tools/gen_tutorial.py` (reads the header and footer from `index.html`).

## 8. Open items and placeholders

- Sample data everywhere (hero dashboard, chat conversations, Zapier example, "Cabinet Archi") is invented and should be checked or replaced.
- Press names are text, not logos. No customer quotes, case studies or pricing yet. The "Tarifs" link has no page.
- Module card descriptions, métier card descriptions, FAQ answers beyond the ones taken from the PDF, and the footer text were written for this prototype. Review them against the real product.
- Forms ("Essai gratuit", demo, feedback buttons) are front-end only and send nothing. A marked TODO is in `js/main.js`.
- The métier cards, module cards and "En savoir plus" links point to `#` or sections. There are no per-métier pages yet. Real métier URLs exist on kiwili.com (architectes, ingénieurs, construction, OBNL, design intérieur, comptables, agences marketing, entreprises de services).
- The tutorial row "Transferts de fonds électroniques" under Comptabilité was omitted because the source text gives no access status. Ask the client.
- Tutorial sidebar group names ("Ventes et achats", "Finances"...) are invented.
- The audio transcript was removed on request. The audio is the only version of that message.
- Not built yet: other pages, the English version, mobile checks on real devices, accessibility audit, speed test.
- The FAQ contains two security-related Claude questions. The client was cautious about security wording. Revisit if needed.

## 9. How to run and publish

- No build step. Open `index.html` in a browser, or serve the folder with any static server.
- Single-file previews for Claude "Artifacts" are generated by `tools/build_homepage.py` and `tools/build_tutorial.py` into `dist/` (git-ignored). They inline CSS, JS and images, because artifacts block external images. To publish, publish `dist/kiwili-v2.html` (and `dist/kiwili-tutoriel.html`) with the Artifact tool, passing `design-system.html` as a supporting file. Publishing the same file path updates the same link. A new path creates a new link.
- Artifacts only allow external scripts from a few CDNs and stylesheets only from Google Fonts. Audio and images must be embedded as data URIs.

## 10. Environment gotchas (cloud session)

- Outbound network is limited by an egress proxy. At first kiwili.com, hubspot.com and others were blocked; the client changed the environment's Network access setting (cloud environment menu in the session title bar, then Edit) and it worked.
- Headless Chromium rejected the proxy's certificates (`ERR_CERT_AUTHORITY_INVALID`). A working method: create a Playwright context and route every request through `route.fetch()` and `route.fulfill()`, so Node's trusted TLS makes the request. Do not disable certificate checks.
- Google Fonts is unreachable from the sandbox. Screenshots used local copies of the fonts from `@fontsource-variable/*` packages.
- `git push` of tags fails in this environment. Pushing branches works.

## 11. To continue in a new session

1. Give the new session access to the repo that holds the work (`Kiwili-com/website` once the branches are copied, otherwise `NaginiMtl/extrawork`) and check out the v2 branch (`claude/kiwili-v2`, or `redesign-v2` if you used the names in section 12).
2. Tell it to read `HANDOFF.md` and `VERSIONS.md` first.
3. Ask it to confirm the plan before large changes (the client's preference).

## 12. Copying the work into the company repo (manual steps)

The Claude session could not attach `Kiwili-com/website` (no access for its GitHub connection), so the copy has to be done by someone who can push to both repositories.

```bash
git clone https://github.com/NaginiMtl/extrawork.git kiwili-redesign
cd kiwili-redesign
git remote add company https://github.com/Kiwili-com/website.git

# v1 = frozen first version, v2 = current work (homepage, tutorial, HANDOFF.md, tools/)
git push company claude/keen-fermat-ommrjd:redesign-v1
git push company claude/kiwili-v2:redesign-v2

# optional: tags (these could not be pushed from the cloud session)
git tag v1-homepage 9d42cb5
git tag v2-homepage 2928054
git push company v1-homepage v2-homepage
```

Notes:

- These push new branches only. The default branch of the company repo is not touched. Choose other branch names if the team has a convention.
- `NaginiMtl/extrawork` is private. The person running the commands needs read access to it as well as push access to the company repo.
- On 2026-10-07 `Kiwili-com/website` was empty (no commits, so no default branch yet). That means there are no file clashes today, and the first push creates the first branch. If you want the v2 work to become the starting point of the repo, push it as `main` instead (`git push company claude/kiwili-v2:main`). Check the repo again before pushing, in case someone has added files since.
- Otherwise, the branches have their own history, unrelated to the company website's history. To bring the pages into the real site, copy the files into the right folder of the website instead of merging. Check for name clashes first: this prototype uses `index.html`, `tutoriel.html`, `design-system.html`, `css/`, `js/`, `assets/` and `tools/` at its root.
- After the copy, change the "Final home" line in section 2 and the table in `VERSIONS.md` if the branch names differ.
