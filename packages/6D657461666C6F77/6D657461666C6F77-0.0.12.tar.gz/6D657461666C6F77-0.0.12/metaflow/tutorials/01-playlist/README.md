# Episode 01-playlist: Let's build you a movie playlist.
--
**This flow loads a movie metadata CSV file and builds a playlist for your favorite movie genre. You can run it multiple times and view all the historical playlists with the Metaflow client in a Notebook, since everything in Metaflow is versioned.**

--

#### Before playing this episode:
This tutorial uses a jupyter notebook to view the results from running PlayListFow. If you don't already have something installed, you can try: ```python -m pip install jupyter```

#### Showcasing:
- Including external files with 'IncludeFile'.
- Basic Metaflow Parameters.
- Running workflow branches in parallel and joining results.

#### To play this episode:
1. ```cd metaflow-tutorials```
2. ```python 01-playlist/playlist.py show```
3. ```python 01-playlist/playlist.py run```
4. ```python 01-playlist/playlist.py run --genre comedy```
5. ```jupyter-notebook 01-playlist/playlist.ipynb```
