# Episode 04-playlist-plus: The Final Showdown.
--
**Build a playlist generator that exposes a 'hint' parameter allowing the user to suggest titles. This is achieved by importing a string edit distance package using Metaflow's conda based dependency management feature. Dependency management builds isolated and reproducible environments for individual steps.**

--

#### Before playing this episode:
This tutorial uses a Pandas Dataframe. If you don't already have pandas installed you can try: ```python -m pip install pandas```

This tutorial requires the 'conda' package manager to be installed. Please visit 'https://docs.conda.io/projects/conda/en/latest/user-guide/install/download.html' to download 'conda'.

#### Showcasing:
- Metaflow's conda based dependency management.

#### To play this episode:
1. ```cd metaflow-tutorials```
2. ```python 04-playlist-plus/playlist.py --environment=conda show```
3. ```python 04-playlist-plus/playlist.py --environment=conda run```
4. ```python 04-playlist-plus/playlist.py --environment=conda run --hint "Data Science Strikes Back"```