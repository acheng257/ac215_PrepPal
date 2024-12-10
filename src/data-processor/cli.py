"""
Module that contains the command line app.

Typical usage example from command line:
        python cli.py --clean --prepare
"""

import os
import argparse
import preprocessor


dataset_folder = os.path.join("/persistent", "dataset")
raw_folder = os.path.join(dataset_folder, "raw")
clean_folder = os.path.join(dataset_folder, "clean")
ready_folder = os.path.join(dataset_folder, "ready_for_training")


def main(args=None):
    GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")
    print("GCS_BUCKET_NAME:", GCS_BUCKET_NAME)

    # Make dirs
    os.makedirs(dataset_folder, exist_ok=True)
    os.makedirs(raw_folder, exist_ok=True)
    os.makedirs(clean_folder, exist_ok=True)
    os.makedirs(ready_folder, exist_ok=True)

    # ARGUMENT: CLEAN
    if args.generate:
        """
        This should only be executed if a new file has been added to the GCS bucket.
        """
        print("Generating new dataset")
        preprocessor.generate(raw_folder, args.data_iters)
        preprocessor.prepare_and_upload(raw_folder, clean_folder)

    # ARGUMENT: PREPARE
    if args.prepare:
        print("Prepare dataset for training")
        preprocessor.train_test_split_from_clean_data(ready_folder)
        preprocessor.upload_train_test_data(ready_folder)

    if args.delete:
        print("Deleting...")
        # if os.path.exists(raw_folder):
        #     os.remove(raw_folder)

    if args.test:
        print("Test method")


if __name__ == "__main__":
    # Generate the inputs arguments parser
    # if you type into the terminal 'python cli.py --help', it will provide the description
    parser = argparse.ArgumentParser(description="Data Collector CLI")

    parser.add_argument(
        "-g",
        "--generate",
        action="store_true",
        help="whether or not to generate new training data",
    )
    parser.add_argument("--data-iterations", dest="data_iters", default=10, type=int, help="Number of data to train. 34 == $1.")
    parser.add_argument(
        "-p",
        "--prepare",
        action="store_true",
        help="Prepare data for training",
    )
    parser.add_argument(
        "-t",
        "--test",
        action="store_true",
        help="Testing...",
    )
    parser.add_argument(
        "-d",
        "--delete",
        action="store_true",
        help="todo",
    )

    args = parser.parse_args()

    main(args)
