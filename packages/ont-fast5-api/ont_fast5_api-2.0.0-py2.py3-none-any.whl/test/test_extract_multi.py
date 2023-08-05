try:
    from unittest.mock import patch
except ImportError:  # python2 compatibility
    from mock import patch

from tempfile import _get_candidate_names, mkdtemp
from ont_fast5_api.conversion_tools.fast5_subset import Fast5Filter, read_generator, extract_selected_reads
from ont_fast5_api.multi_fast5 import MultiFast5File
import unittest
from os import path, unlink
from glob import glob


class ExtractMultiTest(unittest.TestCase):
    def setUp(self):
        self.multifast5 = path.join(path.dirname(__file__), "data", "multi_read", "batch_0.fast5")
        self.read_set = {"568b93db", "9171d66b"}

    def test_read_generator(self):
        test_read_set = {item for item in self.read_set}  # copy

        for read_id, read in read_generator(input_file=self.multifast5, read_set=self.read_set):
            assert read_id in self.read_set
            test_read_set.remove(read_id)

        assert len(test_read_set) == 0

    def test_extract_selected_reads(self):
        test_read_set = {item for item in self.read_set}  # copy to be modified

        # three test for count below, equaling and above number of read in input file
        for count in (1, 2, 3):
            temp_file_name = next(_get_candidate_names())
            found_reads, output_file, input_file = extract_selected_reads(input_file=self.multifast5,
                                                                          output_file=temp_file_name,
                                                                          count=count, read_set=self.read_set)
            if count < len(test_read_set):
                assert found_reads.issubset(test_read_set)
                assert input_file == self.multifast5
            elif count == len(test_read_set):
                assert found_reads == test_read_set
                assert input_file == self.multifast5
            elif count >= len(test_read_set):
                assert found_reads == test_read_set
                assert input_file is None

            assert output_file == temp_file_name
            # verify that resulting output file is a legal MultiFast5 with desired reads in it
            with MultiFast5File(output_file) as multi_file:
                readlist = multi_file.get_read_ids()
                assert len(readlist) > 0
                for read in readlist:
                    assert read in test_read_set

            unlink(temp_file_name)

    @patch('ont_fast5_api.conversion_tools.fast5_subset.get_progress_bar')
    def test_selector_args_generator(self, mock_pbar):
        test_read_set = {item for item in self.read_set}  # copy to be modified
        base_path = path.dirname(__file__)
        single_reads = path.join(base_path, "data", "single_reads")
        assert path.isdir(single_reads), single_reads

        input_f5s = glob(path.join(single_reads, '*.fast5'))  #list(single_reads.glob('*'))
        batch_size = 1

        # create mock read id list file
        temp_file_name = next(_get_candidate_names())
        with open(temp_file_name, 'w') as temp_file:
            for read in test_read_set:
                temp_file.write(read + '\n')
            temp_file.flush()
            temp_file.seek(0)

        # catch exceptions to make sure temp_file is deleted after
        try:
            temp_dir = mkdtemp()
            f = Fast5Filter(input_folder=single_reads, output_folder=temp_dir, read_list_file=temp_file_name,
                            batch_size=batch_size,
                            filename_base="batch")

            args_combos = list(f._args_generator())
            # there should be two tuples of arguments
            assert len(args_combos) == len(test_read_set) / batch_size

            num_files_queued = len(f.input_f5s)
            assert num_files_queued == (len(input_f5s) - len(args_combos)), f.input_f5s
            assert len(f.available_out_files) == 0

            # "exhaust" an input file and put output file back on queue
            input_file, output_file, reads, count = args_combos[0]
            f._update_file_lists(reads={}, in_file=None, out_file=output_file)
            assert len(f.input_f5s) == num_files_queued
            assert len(f.available_out_files) == 1

            # this results in another args tuple generated
            new_args_combos = list(f._args_generator())
            assert len(new_args_combos) == 1, len(new_args_combos)
            unlink(temp_file_name)

        except Exception as e:
            unlink(temp_file_name)
            raise
