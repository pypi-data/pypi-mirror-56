import csv, sys
from qualifyr.quality_file import QualityFile
from qualifyr.utility import string_to_num, get_logger

# N.B This assumes ConFindr has only been run on a pair of fastq files from a single sample
class ConFindrFile(QualityFile):
    logger = get_logger(__file__)
    file_type = 'confindr'

    def __init__(self, file_path, file_id = None):
        super().__init__(file_path, file_id)
        self.overall_qc_check_result_operator = 'AND'

    def validate(self):
        # method to check file looks like what it says it is
        '''Returns valid rows from file. An empty list if invalid'''
        with open(self.file_path) as fh:
            reader = csv.DictReader(fh, delimiter=",", quotechar='"')
            headers = reader.fieldnames
            rows = list(reader)
            if headers == ['Sample', 'Genus', 'NumContamSNVs', 'ContamStatus', 'PercentContam', 'PercentContamStandardDeviation', 'BasesExamined', 'DatabaseDownloadDate']:
                return rows
            else:
                return []
    

    def parse(self):
        # read in file and make a dict:
        valid_rows = self.validate()
        if len(valid_rows) == 0:
            self.logger.error('{0} file invalid'.format(self.file_type))
            raise(Exception)

        else:
            self.metrics['contam_status'] = valid_rows[0]['ContamStatus']
            self.metrics['num_contam_snvs'] = string_to_num(valid_rows[0]['NumContamSNVs'])
            self.metrics['percentage_contamination'] = string_to_num(valid_rows[0]['PercentContam'], 0)
            self.metrics['genus'] = valid_rows[0]['Genus']
            self.extra_info = f"{valid_rows[0]['Genus']}. {valid_rows[0]['PercentContam']} % contamination. {valid_rows[0]['NumContamSNVs']} contaminating SNVs."



