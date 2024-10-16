import argparse

from preprocess_rag import chunk, clean_dataset, embed, load

# Generate the inputs arguments parser
parser = argparse.ArgumentParser(description="Command description.")

def main(args=None):
    print("CLI Arguments:", args)
     
    if args.data_type == "rag":
	
        if args.clean_dataset:
            clean_dataset(download=args.download, upload=args.upload)

        if args.chunk:
            chunk(method=args.chunk_type, download=args.download, upload=args.upload)

        if args.embed:
            embed(method=args.chunk_type, download=args.download, upload=args.upload)

        if args.load:
            load(method=args.chunk_type, download=args.download)


if __name__ == "__main__":
    # Generate the inputs arguments parser
    parser = argparse.ArgumentParser(description="Preprocessing PrePal data")

    parser.add_argument(
        "--clean_dataset",
        action="store_true",
        help="Process and clean the recipes data",
    )

    parser.add_argument(
        "--chunk",
        action="store_true",
        help="Chunk recipe data",
    )

    parser.add_argument(
        "--embed",
        action="store_true",
        help="Embed recipe chunks",
    )

    parser.add_argument(
        "--load",
        action="store_true",
        help="Load embeddings to vector db",
    )
	
    parser.add_argument(
        "--download",
        action="store_true",            
        help="Enable or disable download",
    )

    parser.add_argument(
        "--upload",
        action="store_true",            
        help="Enable or disable upload",
    )
	
    parser.add_argument(
        "--data_type",         
        default="rag",
        help="rag | fine_tune"
    )

    parser.add_argument(
        "--chunk_type",         
        default="entire_recipe",
        help="entire_recipe | sliding_window"
    )

    args = parser.parse_args()

main(args)