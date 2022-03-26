import argparse
import subprocess
import time
from multiprocessing import Pool

from tqdm import tqdm


def test_one(file_id):
    command = f"poetry run python3 main.py < tools/in/{file_id}.txt"
    score_str = subprocess.getoutput(command)

    return file_id, score_str


def test(file_ids):
    with Pool(processes=4) as p:
        results = list(
            tqdm(
                p.imap(func=test_one, iterable=file_ids),
            )
        )

    for file_num, score in results:
        print(file_num, score)


if __name__ == "__main__":
    file_ids = [format(i, "0>4") for i in range(100)]
    test(file_ids)
