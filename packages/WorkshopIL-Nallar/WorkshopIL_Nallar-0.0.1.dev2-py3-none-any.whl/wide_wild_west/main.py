#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging.config
from monkey.ioc.core import Registry

logging.config.fileConfig('logging.conf')


def run():
    registry = Registry()
    registry.load('data/ok_coral.json')
    tombstone_police = registry.get('tombstone_police')
    for member in tombstone_police.members:
        print(member.__dict__)


if __name__ == '__main__':  # pragma: no coverage
    run()
