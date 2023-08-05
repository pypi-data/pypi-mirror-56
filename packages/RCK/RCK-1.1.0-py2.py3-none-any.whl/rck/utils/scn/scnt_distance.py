import argparse

import os
import sys

current_file_level = 2
current_dir = os.path.dirname(os.path.realpath(__file__))
for _ in range(current_file_level):
    current_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)

from rck.core.structures import aligned_scnts, cn_distance_inter_scnt
from rck.core.io import read_scnt_from_source


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scnt1", type=argparse.FileType("rt"), required=True)
    parser.add_argument("--scnt2", type=argparse.FileType("rt"), required=True)
    parser.add_argument("--clone-ids")
    args = parser.parse_args()
    segments1, scnt1 = read_scnt_from_source(source=args.scnt1)
    segments2, scnt2 = read_scnt_from_source(source=args.scnt2)
    if args.clone_ids is None:
        clone_ids = sorted(set(scnt1.keys()) & set(scnt2.keys()))
    else:
        clone_ids = args.clone_ids.split(",")
    for clone_id in sorted(scnt2.keys()):
        scnt_clone_id = sorted(scnt1.keys())[0]
        ref_scnt2 = {scnt_clone_id: scnt2[clone_id]}
        scnt1 = {clone_id: scnt1[clone_id] for clone_id in clone_ids}
    # scnt2 = {clone_id: scnt2[clone_id] for clone_id in clone_ids}
    # segments_by_sample_names = {"sample1": segments1, "sample2": segments2}
    # scnts_by_sample_names = {"sample1": scnt1, "sample2": scnt2}
    # segments_by_sn, scnts_by_sn = aligned_scnts(segments_by_sample_names=segments_by_sample_names, scnts_by_sample_names=scnts_by_sample_names)
    # scnt1, scnt2 = scnts_by_sn["sample1"], scnts_by_sn["sample2"]
    # segments1, segments2 = segments_by_sn["sample1"], segments_by_sn["sample2"]
        clone_specific_cn_distance = cn_distance_inter_scnt(tensor1=scnt1, tensor2=ref_scnt2, segments=segments1)
        print(clone_id, clone_specific_cn_distance.values())


if __name__ == "__main__":
    main()
