# -*- coding: utf-8 -*-
u"""pytest for `pykern.pkconfig`

:copyright: Copyright (c) 2015 RadiaSoft LLC.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from __future__ import absolute_import, division, print_function
import dateutil.parser
import py.path
import pytest
import sys

_CHANNEL = 'dev'

_NOT_CHANNEL = 'alpha'


def test_all_modules_in_load_path(monkeypatch):
    """Validate initializing a module"""
    _setup(monkeypatch)
    pkconfig.append_load_path(u'p1')
    pkconfig.append_load_path(u'p2')
    import p1.s1
    assert ['m11', 'm12', 'm13'] == sorted(p1.s1.all_modules().keys())
    import p2.s1
    x = p2.s1.all_modules()
    assert 'p2.s1.m11' == x['m11'].__name__
    assert 'p1.s1.m12' == x['m12'].__name__
    assert 'p2.s1.m13' == x['m13'].__name__


def test_channel_in(monkeypatch):
    """Validate channel_in()"""
    _setup(monkeypatch)
    pkconfig.append_load_path(u'p1')
    assert pkconfig.channel_in(_CHANNEL), \
        'Should match configured channel'
    assert not pkconfig.channel_in(_NOT_CHANNEL), \
        'Should not match configured channel'
    assert pkconfig.channel_in(_NOT_CHANNEL, _CHANNEL), \
        'Should match configured channel'
    with pytest.raises(AssertionError):
        pkconfig.channel_in('bad channel')


def test_flatten_values():
    from pykern.pkconfig import flatten_values
    from pykern import pkcollections

    base = pkcollections.Dict()
    flatten_values(base, {'aa': 1, 'bb': {'cc': 3}})
    assert base['bb_cc'] == 3
    flatten_values(base, {'bb': {'dd': 4}})
    assert base['bb_cc'] == 3
    assert base['bb_dd'] == 4


def test_init(monkeypatch):
    """Validate initializing a module"""
    home = _setup(monkeypatch, dict(P1_M1_BOOL3='', P1_M1_BOOL4='y'))
    pkconfig.append_load_path('p1')
    from p1.m1 import cfg
    assert 'replace1' == cfg['dict1']['d1'], \
        '~/.p1_pkconfig.py should replace dict1[d1]'
    assert 'default2' == cfg['dict1']['d2'], \
        'Nothing should change dict1[d2]'
    assert 'd3' in cfg['dict1'], \
        'd3 should appear in dict1 from the merge in ~/.p1_pkconfig.py'
    assert 'new3' == cfg.dict1.d3, \
        'dict1[d3] should be set to the value in new3'
    assert ['first1', 'second1'] == cfg['list2'], \
        '~/.p1_pkconfig.py should prepend list2'
    assert 55 == cfg['p3'], \
        '~/.p1_pkconfig.py should set p3'
    assert 550 == cfg['p4'], \
        '~/.p1_pkconfig.py should set p4 to 10*p3'
    assert home == cfg['p5'], \
        'environment variables should be visible in formatted params'
    assert dateutil.parser.parse('2012-12-12T12:12:12Z') == cfg['p6'], \
        'pkconfig_base.py sets time value and m1._custom_p6'
    assert 999 == cfg.dynamic_default10, \
        'When value is None, calls parser'
    assert False == cfg.bool1, \
        'When bool1 is none, is False'
    assert True == cfg.bool2, \
        'When bool2 is none, is True'
    pkconfig.reset_state_for_testing()
    assert False == cfg.bool3, \
        'bool3 should be overriden to be False'
    assert True == cfg.bool4, \
        'bool4 should be overriden to be True'


def test_init2(monkeypatch):
    # base_pkconfig is optional so this should ass
    _setup(monkeypatch)
    pkconfig.append_load_path('p2')
    from p2.m1 import cfg


def test_init3(monkeypatch):
    """Validate parse_tuple"""
    home = _setup(monkeypatch, dict(P1_M1_TUPLE3='', P1_M1_TUPLE4='a:b'))
    pkconfig.append_load_path('p1')
    from p1.m1 import cfg
    assert () == cfg.tuple1, \
        'When tuple1 is none, is empty'
    assert (1,) == cfg.tuple2, \
        'When tuple2 is none, is (1,)'
    pkconfig.reset_state_for_testing()
    assert () == cfg.tuple3, \
        'tuple3 should be overriden to be empty'
    assert ("a", "b") == cfg.tuple4, \
        'tuple4 should be overriden to be ("a", "b")'


def test_init4(monkeypatch):
    """Validate parse_set"""
    home = _setup(monkeypatch, dict(P1_M1_SET3='', P1_M1_SET4='a:b'))
    pkconfig.append_load_path('p1')
    from p1.m1 import cfg
    assert set() == cfg.set1, \
        'When set1 is none, is empty'
    assert set([1]) == cfg.set2, \
        'When set2 is none, is (1,)'
    pkconfig.reset_state_for_testing()
    assert set() == cfg.set3, \
        'set3 should be overriden to be empty'
    assert set(('a', 'b')) == cfg.set4, \
        'set4 should be overriden to be ("a", "b")'


def _setup(monkeypatch, env=None):
    # Can't import anything yet
    global pkconfig
    data_dir = py.path.local(__file__).dirpath('pkconfig_data')
    home = str(data_dir)
    monkeypatch.setenv('HOME', home)
    monkeypatch.setenv('PYKERN_PKCONFIG_CHANNEL', _CHANNEL)
    if data_dir not in sys.path:
        sys.path.insert(0, str(data_dir))
    from pykern import pkconfig
    pkconfig.reset_state_for_testing(add_to_environ=env)
    return home
