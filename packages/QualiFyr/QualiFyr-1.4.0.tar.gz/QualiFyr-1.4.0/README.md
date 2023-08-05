# Qualifyr
This package provides an extensible framework whereby multiple text files that provide QC information can be parsed to give a failure/warning/pass status for each QC file and combined to give an overall QC status for a sample. The 'worst' QC status from any QC file will be used to derive a QC status. For example if some of the QC files are pass but one is deemed a failure the overall status will be FAILURE.

The command is invoked as follows

```
usage: qualifyr [-h] {check,report} ...

A package to check quality files and assess overall pass/fail

positional arguments:
  {check,report}  The following commands are available. Type qualifyr
                  <COMMAND> -h for more help on a specific commands
    check         Check multiple quality metric files based on conditions and
                  produce overall result
    report        Produce a html report based on the qualifyr output from
                  multiple sampels

optional arguments:
  -h, --help      show this help message and exit
```

There are two subcommands:

1. check. Specify multiple qc files two assess and assign an individual and overall QC status.

    ```
    usage: qualifyr check [-h] [-q QUAST_FILE] [-f FASTQC_FILE [FASTQC_FILE ...]]
                          [-c CONFINDR_FILE] -y CONDITIONS_YAML_FILE [-j] -s
                          SAMPLE_NAME [-o OUTPUT_DIR]
    required arguments:
      At least one of the following quality files
      -q QUAST_FILE, --quast_file QUAST_FILE
                            quast file path
      -f FASTQC_FILE [FASTQC_FILE ...], --fastqc_file FASTQC_FILE [FASTQC_FILE ...]
                            fastqc summary file path
      -c CONFINDR_FILE, --confindr_file CONFINDR_FILE
                            confindr report file path


      -y CONDITIONS_YAML_FILE, --conditions_yaml_file CONDITIONS_YAML_FILE
                            conditions yaml file path
      -s SAMPLE_NAME, --sample_name SAMPLE_NAME
                        The name of the sample from which the quality files
                        are derived
    optional arguments:
      -j, --json_output_format
                            Output the check results as JSON rather than TSV
                            (default)
      -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                            Path to output directory. If specified output will be
                            written to file in format
                            sample_name.qualifyr.{tsv,json}
      -h, --help            show this help message and exit
    ```
    Currently QC files from
      - [fastqc](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/)
      - [quast](http://bioinf.spbau.ru/quast)
      - [confindr](https://lowandrew.github.io/ConFindr/)

    are supported. Multiple summary fastqc files can be supplied e.g from read 1 and 2

    The overall sample status will be returned to STDOUT

    The possible return statuses are
      - PASS
      - WARNING
      - FAILURE

  If there are any warnings or failures, the reason for the status along with the file will be returned as tab separated lines to STDERR

2. report. Generate an html report from multiple qualifyr outputs in json format
    ```
    usage: qualifyr report [-h] -i INPUT_DIR [-o OUTPUT_DIR] [-c EXTRA_COLUMNS]
                       [-t REPORT_TITLE]
    required arguments:
    -i INPUT_DIR, --input_dir INPUT_DIR
                      Path to input directory containing multiple qualifyr
                      json outputs

    optional arguments:
      -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                            Path to output directory. If not supplied this will be 
                            the same as the input directory
      -c EXTRA_COLUMNS, --extra_columns EXTRA_COLUMNS
                            Extra columns to add to the report provided as a quote
                            enclosed comma separated list e.g 'quast.N50,quast.#
                            contigs (>= 1000 bp),confindr.contam_status'
      -t REPORT_TITLE, --report_title REPORT_TITLE
                            Title for the report
      -h, --help            show this help message and exit
    ```
    The command requires an input directory that contains multiple qualifyr json output files.


## Supplying conditions for the warning, failure criteria
These are supplied in a YAML file that is specified by the `-y` argument to the `qualifyr` script. The basic format is:

```
<FILE TYPE:
  '<METRIC NAME':
    <WARNING or PASS>:
      condition_type: <One of gt, lt, lt_or_gt, gt_and_lt, eq, ne, any>
      condition_value: <VALUE>
```

A specific example for quast output is

```
quast:
  '# contigs (>= 1000 bp)':
    warning:
      condition_type: gt
      condition_value: 75
    failure:
      condition_type: gt
      condition_value: 150
```
In this case a sample will be a given a WARNING status if there are greater than 75 contigs of size 1000bp or more, and a FAILURE status if the same values is graeter than 150.

An example of a full conditions file can be found [here](example_qc_conditions.yml)


## Installation 
```
pip3 install qualifyr
```

## Installation from source
Clone the git repo and install via python setup
```
git clone https://gitlab.com/cgps/qualifyr.git
cd qualifyr
python setup.py install
```

## Tests
```
python setup.py test
``` 

## Test in dev
  - clone repo
  - cd into directory
  - to see pass result run
  ```
  qualifyr -y tests/test_data/pass_conditions.yml -q tests/test_data/quast_valid.txt  -f tests/test_data/fastqc_valid.txt   tests/test_data/fastqc_fail.txt -c tests/test_data/confindr_pass.csv
  ```
  - to see fail result run
  ```
  qualifyr -y tests/test_data/fail_conditions.yml -q tests/test_data/quast_valid.txt  -f tests/test_data/fastqc_valid.txt   tests/test_data/fastqc_fail.txt -c tests/test_data/confindr_pass.csv`
  ```

## Adding other QC file types
The framework is designed to be extensible by subclassing the [QualityFile](qualifyr/quality_file.py) class. See the [quast_file.py](qualifyr/quast_file.py) for an example.
The subclass must implement 2 functions

1. validate: This function should check the file is the expected format and return a list of lines containing just the metrics from the file.
2. parse: This function should call validate and then with the returned list populate an instance variable `metrics` which is a dict containing the metric names as keys and the associated values as the values.

In addition the class should specify a class variable `file_type`
