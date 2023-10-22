from pathlib import Path
from pyformlang.cfg import CFG, Variable
from typing import Union


def cfg_to_wcnf(cfg: Union[str, CFG], start: Union[str, None] = None) -> CFG:
    if start is None:
        start = "S"
    if not isinstance(cfg, CFG):
        cfg = CFG.from_text(cfg, Variable(start))
    cfg_new = (
        cfg.remove_useless_symbols()
        .eliminate_unit_productions()
        .remove_useless_symbols()
    )
    return CFG(
        start_symbol=cfg_new._start_symbol,
        productions=set(
            cfg_new._decompose_productions(
                cfg_new._get_productions_with_only_single_terminals()
            )
        ),
    )


def read_cfg(path: Path, start: str = "S") -> CFG:
    with open(path, "r") as file:
        data = file.read()
    return CFG.from_text(data, Variable(start))
