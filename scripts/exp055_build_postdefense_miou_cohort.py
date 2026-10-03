from pathlib import Path
import argparse
import csv
import hashlib
import json
import os
import subprocess

import numpy as np


REPO=Path.home()/"thesis"/"identitygate"
CONFIG=REPO/"configs"/"EXP055-postdefense-miou-v1.json"

OUTDIR=REPO/"experiments"/"EXP055_postdefense_miou"
COHORT_OUT=OUTDIR/"cohort.csv"
MANIFEST_OUT=OUTDIR/"cohort_manifest.json"


def sha256_file(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()


def git_head():
    return subprocess.check_output(
        ["git","-C",str(REPO),"rev-parse","HEAD"],
        text=True,
    ).strip()


def git_status():
    return subprocess.check_output(
        ["git","-C",str(REPO),"status","--porcelain"],
        text=True,
    ).strip()


def require_clean_committed():
    status=git_status()

    if status:
        raise RuntimeError(
            "STOP: run requires clean thesis repo: "+status
        )

    for path in (
        Path(__file__).resolve(),
        CONFIG,
    ):
        rel=str(path.relative_to(REPO))

        result=subprocess.run(
            [
                "git","-C",str(REPO),
                "ls-files","--error-unmatch",rel
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        if result.returncode != 0:
            raise RuntimeError(
                "STOP: run requires committed file: "+rel
            )


def read_csv(path):
    with open(path,newline="",encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv_atomic(path,fieldnames,rows):
    path.parent.mkdir(parents=True,exist_ok=True)

    tmp=Path(str(path)+".tmp")

    with open(tmp,"w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(
            f,
            fieldnames=fieldnames,
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)

    os.replace(tmp,path)


def write_json_atomic(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)

    tmp=Path(str(path)+".tmp")

    tmp.write_text(
        json.dumps(
            data,
            indent=2,
            sort_keys=True,
        )+"\n",
        encoding="utf-8",
    )

    os.replace(tmp,path)


def membership_hash(label,videos):
    payload=(
        label+"\n"
        +"\n".join(videos)
        +"\n"
    ).encode("utf-8")

    return hashlib.sha256(payload).hexdigest()


def load_context():
    cfg=json.loads(
        CONFIG.read_text(encoding="utf-8")
    )

    population_path=REPO/cfg["input"]["population"]["path"]

    got=sha256_file(population_path)
    want=cfg["input"]["population"]["sha256"]
    assert got==want,(got,want)

    population_rows=read_csv(population_path)

    assert (
        len(population_rows)
        == cfg["input"]["population"]["expected_videos"]
    )

    videos=[r["video"] for r in population_rows]

    assert videos==sorted(videos)
    assert len(videos)==len(set(videos))

    excluded={}

    for label,path in cfg["input"]["exclude"].items():
        rows=read_csv(REPO/path)
        ids=[r["video"] for r in rows]
        assert len(ids)==len(set(ids))
        excluded[label]=set(ids)

    return cfg,population_rows,excluded


def build(cfg,population_rows,excluded):
    population_ids={
        r["video"]
        for r in population_rows
    }

    fresh=excluded["fresh_dev"]
    hard=excluded["hard_test"]
    representative=excluded["representative_test"]

    assert not (fresh & hard)
    assert not (fresh & representative)
    assert not (hard & representative)

    excluded_union=fresh | hard | representative

    assert excluded_union <= population_ids

    assert (
        len(excluded_union)
        == cfg["sampling"]["expected_excluded_union_videos"]
    )

    untouched=sorted(
        population_ids-excluded_union
    )

    assert (
        len(untouched)
        == cfg["sampling"]["expected_untouched_videos"]
    )

    rng=np.random.default_rng(
        cfg["sampling"]["rng_seed"]
    )

    positions=rng.choice(
        len(untouched),
        size=cfg["sampling"]["videos"],
        replace=False,
    )

    selected=sorted(
        untouched[int(i)]
        for i in positions
    )

    assert len(selected)==cfg["sampling"]["videos"]
    assert len(selected)==len(set(selected))
    assert not (set(selected) & excluded_union)

    row_by_video={
        r["video"]:r
        for r in population_rows
    }

    output=[]

    for video in selected:
        row=row_by_video[video]

        output.append({
            "video":video,
            "cohort":"POSTDEFENSE_MIOU80",
            "primary_event_count":int(
                row["primary_event_count"]
            ),
            "di_v1_score":row["di_v1_score"],
            "visual_cluster":int(
                row["visual_cluster"]
            ),
        })

    return {
        "output_rows":output,
        "selected":selected,
        "untouched":untouched,
        "excluded_union":excluded_union,
        "membership_sha256":membership_hash(
            "POSTDEFENSE_MIOU80",
            selected,
        ),
    }


def plan():
    cfg,rows,excluded=load_context()
    result=build(cfg,rows,excluded)

    print("EXP055 COHORT PLAN")
    print("identitygate_head =",git_head())
    print("population_videos =",len(rows))
    print(
        "excluded_union_videos =",
        len(result["excluded_union"]),
    )
    print(
        "untouched_videos =",
        len(result["untouched"]),
    )
    print(
        "selected_videos =",
        len(result["selected"]),
    )
    print(
        "POSTDEFENSE_MIOU80_VIDEO_SHA256 =",
        result["membership_sha256"],
    )
    print("model_outcomes_used = false")
    print("sam_inference_performed = false")
    print("gate_inference_performed = false")
    print("cohort_written = false")
    print("EXP055_COHORT_PLAN_PASS")


def run():
    require_clean_committed()

    if OUTDIR.exists():
        raise RuntimeError(
            "STOP: EXP055 output directory exists; do not rerun"
        )

    cfg,rows,excluded=load_context()
    result=build(cfg,rows,excluded)

    fields=[
        "video",
        "cohort",
        "primary_event_count",
        "di_v1_score",
        "visual_cluster",
    ]

    write_csv_atomic(
        COHORT_OUT,
        fields,
        result["output_rows"],
    )

    manifest={
        "experiment":"EXP055",
        "status":"POSTDEFENSE_MIOU_COHORT_FROZEN",
        "identitygate_commit_at_execution":
            git_head(),
        "config_sha256":
            sha256_file(CONFIG),
        "script_sha256":
            sha256_file(Path(__file__).resolve()),
        "population_videos":len(rows),
        "excluded_union_videos":
            len(result["excluded_union"]),
        "untouched_candidate_videos":
            len(result["untouched"]),
        "selected_videos":
            len(result["selected"]),
        "rng_seed":cfg["sampling"]["rng_seed"],
        "sampling_method":
            cfg["sampling"]["method"],
        "membership_sha256":
            result["membership_sha256"],
        "boundary":{
            "model_outcomes_used":False,
            "sam_inference_performed":False,
            "gate_inference_performed":False,
            "selection_is_outcome_independent":True,
        },
    }

    manifest["output_hashes"]={
        "cohort.csv":
            sha256_file(COHORT_OUT),
    }

    write_json_atomic(
        MANIFEST_OUT,
        manifest,
    )

    print("population_videos =",len(rows))
    print(
        "excluded_union_videos =",
        len(result["excluded_union"]),
    )
    print(
        "untouched_videos =",
        len(result["untouched"]),
    )
    print(
        "selected_videos =",
        len(result["selected"]),
    )
    print(
        "POSTDEFENSE_MIOU80_VIDEO_SHA256 =",
        result["membership_sha256"],
    )
    print("model_outcomes_used = false")
    print("sam_inference_performed = false")
    print("gate_inference_performed = false")
    print("EXP055_COHORT_RUN_PASS")


def main():
    parser=argparse.ArgumentParser()

    parser.add_argument(
        "mode",
        choices=[
            "plan",
            "run",
        ],
    )

    args=parser.parse_args()

    if args.mode=="plan":
        plan()
    else:
        run()


if __name__=="__main__":
    main()
