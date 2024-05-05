from qilocal.utils import Storage
import os


class TestBucket:
    storage = Storage()

    def test_bucket(self):
        bucket1 = self.storage.get_bucket("my_bucket")
        assert self.storage.list_buckets()[0] == "my_bucket"
        open("file1", "w")
        bucket1.upload_file("file1")
        os.remove("file1")
        assert bucket1.list_files()[0] == "file1"
