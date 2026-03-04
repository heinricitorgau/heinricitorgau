name: Metrics

on:
  schedule:
    - cron: "0 0 * * *"   # run daily
  workflow_dispatch:

permissions:
  contents: write

jobs:
  github-metrics:
    runs-on: ubuntu-latest
    steps:
      - name: Generate GitHub metrics
        uses: lowlighter/metrics@v3.34
        with:
          token: ${{ secrets.GITHUB_TOKEN }}

          filename: github-metrics.svg

          # Base sections (header includes your GitHub bio / intro)
          base: header, activity, community, repositories

          # Language distribution
          plugin_languages: yes

          # Contribution calendar
          plugin_isocalendar: yes

          # Work habits
          plugin_habits: yes

          # Code line statistics
          plugin_lines: yes

          # Repository traffic
          plugin_traffic: yes

          # Achievements
          plugin_achievements: yes

          output_action: commit
          committer_message: "chore: update github metrics dashboard"
