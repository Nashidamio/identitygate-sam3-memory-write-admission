from pathlib import Path
import argparse
import csv
import gc
import hashlib
import importlib.util
import json
import os
import subprocess
import sys

import numpy as np
import torch


ROOT=Path(__file__).resolve().parents[1]
CONFIG=ROOT/"configs"/"EXP055-postdefense-miou-inference-v1.json"


def sha256sum(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda:f.read(1048576),b""):
            h.update(chunk)
    return h.hexdigest()


def read_csv(path):
    with open(path,newline="",encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv_atomic(path,fields,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    tmp=Path(str(path)+".tmp")
    with open(tmp,"w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(
            f,
            fieldnames=fields,
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)
    os.replace(tmp,path)


def write_json_atomic(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    tmp=Path(str(path)+".tmp")
    tmp.write_text(
        json.dumps(data,indent=2,sort_keys=True)+"\n",
        encoding="utf-8",
    )
    os.replace(tmp,path)


def load_module(name,path):
    spec=importlib.util.spec_from_file_location(name,str(path))
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load module: "+str(path))
    module=importlib.util.module_from_spec(spec)
    sys.modules[name]=module
    spec.loader.exec_module(module)
    return module


def git_head():
    return subprocess.check_output(
        ["git","-C",str(ROOT),"rev-parse","HEAD"],
        text=True,
    ).strip()


def git_status():
    return subprocess.check_output(
        ["git","-C",str(ROOT),"status","--porcelain"],
        text=True,
    ).strip()


def membership_hash(label,videos):
    payload=(
        label+"\n"
        +"\n".join(videos)
        +"\n"
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def verify_sha(path,want,label):
    got=sha256sum(path)
    if got != want:
        raise RuntimeError(
            "{} SHA mismatch: {} != {}".format(label,got,want)
        )


def load_cfg():
    cfg=json.loads(CONFIG.read_text(encoding="utf-8"))

    if cfg["experiment"] != "EXP055":
        raise RuntimeError("Wrong experiment config")

    if cfg["scientific_status"] != "SUPPLEMENTARY_POSTDEFENSE_NONCONFIRMATORY":
        raise RuntimeError("Wrong scientific status")

    if float(cfg["methods"]["B2"]["tau"]) != 0.1:
        raise RuntimeError("Frozen B2 tau changed")

    if cfg["metric"]["exclude_conditioning_frame"] is not True:
        raise RuntimeError("Frame-0 exclusion changed")

    if cfg["metric"]["absent_gt_object_frames_in_iou_denominator"] is not False:
        raise RuntimeError("Absent-GT denominator rule changed")

    if int(cfg["inference"]["bootstrap_replicates"]) != 50000:
        raise RuntimeError("Bootstrap replicate count changed")

    if int(cfg["scope"]["expected_videos"]) != 80:
        raise RuntimeError("Cohort size changed")

    for name,item in cfg["source_dependencies"].items():
        verify_sha(
            ROOT/item["path"],
            item["sha256"],
            name,
        )

    verify_sha(
        ROOT/cfg["scope"]["cohort_csv"],
        cfg["scope"]["cohort_csv_sha256"],
        "cohort_csv",
    )

    verify_sha(
        ROOT/cfg["scope"]["cohort_manifest"],
        cfg["scope"]["cohort_manifest_sha256"],
        "cohort_manifest",
    )

    verify_sha(
        ROOT/cfg["methods"]["B2"]["model_path"],
        cfg["methods"]["B2"]["model_sha256"],
        "B2_model",
    )

    return cfg


def require_clean_committed():
    status=git_status()
    if status:
        raise RuntimeError(
            "STOP: EXP055 inference requires clean committed tree: "+status
        )

    required=[
        str(CONFIG.relative_to(ROOT)),
        str(Path(__file__).resolve().relative_to(ROOT)),
    ]

    for rel in required:
        result=subprocess.run(
            [
                "git","-C",str(ROOT),
                "ls-files","--error-unmatch",rel,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if result.returncode != 0:
            raise RuntimeError(
                "STOP: EXP055 inference requires committed file: "+rel
            )


def load_cohort(cfg):
    rows=read_csv(ROOT/cfg["scope"]["cohort_csv"])

    if len(rows) != int(cfg["scope"]["expected_videos"]):
        raise RuntimeError("Cohort row-count mismatch")

    videos=[r["video"] for r in rows]

    if videos != sorted(videos):
        raise RuntimeError("Cohort is not video-sorted")

    if len(videos) != len(set(videos)):
        raise RuntimeError("Duplicate cohort video")

    got=membership_hash("POSTDEFENSE_MIOU80",videos)

    if got != cfg["scope"]["membership_sha256"]:
        raise RuntimeError("Cohort membership SHA mismatch")

    if cfg["scope"]["sanity_video"] in set(videos):
        raise RuntimeError("Sanity video overlaps evaluation cohort")

    return rows,videos


def load_runtime(cfg):
    exp053=load_module(
        "exp053_for_exp055",
        ROOT/cfg["source_dependencies"]["exp053_script"]["path"],
    )

    exp053_cfg=json.loads(
        (
            ROOT
            / cfg["source_dependencies"]["exp053_config"]["path"]
        ).read_text(encoding="utf-8")
    )

    exp051,exp050,runtime=exp053.load_runtime(exp053_cfg)

    exp054=load_module(
        "exp054_for_exp055",
        ROOT/cfg["source_dependencies"]["exp054_bca_script"]["path"],
    )

    return exp053_cfg,exp051,exp050,runtime,exp054


def cache_path(cfg,video,label,sanity):
    root=Path(cfg["runtime"]["scratch_dir"])
    scope="sanity" if sanity else "cohort"
    return root/scope/"{}_{}.json".format(video,label)


def score_predictions(
    exp051,
    predictions,
    gt_cache,
    visibility,
    object_ids,
    n_frames,
):
    iou_sum=0.0
    count=0

    for frame_idx in range(1,int(n_frames)):
        if frame_idx not in predictions:
            raise RuntimeError(
                "Missing prediction frame {}".format(frame_idx)
            )

        for oid in object_ids:
            if not bool(visibility[oid][frame_idx]):
                continue

            if oid not in predictions[frame_idx]:
                raise RuntimeError(
                    "Missing prediction object {} frame {}".format(
                        oid,
                        frame_idx,
                    )
                )

            target=(gt_cache[frame_idx] == oid)

            value=float(
                exp051.iou_bool(
                    predictions[frame_idx][oid],
                    target,
                )
            )

            if not np.isfinite(value):
                raise RuntimeError("Non-finite IoU")

            if value < 0.0 or value > 1.0:
                raise RuntimeError("IoU outside [0,1]")

            iou_sum += value
            count += 1

    if count <= 0:
        raise RuntimeError("No evaluable GT-visible object-frames")

    return {
        "evaluable_object_frames":int(count),
        "iou_sum":float(iou_sum),
        "mean_iou":float(iou_sum/count),
    }


def validate_cached(cached,expected):
    for key,value in expected.items():
        if cached.get(key) != value:
            raise RuntimeError(
                "Cache identity mismatch for {}: {} != {}".format(
                    key,
                    cached.get(key),
                    value,
                )
            )

    n=int(cached["evaluable_object_frames"])
    total=float(cached["iou_sum"])
    mean=float(cached["mean_iou"])

    if n <= 0:
        raise RuntimeError("Cached denominator invalid")

    if not np.isfinite(total) or not np.isfinite(mean):
        raise RuntimeError("Cached IoU non-finite")

    if abs(mean-total/n) > 1e-12:
        raise RuntimeError("Cached IoU arithmetic mismatch")

    if not 0.0 <= mean <= 1.0:
        raise RuntimeError("Cached mean IoU outside [0,1]")

    return cached


def run_one(
    cfg,
    exp053_cfg,
    exp051,
    exp050,
    runtime,
    predictor,
    video,
    label,
    sanity,
):
    config_sha=sha256sum(CONFIG)
    script_sha=sha256sum(Path(__file__).resolve())

    expected={
        "experiment":"EXP055",
        "repo_commit":git_head(),
        "config_sha256":config_sha,
        "script_sha256":script_sha,
        "video":video,
        "run_label":label,
        "tracker_variant":cfg["methods"][label]["tracker_variant"],
        "tau":cfg["methods"][label]["tau"],
        "sanity":bool(sanity),
    }

    path=cache_path(cfg,video,label,sanity)

    if path.exists():
        cached=json.loads(path.read_text(encoding="utf-8"))
        return validate_cached(cached,expected),True

    ctx,gt_cache,visibility=exp051.context_gt(
        runtime,
        exp050,
        exp053_cfg,
        video,
    )

    if label == "B0":
        effective_tau=float(cfg["methods"]["B2"]["tau"])
    else:
        effective_tau=float(cfg["methods"][label]["tau"])

    run_cfg=exp051.make_run_cfg(
        runtime,
        exp050,
        exp053_cfg,
        ctx,
        effective_tau,
    )

    tracked=runtime["exp033"].run_tracker(
        predictor=predictor,
        jpg_dir=ctx["jpg_dir"],
        gt0=ctx["gt0"],
        object_ids=ctx["object_ids"],
        cfg=run_cfg,
        variant=cfg["methods"][label]["tracker_variant"],
        packs=runtime["packs"],
        deps=runtime["deps"],
    )

    eligible=int(ctx["n_frames"])-1

    if label == "B0":
        admit_count=eligible
        block_count=0
    else:
        decisions=tracked["decisions"]

        if len(decisions) != eligible:
            raise RuntimeError("B2 decision-count mismatch")

        admit_count=sum(
            row["action"] == "ADMIT"
            for row in decisions
        )

        block_count=sum(
            row["action"] == "BLOCK"
            for row in decisions
        )

        if admit_count+block_count != eligible:
            raise RuntimeError("B2 action-count mismatch")

        if not runtime["exp037"].block_integrity_pass(
            decisions,
            len(ctx["object_ids"]),
        ):
            raise RuntimeError("B2 block-integrity failure")

    score=score_predictions(
        exp051,
        tracked["predictions"],
        gt_cache,
        visibility,
        ctx["object_ids"],
        ctx["n_frames"],
    )

    result={
        **expected,
        "n_frames":int(ctx["n_frames"]),
        "n_objects":len(ctx["object_ids"]),
        "eligible_nonconditioning_frames":eligible,
        "admit_count":int(admit_count),
        "block_count":int(block_count),
        "write_rate":float(admit_count/eligible),
        "peak_vram_gb":float(tracked["peak_vram_gb"]),
        "runtime_sec":float(tracked["runtime_sec"]),
        **score,
    }

    path.parent.mkdir(parents=True,exist_ok=True)
    write_json_atomic(path,result)

    del tracked
    gc.collect()
    torch.cuda.empty_cache()

    return result,False


def paired_arrays(rows):
    by={}
    for row in rows:
        key=(row["video"],row["run_label"])
        if key in by:
            raise RuntimeError("Duplicate per-video result")
        by[key]=row

    videos=sorted({r["video"] for r in rows})

    if len(rows) != 2*len(videos):
        raise RuntimeError("Incomplete B0/B2 pairing")

    counts=[]
    sums_b0=[]
    sums_b2=[]
    means_b0=[]
    means_b2=[]

    for video in videos:
        b0=by[(video,"B0")]
        b2=by[(video,"B2")]

        n0=int(b0["evaluable_object_frames"])
        n2=int(b2["evaluable_object_frames"])

        if n0 != n2:
            raise RuntimeError(
                "Paired denominator mismatch for "+video
            )

        counts.append(n0)
        sums_b0.append(float(b0["iou_sum"]))
        sums_b2.append(float(b2["iou_sum"]))
        means_b0.append(float(b0["mean_iou"]))
        means_b2.append(float(b2["mean_iou"]))

    return (
        videos,
        np.asarray(counts,dtype=np.int64),
        np.asarray(sums_b0,dtype=np.float64),
        np.asarray(sums_b2,dtype=np.float64),
        np.asarray(means_b0,dtype=np.float64),
        np.asarray(means_b2,dtype=np.float64),
    )


def pooled_delta(counts,sums_b2,sums_b0):
    return float(
        sums_b2.sum()/counts.sum()
        - sums_b0.sum()/counts.sum()
    )


def video_balanced_delta(means_b2,means_b0):
    return float(
        np.mean(means_b2-means_b0)
    )


def bootstrap_inference(
    cfg,
    exp054,
    counts,
    sums_b0,
    sums_b2,
    means_b0,
    means_b2,
):
    n=len(counts)

    rng=np.random.default_rng(
        int(cfg["inference"]["seed"])
    )

    draw_index=rng.integers(
        0,
        n,
        size=(
            int(cfg["inference"]["bootstrap_replicates"]),
            n,
        ),
        dtype=np.int64,
    )

    denom=counts[draw_index].sum(axis=1,dtype=np.int64)

    primary_draws=(
        sums_b2[draw_index].sum(axis=1)/denom
        - sums_b0[draw_index].sum(axis=1)/denom
    )

    secondary_draws=np.mean(
        means_b2[draw_index]-means_b0[draw_index],
        axis=1,
    )

    observed_primary=pooled_delta(
        counts,
        sums_b2,
        sums_b0,
    )

    observed_secondary=video_balanced_delta(
        means_b2,
        means_b0,
    )

    total_n=int(counts.sum())
    total_b0=float(sums_b0.sum())
    total_b2=float(sums_b2.sum())

    jack_primary=np.empty(n,dtype=np.float64)
    jack_secondary=np.empty(n,dtype=np.float64)

    diff_means=means_b2-means_b0
    total_diff=float(diff_means.sum())

    for i in range(n):
        denom_i=total_n-int(counts[i])
        if denom_i <= 0:
            raise RuntimeError("Invalid delete-one-video denominator")

        jack_primary[i]=(
            (total_b2-float(sums_b2[i]))/denom_i
            - (total_b0-float(sums_b0[i]))/denom_i
        )

        jack_secondary[i]=(
            (total_diff-float(diff_means[i]))
            /(n-1)
        )

    primary_bca=exp054.bca_interval(
        observed_primary,
        primary_draws,
        jack_primary,
        float(cfg["inference"]["confidence"]),
    )

    secondary_bca=exp054.bca_interval(
        observed_secondary,
        secondary_draws,
        jack_secondary,
        float(cfg["inference"]["confidence"]),
    )

    return {
        "observed_primary":observed_primary,
        "observed_secondary":observed_secondary,
        "primary_draws":primary_draws,
        "secondary_draws":secondary_draws,
        "primary_bca":primary_bca,
        "secondary_bca":secondary_bca,
    }


def selftest():
    counts=np.asarray([2,3,4,1],dtype=np.int64)
    b0=np.asarray([1.0,1.5,2.0,0.5],dtype=np.float64)
    b2=np.asarray([1.2,1.8,2.1,0.6],dtype=np.float64)
    m0=b0/counts
    m2=b2/counts

    assert abs(
        pooled_delta(counts,b2,b0)-0.07
    ) < 1e-12

    expected=float(np.mean(m2-m0))
    assert abs(
        video_balanced_delta(m2,m0)-expected
    ) < 1e-12

    print("EXP055_SELFTEST=PASS")


def sanity():
    require_clean_committed()
    cfg=load_cfg()
    _,videos=load_cohort(cfg)

    video=cfg["scope"]["sanity_video"]
    if video in set(videos):
        raise RuntimeError("Sanity/evaluation overlap")

    exp053_cfg,exp051,exp050,runtime,_=load_runtime(cfg)

    model,predictor=exp050.build_predictor(runtime)
    del model

    rows=[]
    cache_hits=0

    for label in ("B0","B2"):
        result,hit=run_one(
            cfg,
            exp053_cfg,
            exp051,
            exp050,
            runtime,
            predictor,
            video,
            label,
            True,
        )
        rows.append(result)
        cache_hits += int(hit)

    if (
        int(rows[0]["evaluable_object_frames"])
        != int(rows[1]["evaluable_object_frames"])
    ):
        raise RuntimeError("Sanity paired denominator mismatch")

    print("sanity_video =",video)
    print(
        "evaluable_object_frames =",
        rows[0]["evaluable_object_frames"],
    )
    print("B0_mean_iou =",rows[0]["mean_iou"])
    print("B2_mean_iou =",rows[1]["mean_iou"])
    print("B2_write_rate =",rows[1]["write_rate"])
    print(
        "max_peak_vram_gb =",
        max(float(r["peak_vram_gb"]) for r in rows),
    )
    print("cache_hits =",cache_hits)
    print("evaluation_cohort_touched = false")
    print("EXP055_SANITY=PASS")


def run():
    require_clean_committed()
    cfg=load_cfg()
    _,videos=load_cohort(cfg)

    outputs=[
        ROOT/cfg["outputs"]["per_video_csv"],
        ROOT/cfg["outputs"]["summary_json"],
        ROOT/cfg["outputs"]["bootstrap_draws_csv"],
    ]

    if cfg["runtime"]["refuse_existing_inference_outputs"]:
        existing=[str(p) for p in outputs if p.exists()]
        if existing:
            raise RuntimeError(
                "STOP: inference output already exists: "
                +", ".join(existing)
            )

    exp053_cfg,exp051,exp050,runtime,exp054=load_runtime(cfg)

    model,predictor=exp050.build_predictor(runtime)
    del model

    rows=[]
    cache_hits=0
    cache_misses=0

    for index,video in enumerate(videos,start=1):
        print(
            "EXP055 video {}/{} {}".format(
                index,
                len(videos),
                video,
            ),
            flush=True,
        )

        for label in ("B0","B2"):
            result,hit=run_one(
                cfg,
                exp053_cfg,
                exp051,
                exp050,
                runtime,
                predictor,
                video,
                label,
                False,
            )

            rows.append(result)

            if hit:
                cache_hits += 1
            else:
                cache_misses += 1

            print(
                "  {} mean_iou={:.6f} write_rate={:.6f} "
                "peak_vram_gb={:.3f} cache_hit={}".format(
                    label,
                    float(result["mean_iou"]),
                    float(result["write_rate"]),
                    float(result["peak_vram_gb"]),
                    int(hit),
                ),
                flush=True,
            )

    (
        paired_videos,
        counts,
        sums_b0,
        sums_b2,
        means_b0,
        means_b2,
    )=paired_arrays(rows)

    if paired_videos != videos:
        raise RuntimeError("Final paired video order mismatch")

    inference=bootstrap_inference(
        cfg,
        exp054,
        counts,
        sums_b0,
        sums_b2,
        means_b0,
        means_b2,
    )

    fields=[
        "video",
        "run_label",
        "tracker_variant",
        "tau",
        "n_frames",
        "n_objects",
        "eligible_nonconditioning_frames",
        "evaluable_object_frames",
        "iou_sum",
        "mean_iou",
        "admit_count",
        "block_count",
        "write_rate",
        "peak_vram_gb",
        "runtime_sec",
    ]

    per_video_rows=[]

    for row in rows:
        per_video_rows.append({
            key:row[key]
            for key in fields
        })

    per_video_path=ROOT/cfg["outputs"]["per_video_csv"]
    draws_path=ROOT/cfg["outputs"]["bootstrap_draws_csv"]
    summary_path=ROOT/cfg["outputs"]["summary_json"]

    write_csv_atomic(
        per_video_path,
        fields,
        per_video_rows,
    )

    draw_rows=[
        {
            "replicate":i,
            "pooled_delta_b2_minus_b0":
                float(inference["primary_draws"][i]),
            "video_balanced_delta_b2_minus_b0":
                float(inference["secondary_draws"][i]),
        }
        for i in range(
            int(cfg["inference"]["bootstrap_replicates"])
        )
    ]

    write_csv_atomic(
        draws_path,
        [
            "replicate",
            "pooled_delta_b2_minus_b0",
            "video_balanced_delta_b2_minus_b0",
        ],
        draw_rows,
    )

    pooled_b0=float(sums_b0.sum()/counts.sum())
    pooled_b2=float(sums_b2.sum()/counts.sum())

    video_balanced_b0=float(np.mean(means_b0))
    video_balanced_b2=float(np.mean(means_b2))

    b0_rows=[r for r in rows if r["run_label"]=="B0"]
    b2_rows=[r for r in rows if r["run_label"]=="B2"]

    total_eligible=sum(
        int(r["eligible_nonconditioning_frames"])
        for r in b2_rows
    )

    total_admit=sum(
        int(r["admit_count"])
        for r in b2_rows
    )

    summary={
        "experiment":"EXP055",
        "status":"SUPPLEMENTARY_POSTDEFENSE_MIOU_COMPLETE",
        "scientific_status":
            "SUPPLEMENTARY_POSTDEFENSE_NONCONFIRMATORY",
        "repo_commit":git_head(),
        "config_sha256":sha256sum(CONFIG),
        "script_sha256":sha256sum(Path(__file__).resolve()),
        "videos":len(videos),
        "paired_runs":len(rows),
        "evaluable_object_frames":
            int(counts.sum()),
        "B0":{
            "pooled_mean_iou":pooled_b0,
            "video_balanced_mean_iou":
                video_balanced_b0,
            "pooled_write_rate":1.0,
        },
        "B2":{
            "tau":float(cfg["methods"]["B2"]["tau"]),
            "pooled_mean_iou":pooled_b2,
            "video_balanced_mean_iou":
                video_balanced_b2,
            "pooled_write_rate":
                float(total_admit/total_eligible),
        },
        "primary":{
            "contrast":"B2_minus_B0",
            "estimator":"pooled_object_frame_mean_iou",
            "delta":
                float(inference["observed_primary"]),
            "confidence":
                float(cfg["inference"]["confidence"]),
            "bootstrap_replicates":
                int(cfg["inference"]["bootstrap_replicates"]),
            "seed":
                int(cfg["inference"]["seed"]),
            "cluster_unit":"video",
            "bca":inference["primary_bca"],
        },
        "secondary":{
            "contrast":"B2_minus_B0",
            "estimator":"video_balanced_mean_iou",
            "delta":
                float(inference["observed_secondary"]),
            "bca":inference["secondary_bca"],
        },
        "runtime":{
            "cache_hits":cache_hits,
            "cache_misses":cache_misses,
            "max_peak_vram_gb":
                max(float(r["peak_vram_gb"]) for r in rows),
            "total_tracker_runtime_sec":
                float(sum(float(r["runtime_sec"]) for r in rows)),
        },
        "claim_boundary":{
            "postdefense_supplementary":True,
            "confirmatory_test_result":False,
            "exp053_exp054_conclusions_modified":False,
            "retraining_performed":False,
            "threshold_search_performed":False,
            "threshold_retuning_performed":False,
        },
        "output_hashes":{
            "per_video_miou.csv":
                sha256sum(per_video_path),
            "miou_bootstrap_draws.csv":
                sha256sum(draws_path),
        },
    }

    write_json_atomic(summary_path,summary)

    print("videos =",len(videos))
    print(
        "evaluable_object_frames =",
        int(counts.sum()),
    )
    print("B0_pooled_mean_iou =",pooled_b0)
    print("B2_pooled_mean_iou =",pooled_b2)
    print(
        "B2_minus_B0_pooled =",
        inference["observed_primary"],
    )
    print(
        "primary_BCa_95CI =",
        [
            inference["primary_bca"]["ci_lower"],
            inference["primary_bca"]["ci_upper"],
        ],
    )
    print(
        "B0_video_balanced_mean_iou =",
        video_balanced_b0,
    )
    print(
        "B2_video_balanced_mean_iou =",
        video_balanced_b2,
    )
    print(
        "B2_minus_B0_video_balanced =",
        inference["observed_secondary"],
    )
    print(
        "secondary_BCa_95CI =",
        [
            inference["secondary_bca"]["ci_lower"],
            inference["secondary_bca"]["ci_upper"],
        ],
    )
    print(
        "B2_pooled_write_rate =",
        total_admit/total_eligible,
    )
    print(
        "max_peak_vram_gb =",
        summary["runtime"]["max_peak_vram_gb"],
    )
    print("EXP055_RUN=PASS")


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument(
        "mode",
        choices=[
            "selftest",
            "sanity",
            "run",
        ],
    )
    args=parser.parse_args()

    if args.mode=="selftest":
        selftest()
    elif args.mode=="sanity":
        sanity()
    else:
        run()


if __name__=="__main__":
    main()
