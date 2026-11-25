# FOGGYStreams OBS

Official FOGGYStreams OBS Overlays, Widgets And Scene Collections.

## Overlay Hub

https://iillifoggyiilli.github.io/FOGGYStreams-OBS/

## Available Packs

- GTA VI / Vice City Broadcast v1.4: 12 scenes, 17 hosted sources, 1920 × 1080, ten-minute Starting Soon timer, timer-free BRB, no webcam.

- WWE 2K26 / Ringside Broadcast v1.0: 15 scenes, 20 hosted sources, editable match cards, results and championship spotlight. Includes 10-minute start, timer-free BRB and no webcam.

DayZ, FiveM, BeamNG.drive and Universal packs are planned.

## Setup

Import the JSON from downloads/ or copy individual Browser Source URLs from the control room. Add gameplay and audio capture in OBS. Use the existing Twitch alert browser source for automatic alerts. Manual alerts and goals use browser-local storage; test dock synchronisation first. No Python server, BAT file or extra desktop application required. The old GTA VI website remains unchanged. Do not commit Twitch credentials or private alert URLs.

## GitHub Pages

In Settings → Pages, choose GitHub Actions as the source. Run the Publish FOGGYStreams OBS workflow if necessary. The workflow validates the overlay script and scene references before deployment.

## Artwork

Hub images link to publisher Steam artwork, Rockstar's GTA VI screenshot gallery and the FiveM logo on Wikimedia Commons. The Universal card uses original branding. No publisher affiliation is implied. Remote artwork may change; fallback titles are provided.

## WWE Ringside Production 2.0

21 scenes, 26 browser sources, match format library, saved event rundown, 4/8/16 entrant brackets, Rumble/Gauntlet tracker, mystery reveals, preview of published graphics and Program Output. Manual game data; test OBS dock synchronisation first. Portraits are optional authorised HTTPS URLs.

## Ringside Production 3.0 — Broadcast Graphics

Portrait-led 1080p match graphics, theme-specific palettes, mirrored tournament layouts and compact Royal Rumble lower thirds with entry/elimination notices and manual countdowns. Eight official WWE profile images linked from WWE.com (not game renders; may depict real-world belts), plus custom roster artwork. Demo URLs never affect Program Output. Existing OBS v2.0 collection URLs remain compatible. Research: https://www.wwe.com/article/2025-king-queen-of-the-ring-tournament-bracket ; https://awfulannouncing.com/wwe/royal-rumble-new-lower-third-graphic-ticker.html ; https://www.wwe.com/shows/raw/2025-03-31/article/jimmy-uso-takes-on-gunther ; https://www.wwe.com/shows/smackdown/2025-02-21/article/cody-rhodes-damian-priest-braun-strowman-vs-solo-sikoa-jacob-fatu . Unofficial fan-created graphics; not WWE's proprietary broadcast package.

## WWE 3.1 — Customisation

Free-text match type/format with suggestions, per-match on-air heading and descriptions, custom result fields, portrait URL per entrant, editable global broadcast captions, per-scene text and colour overrides, duplication, editable tournament and Rumble entrants without reset, all-at-once elimination tracking. Changes are saved backstage until applied; browser storage and OBS dock sync are still required.

## WWE 3.2 — Automatic Portraits

Searchable roster picker for match cards, tournaments and Rumbles; automatic normalized/alias lookup, portrait previews, and manual artwork overrides. Built-in WWE profile images include The Miz, Jeff Hardy, Chad Gable and Rey Fenix. The build indexes public image links from https://www.thesmackdownhotel.com/wwe2k26/roster/ and https://www.wwe.com/superstars. Portraits are externally hosted and not all game variants are guaranteed. Source rights remain with their respective owners. The importer is best-effort and logs its actual count in Actions.

## WWE 3.3 — Roster gallery and artwork coverage

Uses the game-roster index that previously returned 512 links. Each link is checked for image content; coverage is published in `wwe-2k26/roster-coverage.json` and GitHub Actions. Editor includes a searchable visual gallery, direct portrait selection, entrant editing, ordering and mystery flags. Penta and Drew McIntyre are included alongside The Miz, Jeff Hardy, Chad Gable and Rey Fenix. External artwork remains on its original hosts; an HTTP check does not guarantee exact in-game attire. OBS URLs and saved shows remain compatible.
