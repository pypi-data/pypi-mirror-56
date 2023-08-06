import argparse
import csv
import logging
import sys
import json
from lusidtools.cocoon.cocoon import load_from_data_frame
import pandas as pd
from detect_delimiter import detect
from lusid.utilities import ApiClientFactory
from lusidtools.logger import LusidLogger


def load_mapping_file_for_file_type(mapping_path, file_type) -> dict:
    '''

    :param mapping_path: The full path of mapping_file.json
    :param file_type: The type of file i.e. transactions or holdings or instruments
    :return:
    '''
    with open(mapping_path, "r") as read_file:
        return json.load(read_file)[file_type]


def get_delimiter(header_line) -> str:
    '''
    This function detects and logs a delimiter given a line of data
    :param header_line: sample line of data as string
    :return: delimiter
    '''
    try:
        # delimiter = detect(header_line).replace("{}".format("\\"), "{}".format("\\\\"))
        delimiter = detect(header_line).replace("\\", "\\\\")
        logging.debug(f"detected delimiter: " + repr(delimiter))
        return delimiter
    except:
        err = "no args delimiter was specified and failed to detect delimiter from data"
        logging.error(err)
        raise ValueError(err)


def get_instruments_data(args) -> pd.DataFrame():
    '''
    This function loads data from given file path and converts it into a pandas DataFrame
    :param args:
    :return: pandas.DataFrame Containing instruments from given file path
    '''

    logging.debug(f"Getting data")
    with open(args["file_path"], "r") as read_file:
        instruments = csv.reader(read_file, lineterminator='\n')
        for pre_amble in range(args["num_header"]):
            logging.debug(f"skipping line number:{pre_amble}, containing data:{read_file.readline()}")

        header_line = read_file.readline()
        logging.debug(f"Getting column titles as first line after header lines as specified as --num_header] : "
                      f"{header_line}")

        if not args["delimiter"]:
            args["delimiter"] = get_delimiter(header_line)
        else:
            logging.debug(f"Delimiter Specified as -dl = " + repr(args["delimiter"]))

    logging.debug(f"Reading data")
    with open(args["file_path"], "r") as read_file:
        return pd.read_csv(args["file_path"],
                           delimiter=args["delimiter"],
                           header=args["num_header"],
                           skipfooter=args["num_footer"],
                           engine='python')


def print_response(instruments_response) -> None:
    '''
    This function prints the Response ID (not implemented yet) and logs success/failed uploads
    :param instruments_response: LUSID response from request to upsert instruments
    :return:
    '''
    # TODO: get Response ID and print that
    response_ids = ["Response-ID-xxxx"]
    print(f"Response IDs: {str(response_ids)}")
    # TODO: put check in: if >100, only print 100
    # Log the successful API calls
    for response in instruments_response['success']:
        logging.debug("successfully uploaded instruments:")
        for inst in response.values.keys():
            logging.debug(f"successfully uploaded: {inst}")
        logging.debug("instruments that failed to upload:")
        for inst in response.failed.keys():
            logging.debug(f"failed to upload: {inst}")

    # Log the failed API calls
    for response in instruments_response['errors']:
        logging.debug(response)


def check_mapping_fields_exist(required_list, search_list):
    '''
    This function checks that items in one list exist in another list
    :param required_list: List of items to search for
    :param search_list:  list to search in
    :return:
    '''
    # TODO: move to command line utilities
    missing_fields = [item for item in required_list if item not in search_list]
    if missing_fields:
        logging.error(
            f"Some fields specified in the mapping file were not found in the column titles of the data file")
        logging.error(f"Data Column titles:")
        [logging.error(f"\t\t{item}") for item in search_list]
        logging.error(f"missing fields:")
        [logging.error(f"\t\t{item}") for item in missing_fields]
        logging.error(f"Suggestion: Check that mapping file is configured correctly")
        logging.error(
            f"Suggestion: Explicitly specify what line number the column titles exist in data file using -t "
            f"as an argument (see --help)")
        raise ValueError(f"Could not find fields in data column titles: {missing_fields}")


def load_instruments(args):
    if not args["file_path"]:
        raise ValueError("File path not given to load_instruments")
    file_type = "instruments"


    # create ApiFactory
    factory = ApiClientFactory(api_secrets_filename=args["secrets_file"])

    # get instruments
    instruments = get_instruments_data(args)
    if len(instruments) > 2000:
        logging.warning("large batch size of instruments detected. ensure async upsert request is used max number of "
                        "instruments per request is 2000 (see: "
                        "https://www.lusid.com/docs/api/#operation/UpsertInstruments)")
    instruments = instruments.head(2000)

    # get mappings
    mappings = load_mapping_file_for_file_type(args["mapping"], file_type)

    if "property_columns" not in mappings.keys() and not args["scope"]:
        raise ValueError(r"Instrument properties must be upserted to a specified scope, but no scope was provided. "
                         r"Please state what scope to upsert properties to using '-s'.")
    check_mapping_fields_exist(required_list=mappings["identifier_mapping"].values(),
                               search_list=instruments.columns)

    # Upsert instruments
    if args["dryrun"]:
        logging.info("--dryrun specified as True, exiting before upsert call is made")
        return 0
    # TODO: pass debug arg into load_file_multiple_portfolios and return request
    instruments_response = load_from_data_frame(
        api_factory=factory,
        data_frame=instruments,
        scope=args["scope"],
        mapping_required=mappings["required"],
        mapping_optional=mappings["optional"],
        file_type=file_type,
        identifier_mapping=mappings["identifier_mapping"],
        property_columns=mappings["property_columns"] if "property_columns" in mappings.keys() else [])

    print_response(instruments_response["instruments"])
    return instruments_response


def parse_args(args):
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--file_path",
                    required=True,
                    help=r"full path for instruments data (eg. c:\Users\Joe\data\instruments1.csv)")
    ap.add_argument("-c", "--secrets_file",
                    help=r"full path for credential secrets (eg. c:\Users\Joe\secrets.json). Not required if set as "
                         r"environment variables")
    ap.add_argument("-m", "--mapping",
                    required=True,
                    help=r"full path to mappings.json (see mappings_template.json)")  # TODO: create support article on mapping.json structure
    ap.add_argument("-s", "--scope",
                    default=None,
                    help=r"LUSID scope to act in")
    ap.add_argument("-dl", "--delimiter",
                    help=r"explicitly specify delimiter for data file and disable automatic delimiter detection")
    ap.add_argument("-nh", "--num_header",
                    type=int,
                    default=0,
                    help="number of header lines before column titles")
    ap.add_argument("-nf", "--num_footer",
                    type=int,
                    default=0,
                    help="number of footer lines after end of data")
    ap.add_argument("-dr", "--dryrun",
                    action='store_true')
    ap.add_argument("-d", "--debug",
                    help=r"print debug messages, expected input: 'debug'")


    return vars(ap.parse_args())


def main(argv):
    args = parse_args(sys.argv[1:])
    LusidLogger(args["debug"])
    load_instruments(args)

    return 0


if __name__ == "__main__":
    main(sys.argv)
