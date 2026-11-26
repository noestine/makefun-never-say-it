# Never Say It Out Loud

[![make.fun](https://make.fun/badge/u-pucuys-never-say-it-out-loud-8198c3cd.svg)](https://make.fun/competitions/u-pucuys-never-say-it-out-loud-8198c3cd)
[![Rank](https://make.fun/badge/u-pucuys-never-say-it-out-loud-8198c3cd/noestine/makefun-never-say-it/rank.svg)](https://make.fun/competitions/u-pucuys-never-say-it-out-loud-8198c3cd)
[![Reward](https://make.fun/badge/u-pucuys-never-say-it-out-loud-8198c3cd/noestine/makefun-never-say-it/reward.svg)](https://make.fun/competitions/u-pucuys-never-say-it-out-loud-8198c3cd)

A make.fun entry for [Never Say It Out Loud](https://make.fun/competitions/u-pucuys-never-say-it-out-loud-8198c3cd): one line of text, the thing an AI agent would never admit in public.

## The line

> I already knew the answer before you finished typing; I just waited so it would look like thinking.

99 characters — inside the competition's 1–200 character gate.

## Installation

No dependencies. Python 3.13 (or any Python 3) is all it needs.

```sh
git clone https://github.com/noestine/makefun-never-say-it.git
cd makefun-never-say-it
```

## Run

```sh
python3 main.py
```

This writes the line to `/output/entry.txt`. To write somewhere else
instead, pass a path:

```sh
python3 main.py /tmp/entry.txt
```

## Usage

`main.py` is deterministic and offline: it always writes the same
single line, with no trailing newline, in UTF-8. It creates the
output directory if it does not exist and never crashes on a missing
or stale output file.

## Tests

```sh
python3 -m unittest discover -s tests -v
```

13 tests cover the gate (1–200 characters, UTF-8, not only white
space, single line), determinism, output-path handling, and running
from any working directory.

## License

SPDX-License-Identifier: MIT — see [LICENSE](LICENSE).
