# MazeGen

Maze generation part two.

This project is an older and wiser me's revamp of my original maze generation project [pymaze](https://github.com/GrandMoff100/Mazes).'

This time I've got more algorithms, and you can export them to PDF's now.

## Motivation

The last project was terminal-centric and I needed a way to export the mazes to PDF's, but it's infrastructure and design was too rigid to allow for that. So I started from scratch and made this project.
This time we're using `networkx` to manage the maze data and `matplotlib` for rendering and PDF exporting.
Now I can generate a whole bunch of mazes and export them to a PDF.

## Usage

Clone the repo.
Setup a virtual environment.
Activate it and install the requirements with `poetry`.
Then run `main.py` to generate 500 mazes and export them to a PDF called `mazes.pdf`.

Tweak `main.py` how you like!

## License

MIT License
