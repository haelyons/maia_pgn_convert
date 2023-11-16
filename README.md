## PGN Convert (Chessbase, Lichess, Maia)

This is a disconnected fork of nas5w's [pgn-converter](https://github.com/nas5w/pgn-converter). I decided not to open a pull request
as the intent here is specifically to convert between Chess.com PGNs and the LichessDB format (a subset of the standard Lichess format)
in order to use Chess.com games as training data to fine-tune the [maia-individual model](https://github.com/CSSLab/maia-individual)

## Installation

Clone down the repository:

```bash
git clone git@github.com:haelyons/maia_pgn_convert.git
```

`cd` into the directory and run the converter

```bash
python convert.py
```

You should see an output explaining that there are no files to be converted.

```
-----
No new lichess to chessbase files.
-----
No new chessbase to lichess files.
-----
No new chesscom to lichess files.
```

## Converting files

Convert files by entering them into the relevant directory based on your needs. Converting from lichess-to-chesscom for example:
`lichess-to-chesscom/input`
Sample games have been included with the express permission of the player. Alternates can easily be found by accessing [OpeningTree](https://www.openingtree.com/) and entering the name of the user you wish to select the games of. 