
import json
import subprocess
import yaml
import pandas as pd
import mlflow

mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("tp3-dvc")

with open("params.yaml", encoding="utf-8") as f:
    P = yaml.safe_load(f)

with open("data/transactions.csv.dvc", encoding="utf-8") as f:
    ticket = yaml.safe_load(f)["outs"][0]

with open("reports/metrics.json", encoding="utf-8") as f:
    mets = json.load(f)

commit = subprocess.getoutput("git rev-parse --short HEAD")
n = len(pd.read_csv("data/transactions.csv"))

with mlflow.start_run(run_name=f"donnees-{ticket['md5'][:8]}"):
    mlflow.log_params(P["entrainement"])
    mlflow.log_metrics(mets)
    mlflow.set_tags({
        "commit": commit,
        "donnees_md5": ticket["md5"],
        "donnees_lignes": n,
    })
    mlflow.log_artifact("dvc.lock")

print(
    "run MLflow cree : donnees",
    ticket["md5"][:8],
    "-",
    n,
    "lignes",
)
