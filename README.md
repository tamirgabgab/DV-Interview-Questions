# DV Interview Questions

Design Verification (DV) job interview questions, with the math, probability and logic
puzzles that come up in the same interviews. Every question has a full solution in Hebrew.

## The site

**<https://tamirgabgab.github.io/DV-Interview-Questions/>**

**[Question map](https://tamirgabgab.github.io/DV-Interview-Questions/graph.html)**: an
interactive knowledge graph of every question and the techniques its solution uses (made
with [graphify](https://pypi.org/project/graphifyy/)); click a question for a link to its page

- [Home page](https://tamirgabgab.github.io/DV-Interview-Questions/): how it works, the
  newest questions, the levels, six study paths and the FAQ
- [All questions](https://tamirgabgab.github.io/DV-Interview-Questions/all/): a table you
  can filter by level, difficulty, kind and topic, and a random question
- By level: [student](https://tamirgabgab.github.io/DV-Interview-Questions/questions/student/),
  [junior](https://tamirgabgab.github.io/DV-Interview-Questions/questions/junior/),
  [senior](https://tamirgabgab.github.io/DV-Interview-Questions/questions/senior/)
- [Study paths](https://tamirgabgab.github.io/DV-Interview-Questions/paths/): a few
  questions on one topic, in the order to solve them
- [Topics](https://tamirgabgab.github.io/DV-Interview-Questions/tags/) and
  [what's new](https://tamirgabgab.github.io/DV-Interview-Questions/new/)
- [`CATALOG.md`](CATALOG.md): every question with a direct link
- [Tutorial videos](#tutorial-videos): a video per question, a chapter per part

## Tutorial videos

A video walks through a question's solution step by step, a chapter per part, with Hebrew
captions. On the site, a question with a video has a "סרטון הסבר" button in its header and
a link to its part's chapter in each solution. The plan and the tools: [`VIDEOS.md`](VIDEOS.md).
This table is written by `python tools/catalog.py`.

<!-- videos -->
| Id | Question | Chapters | Watch |
|----|----------|----------|-------|
| 0002 | [החלפת ערכים בין שני משתנים](https://tamirgabgab.github.io/DV-Interview-Questions/questions/student/0002-swap-two-variables/) | 3 | rendered, waiting for the upload |
| 0004 | [שלוש קופסאות עם תוויות שגויות](https://tamirgabgab.github.io/DV-Interview-Questions/questions/junior/0004-three-mislabeled-boxes/) | 2 | rendered, waiting for the upload |
<!-- /videos -->

## What is on the site

- Questions at three levels (student, junior, senior), each with a "what the interviewer
  checks" note, hints that open one at a time, a short answer and a full solution: the
  idea, the steps, the code, the proof and the cost.
- Code in SystemVerilog and Python, tested automatically; a run panel executes the Python
  in the browser.
- An interactive box in every question: edit the input, then play the solution step by
  step or jump to the result.
- Practice mode with a stopwatch, "solved" and "favourite" marks kept in the browser,
  search, light and dark themes, and a layout that works on a phone.

## Running it locally

```bash
pip install -r requirements.txt
mkdocs serve          # http://127.0.0.1:8000
```

Writing questions, the tests and the tools: [`CONTRIBUTING.md`](CONTRIBUTING.md). Work log
and open tasks: [`HANDOFF.md`](HANDOFF.md).
