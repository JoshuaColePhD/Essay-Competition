# Essay Competition Leaderboard

This repository publishes a single-page HTML tool for loading a spreadsheet or Google Sheets URL, analyzing rubric-based essay scores, and displaying the highest-ranked entries in a clean browser dashboard.

## Live Site

https://joshuacolephd.github.io/Essay-Competition/

## Project Description

Essay Competition Leaderboard is a lightweight, browser-based scoring dashboard designed for classroom or competition judging workflows. It lets a teacher, organizer, or judge drag in a spreadsheet or paste a public Google Sheets link and instantly convert rubric data into a ranked leaderboard.

The app is built to work well with Google Forms or exported spreadsheet data. It automatically detects the entry identifier column, finds the rubric score columns, averages scores across all submitted reviews, ranks the results, and highlights the top three entries with both summary cards and a bar graph based on average criterion performance.

Because the app runs entirely in the browser, it is simple to deploy and easy to use. There is no backend, no database, and no separate build step required for the public site. The public repository intentionally exposes only the deployable front end and the documentation, while local datasets and supporting development files stay outside version control.

## What The App Does

- Accepts `.csv`, `.xlsx`, and `.xls` uploads through drag-and-drop or file selection.
- Accepts public Google Sheets URLs and reads sheet data directly in the browser.
- Detects likely student, essay, or entry identifier columns automatically.
- Detects rubric score columns and calculates average results across multiple judges or reviews.
- Ranks all entries and highlights the top three performers.
- Displays a bar graph based on the average of all criteria for each top-ranked entry.
- Shows a full ranked table for quick review of all results.

## Intended Use

This tool is especially useful for essay competitions, classroom writing contests, scholarship reviews, or any scoring process where multiple criteria are rated numerically and several judges may evaluate the same submission.

## Privacy And Repository Scope

This public repository is intentionally minimal. It is meant to publish the live site without exposing potentially sensitive datasets, spreadsheets, source analysis files, or local development artifacts.

## Public Files

- `index.html` contains the full app.
- `README.md` explains the project.

All local datasets, Python scripts, editor settings, and other project files are intentionally kept out of version control.
