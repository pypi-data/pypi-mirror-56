#!/usr/bin/env python3
# 
# slotmachine_oneline.py
# Copyright (C) 2019  Miguel de Dios Matias
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
import json
from random import randint
from appdirs import user_config_dir

line = '{symbol1}{symbol2}{symbol3}{money}💵'
symbols = ['🍇', '🍋', '🍉', '🍒', '⭐']

combinations = {
    '000': 1, #🍇🍇🍇
    '111': 2, #🍋🍋🍋
    '222': 4, #🍉🍉🍉
    '333': 15, #🍒🍒🍒
    '444': 100} #⭐⭐⭐

wilcardCombination =  {
    'xx3': 5, #xx🍒
    'x33': 10} #x🍒🍒

initMoney = 10

def formatMoney(money):
    formatedMoney = money
    if money < 0:
        formatedMoney *= -1
    
    if formatedMoney < (10**3):
       pass 
    elif formatedMoney > (10**3 - 1):
        formatedMoney = "{}K".format(int(formatedMoney / 10**3))
    elif formatedMoney > (10**6 - 1):
        formatedMoney = "{}M".format(int(formatedMoney / 10**6))
    elif formatedMoney > (10**9 - 1):
        formatedMoney = "{}G".format(int(formatedMoney / 10**9))
    elif formatedMoney > (10**12 - 1):
        formatedMoney = "{}T".format(int(formatedMoney / 10**12))
    elif formatedMoney > (10**15 - 1):
        formatedMoney = "{}P".format(int(formatedMoney / 10**15))
    else:
        formatedMoney = 'INF'
    
    if money < 0:
        formatedMoney = '-{}'.format(formatedMoney)
    return formatedMoney

def slotmachine(pl, *arg, **kwarg):
    configPathfile = os.path.join(user_config_dir(), 'powerline_slotmachine.json')
    try:
        with open(configPathfile) as configFile:
            config = json.load(configFile)
    except FileNotFoundError:
        config = {'money': initMoney,
            'combination': '000'}
        money = initMoney
        symbol1 = 0
        symbol2 = 1
        symbol3 = 2
    else:
        money = config['money'] - 1
        symbol1 = randint(0, len(symbols) - 1)
        symbol2 = randint(0, len(symbols) - 1)
        symbol3 = randint(0, len(symbols) - 1)
    
    combination = '{}{}{}'.format(symbol1, symbol2, symbol3)
    tempCombination = 'x{}{}'.format(symbol2, symbol3)
    tempCombination2 = 'xx{}'.format(symbol3)
    
    if combination in combinations.keys():
        money += combinations[combination]
    elif tempCombination in wilcardCombination.keys():
        money += wilcardCombination[tempCombination]
    elif tempCombination2 in wilcardCombination.keys():
        money += wilcardCombination[tempCombination2]
    
    try:
        with open(configPathfile, 'w') as configFile:
            config = json.dump(
                {'money': money, 'combination': combination},
                configFile)
    except Exception as e:
        exit(1)
    
    return [{
        'contents': line.format(
            symbol1 = symbols[symbol1],
            symbol2 = symbols[symbol2],
            symbol3 = symbols[symbol3],
            money = formatMoney(money)),
        'highlight_groups': ['information:regular'],
        'divider_highlight_group': None}]