import os

from project.cfg_utils import cfg_to_wcnf, read_cfg
from scripts import shared


def test_cfg_utils_1() -> None:
    cfg = (
        read_cfg(
            str(shared.ROOT)
            + os.sep
            + "tests"
            + os.sep
            + "output"
            + os.sep
            + "task_6"
            + os.sep
            + "cfg1.txt"
        )
        .eliminate_unit_productions()
        .remove_useless_symbols()
    )
    assert cfg_to_wcnf(cfg).productions == set(cfg.productions)


def test_cfg_utils_2() -> None:
    cfg = (
        read_cfg(
            str(shared.ROOT)
            + os.sep
            + "tests"
            + os.sep
            + "output"
            + os.sep
            + "task_6"
            + os.sep
            + "cfg2.txt",
            "S",
        )
        .eliminate_unit_productions()
        .remove_useless_symbols()
    )
    wcnf_1 = cfg_to_wcnf(cfg)
    wcnf_2 = cfg_to_wcnf(cfg, "S")
    wcnf_3 = cfg_to_wcnf(cfg, "A")
    assert wcnf_1.productions == set(cfg.productions) and wcnf_1._start_symbol == "S"
    assert wcnf_2.productions == set(cfg.productions) and wcnf_2._start_symbol == "S"
    assert wcnf_3.productions == set(cfg.productions) and wcnf_3._start_symbol == "S"


def test_cfg_utils_3() -> None:
    cfg = (
        read_cfg(
            str(shared.ROOT)
            + os.sep
            + "tests"
            + os.sep
            + "output"
            + os.sep
            + "task_6"
            + os.sep
            + "cfg3.txt",
            "A",
        )
        .eliminate_unit_productions()
        .remove_useless_symbols()
    )
    assert cfg_to_wcnf(cfg).productions == set(cfg.productions)


def test_cfg_utils_4() -> None:
    cfg = (
        read_cfg(
            str(shared.ROOT)
            + os.sep
            + "tests"
            + os.sep
            + "output"
            + os.sep
            + "task_6"
            + os.sep
            + "cfg4.txt",
            "S",
        )
        .eliminate_unit_productions()
        .remove_useless_symbols()
    )

    wcnf = (
        read_cfg(
            str(shared.ROOT)
            + os.sep
            + "tests"
            + os.sep
            + "output"
            + os.sep
            + "task_6"
            + os.sep
            + "wcnf4.txt",
            "S",
        )
        .eliminate_unit_productions()
        .remove_useless_symbols()
    )
    assert cfg_to_wcnf(cfg).productions == set(wcnf.productions)


def test_cfg_utils_5() -> None:
    cfg = (
        read_cfg(
            str(shared.ROOT)
            + os.sep
            + "tests"
            + os.sep
            + "output"
            + os.sep
            + "task_6"
            + os.sep
            + "cfg5.txt",
            "S",
        )
        .eliminate_unit_productions()
        .remove_useless_symbols()
    )
    print(cfg_to_wcnf(cfg).productions, len(cfg_to_wcnf(cfg).productions))
    wcnf = read_cfg(
        str(shared.ROOT)
        + os.sep
        + "tests"
        + os.sep
        + "output"
        + os.sep
        + "task_6"
        + os.sep
        + "wcnf5.txt",
        "S",
    ).eliminate_unit_productions()
    print(set(wcnf.productions), len(set(wcnf.productions)))
    assert cfg_to_wcnf(cfg).productions == set(wcnf.productions)
