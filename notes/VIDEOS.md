# Tutorial videos

The tutorial videos are made outside this repository and published on YouTube. This
repository keeps no video files: a question page only links its video. (The earlier Manim
videos, scripts and render tools were removed on 2026-11-14; they are in the git history
before that date.)

## Adding a video to a question

1. Put the YouTube id in the page's front matter: the 11 characters after `v=` in
   `https://www.youtube.com/watch?v=dQw4w9WgXcQ`, or after `youtu.be/`. Quote it when YAML
   could read it as a number or a boolean.

   ```yaml
   video: "dQw4w9WgXcQ"
   ```

2. Optional, on a page with parts (`### סעיף ...`): the start of each part's chapter in
   whole seconds, one per part, from 0 and rising.

   ```yaml
   video_parts: [0, 95, 210]
   ```

3. Run `python tools/build/catalog.py` (the README's video table), then
   `python tools/checks/check_videos.py`, `python tools/checks/lint_pages.py` and
   `mkdocs build --strict`.

## What the page shows

- A "סרטון הסבר" tool first among the page tools, which opens the video in a dialog
  (`docs/javascripts/video.js`, `docs/stylesheets/20-video.css`). Nothing is loaded from
  YouTube until play; the player is `youtube-nocookie.com`.
- With `video_parts`: a "לפרק בסרטון 1:35" link at the top of each part's first solution, and a
  button per chapter in the dialog. Without it: one "לסרטון ההסבר" link at the top of the first
  solution.

## Videos on the site

The list is the README's "Tutorial videos" table, written from the pages by
`tools/build/catalog.py`.
