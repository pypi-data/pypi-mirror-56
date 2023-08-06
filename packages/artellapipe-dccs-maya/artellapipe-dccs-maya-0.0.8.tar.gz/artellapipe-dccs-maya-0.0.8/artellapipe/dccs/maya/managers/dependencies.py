#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains manager for Maya dependencies
"""

from __future__ import print_function, division, absolute_import

__author__ = "Tomas Poveda"
__license__ = "MIT"
__maintainer__ = "Tomas Poveda"
__email__ = "tpovedatd@gmail.com"

import os

import tpDccLib as tp
from tpPyUtils import decorators

import artellapipe.register
from artellapipe.managers import dependencies

if tp.is_maya():
    from tpMayaLib.core import parser

    class ArtellaMayaAsciiParser(parser.MayaAsciiParser, object):
        def __init__(self, stream):
            super(ArtellaMayaAsciiParser, self).__init__(stream=stream)

            self._references = list()
            self._gpu_cache_paths = list()
            self._alembic_paths = list()

            self._invalid_paths = list()

        @property
        def references(self):
            """
            Returns list of references found in Maya ASCII
            :return: list(str)
            """

            return self._references

        @property
        def gpu_cache_paths(self):
            """
            Returns all GPU cache paths found in Maya ASCII
            :return: list(str)
            """

            return self._gpu_cache_paths

        @property
        def alembic_paths(self):
            """
            Returns all Alembic cache paths found in Maya ASCII
            :return: list(str)
            """

            return self._alembic_paths

        @property
        def invalid_paths(self):
            """
            Returns all invaild paths found in Maya ASCII
            :return: list(str)
            """

            return self._invalid_paths

        def on_file_reference(self, path):
            path = artellapipe.FilesMgr().fix_path(path)
            if path not in self._references:
                if not os.path.isfile(path):
                    if path not in self._invalid_paths:
                        self._invalid_paths.append(path)
                else:
                    self._references.append(path)

        def on_set_attr(self, name, value, attr_type):

            # GPU Cache File Path
            if name == 'cfn':
                value = artellapipe.FilesMgr().fix_path(value)
                if value not in self._gpu_cache_paths:
                    if not os.path.isfile(value):
                        if value not in self._invalid_paths:
                            self._invalid_paths.append(value)
                    else:
                        self._gpu_cache_paths.append(value)
            # Alembic Paths
            elif name == 'fn':
                value = artellapipe.FilesMgr().fix_path(value)
                if value not in self._alembic_paths:
                    if not os.path.isfile(value):
                        if value not in self._invalid_paths:
                            self._invalid_paths.append(value)
                    else:
                        self._alembic_paths.append(value)

        def get_all_paths(self, include_references=True):
            """
            Returns all paths in current Maya ASCII file
            :return: list(str)
            """

            if include_references:
                return self._references + self._alembic_paths + self._gpu_cache_paths
            else:
                return self._alembic_paths + self._gpu_cache_paths

else:
    class ArtellaMayaAsciiParser(object):
        pass


class ArtellaMayaDependenciesManager(dependencies.ArtellaDependenciesManager, object):
    def __init__(self):
        super(ArtellaMayaDependenciesManager, self).__init__()

    def get_dependencies(self, file_path, parent_path=None, found_files=None):
        """
        Returns all dependencies that are currently loaded in the given file
        :param file_path: str, file path we want to get dependencies of
        :param parent_path: str
        :param found_files: list(str)
        :return: list(str)
        """

        if not found_files:
            found_files = dict()

        if parent_path:
            if parent_path not in found_files:
                found_files[parent_path] = list()
            if file_path not in found_files[parent_path]:
                found_files[parent_path].append(file_path)

        if not os.path.isfile(file_path):
            file_path = artellapipe.FilesMgr().fix_path(file_path)
            if not os.path.isfile(file_path):
                return None

        ext = os.path.splitext(file_path)[-1]
        if ext != '.ma':
            return None

        with open(file_path, 'r') as open_file:
            if file_path not in found_files:
                found_files[file_path] = list()
            parser = ArtellaMayaAsciiParser(open_file)
            parser.parse()
            found_paths = parser.get_all_paths(include_references=False)
            for path in found_paths:
                if path not in found_files[file_path]:
                    found_files[file_path].append(path)

            for ref in parser.references:
                ref = artellapipe.FilesMgr().fix_path(ref)
                self.get_dependencies(
                    file_path=ref,
                    parent_path=file_path,
                    found_files=found_files)

        return found_files


@decorators.Singleton
class ArtellaMayaDependenciesManagerSingleton(ArtellaMayaDependenciesManager, object):
    def __init__(self):
        ArtellaMayaDependenciesManager.__init__(self)


artellapipe.register.register_class('DepsMgr', ArtellaMayaDependenciesManagerSingleton)
