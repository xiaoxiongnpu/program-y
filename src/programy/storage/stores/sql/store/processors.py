"""
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import os
from programy.utils.logging.ylogger import YLogger
from programy.storage.stores.sql.store.sqlstore import SQLStore
from programy.storage.entities.processors import ProcessorStore
from programy.storage.stores.sql.dao.processor import PreProcessor
from programy.storage.stores.sql.dao.processor import PostProcessor
from programy.storage.stores.sql.dao.processor import PostQuestionProcessor
from programy.storage.entities.store import Store
from programy.utils.classes.loader import ClassLoader
from programy.utils.console.console import outputLog


class SQLProcessorsStore(SQLStore, ProcessorStore):

    def __init__(self, storage_engine):
        SQLStore.__init__(self, storage_engine)

    def _get_storage_class(self):
        pass

    def load(self, collector, name=None):
        processors = self.get_all_processors()
        for processor in processors:
            try:
                collector.add_processor(ClassLoader.instantiate_class(processor.classname)())
            except Exception as e:
                YLogger.exception(self, "Failed pre-instantiating Processor [%s]", e, processor.classname)

    def upload_from_file(self, filename, fileformat=Store.TEXT_FORMAT, commit=True, verbose=False):

        count = 0
        success = 0

        if os.path.exists(filename):
            try:
                with open(filename, "r", encoding="utf-8") as file:
                    for line in file:
                        if self._process_config_line(line, verbose) is True:
                            success += 1
                        count += 1

                if commit is True:
                    self.commit()

            except FileNotFoundError:
                YLogger.error(self, "File not found [%s]", filename)

        return count, success

    def _process_config_line(self, line, verbose):
        line = line.strip()
        if line:
            if line[0] != '#':
                processor = self._get_entity(line)
                self.storage_engine.session.add(processor)
                if verbose is True:
                    outputLog(self, line)
                return True
        return False

    def _get_entity(self, classname):
        raise NotImplementedError()

    def get_all_processors(self):
        return []


class SQLPreProcessorsStore(SQLProcessorsStore, ProcessorStore):

    def __init__(self, storage_engine):
        SQLProcessorsStore.__init__(self, storage_engine)

    def _get_all(self):
        return self._storage_engine.session.query(ProcessLookupError)

    def empty(self):
        self._storage_engine.session.query(PreProcessor).delete()

    def get_all_processors(self):
        return self._storage_engine.session.query(PreProcessor)

    def _get_entity(self, classname):
        return PreProcessor(classname=classname)


class SQLPostProcessorsStore(SQLProcessorsStore, ProcessorStore):

    def __init__(self, storage_engine):
        SQLProcessorsStore.__init__(self, storage_engine)

    def _get_all(self):
        return self._storage_engine.session.query(PostProcessor)

    def empty(self):
        self._storage_engine.session.query(PostProcessor).delete()

    def get_all_processors(self):
        return self._storage_engine.session.query(PostProcessor)

    def _get_entity(self, classname):
        return PostProcessor(classname=classname)


class SQLPostQuestionProcessorsStore(SQLProcessorsStore, ProcessorStore):

    def __init__(self, storage_engine):
        SQLProcessorsStore.__init__(self, storage_engine)

    def _get_all(self):
        return self._storage_engine.session.query(PostQuestionProcessor)

    def empty(self):
        self._storage_engine.session.query(PostProcessor).delete()

    def get_all_processors(self):
        return self._storage_engine.session.query(PostProcessor)

    def _get_entity(self, classname):
        return PostProcessor(classname=classname)
