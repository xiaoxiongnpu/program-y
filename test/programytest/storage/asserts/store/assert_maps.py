import unittest

from programy.mappings.maps import MapCollection
from programy.storage.entities.store import Store

class MockMapCollection(object):

    def __init__(self):
        self.maps = {}

    def empty(self):
        self.maps.clear()

    def remove(self, name):
        self.maps.pop(name, None)

    def add_map(self, map_name, the_map, store):
        self.maps[map_name] = the_map


class MapStoreAsserts(unittest.TestCase):
    
    def assert_map_storage(self, store):
        store.empty()
    
        store.add_to_map("TESTMAP1", "Key1", "Val1")
        store.add_to_map("TESTMAP1", "Key2", "Val2")
        store.add_to_map("TESTMAP1", "Key3", "Val3")
        store.add_to_map("TESTMAP2", "Key1", "Val1")
        store.commit()
    
        map_collection = MockMapCollection()
        store.load_all(map_collection)
        self.assertEquals(2, len(map_collection.maps.keys()))
        self.assertTrue("TESTMAP1" in map_collection.maps)
        self.assertTrue("Val1", map_collection.maps['TESTMAP1']['Key1'])
        self.assertTrue("Val2", map_collection.maps['TESTMAP1']['Key2'])
        self.assertTrue("Val3", map_collection.maps['TESTMAP1']['Key3'])
        self.assertTrue("TESTMAP2" in map_collection.maps)
        self.assertTrue("Val1", map_collection.maps['TESTMAP2']['Key1'])
    
        store.remove_from_map("TESTMAP1", "Key1")
        store.remove_from_map("TESTMAP2", "Key1")
        store.commit()
    
        map_collection = MockMapCollection()
        store.load_all(map_collection)
        self.assertEquals(1, len(map_collection.maps.keys()))
        self.assertTrue("TESTMAP1" in map_collection.maps)
        self.assertTrue("Val2", map_collection.maps['TESTMAP1']['Key2'])
        self.assertTrue("Val3", map_collection.maps['TESTMAP1']['Key3'])
        self.assertFalse("TESTMAP2" in map_collection.maps)

    def assert_upload_from_text(self, store, store_type):
        store.empty()
    
        store.upload_from_text('TESTMAP', """
        ant:6
        bat:2
        bear:4
        bee:6
        bird:2
        """)

        map_collection = MapCollection()
        store.load(map_collection, 'TESTMAP')

        self.assertTrue(map_collection.contains('TESTMAP'))
        self.assertEquals(store_type, map_collection.storename('TESTMAP'))
        map = map_collection.map('TESTMAP')
        self.assertIsNotNone(map)
        self.assertTrue('ANT' in map)
        self.assertEquals('6', map['ANT'])

    def assert_upload_text_files_from_directory_no_subdir(self, store, filename, store_type):
        store.empty()

        store.upload_from_directory(filename, subdir=False)

        map_collection = MapCollection()
        store.load(map_collection, 'TESTMAP')

        self.assertTrue(map_collection.contains('TESTMAP'))
        self.assertEquals(store_type, map_collection.storename('TESTMAP'))
        map = map_collection.map('TESTMAP')
        self.assertIsNotNone(map)

    def assert_upload_from_csv_file(self, store, filename, store_type):
        store.empty()

        store.upload_from_file(filename, format=Store.CSV_FORMAT)

        map_collection = MapCollection()
        store.load(map_collection, 'TESTMAP')

        self.assertTrue(map_collection.contains('TESTMAP'))
        self.assertEquals(store_type, map_collection.storename('TESTMAP'))
        map = map_collection.map('TESTMAP')
        self.assertIsNotNone(map)

    def assert_upload_csv_files_from_directory_with_subdir(self, store, filename, store_type):
     
        store.empty()

        store.upload_from_directory(filename, format=Store.CSV_FORMAT)

        map_collection = MapCollection()
        store.load_all(map_collection)

        self.assertTrue(map_collection.contains('TESTMAP'))
        self.assertEquals(store_type, map_collection.storename('TESTMAP'))
        map = map_collection.map('TESTMAP')
        self.assertIsNotNone(map)

        self.assertTrue(map_collection.contains('TESTMAP2'))
        self.assertEquals(store_type, map_collection.storename('TESTMAP2'))
        map = map_collection.map('TESTMAP2')
        self.assertIsNotNone(map)