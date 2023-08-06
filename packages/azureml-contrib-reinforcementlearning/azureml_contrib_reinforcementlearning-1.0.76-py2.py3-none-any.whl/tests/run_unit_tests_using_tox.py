import subprocess
import os

# Get latest pip to catch pip errors faster
subprocess.check_call(["python", "-m", "pip", "install", "-U", "pip"])

# Install and run tox. The configuration is at the top level of the module
subprocess.check_call(["python", "-m", "pip", "install", "-U", "tox"])

curdir = os.path.dirname(os.path.abspath(__file__))
aml_core_path = os.path.join(curdir, "../../azureml-core")
hd_rest_client_path = os.path.join(curdir, "../../azureml-train-restclients-hyperdrive")
aml_telemetry_path = os.path.join(curdir, "../../azureml-telemetry")
aml_contrib_nb_path = os.path.join(curdir, "../../azureml-contrib-notebook")
aml_pipeline_core_path = os.path.join(curdir, "../../azureml-pipeline-core")
aml_train_core_path = os.path.join(curdir, "../../azureml-train-core")
aml_pipeline_steps_path = os.path.join(curdir, "../../azureml-pipeline-steps")
aml_rl_path = os.path.join(curdir, "../../azureml-contrib-reinforcementlearning")
subprocess.check_call(["python", "-m", "pip", "install", "-e", aml_core_path])
subprocess.check_call(["python", "-m", "pip", "install", "-e", hd_rest_client_path])
subprocess.check_call(["python", "-m", "pip", "install", "-e", aml_telemetry_path])
subprocess.check_call(["python", "-m", "pip", "install", "-e", aml_contrib_nb_path])
subprocess.check_call(["python", "-m", "pip", "install", "-e", aml_pipeline_core_path])
subprocess.check_call(["python", "-m", "pip", "install", "-e", aml_train_core_path])
subprocess.check_call(["python", "-m", "pip", "install", "-e", aml_pipeline_steps_path])
subprocess.check_call(["python", "-m", "pip", "install", "-e", aml_rl_path])
subprocess.check_call(["python", "-m", "tox"])
