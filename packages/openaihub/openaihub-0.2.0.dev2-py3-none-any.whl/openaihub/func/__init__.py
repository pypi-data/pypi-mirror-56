# Copyright 2019 IBM Corporation 
# 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
# 
#     http://www.apache.org/licenses/LICENSE-2.0 
# 
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License. 
from __future__ import print_function
import logging
import sys
import platform
import subprocess
import time
from git import Repo
import tempfile
import os
import tarfile
import shutil
import yaml
import re

# set up the k8s dynamic client
from kubernetes import client, config
from openshift.dynamic import DynamicClient

if os.path.exists('/proc/self/cgroup'):
    with open('/proc/self/cgroup', 'r') as f:
        if 'kubepod' in f.read():
            config.load_incluster_config()
            k8s_config = client.Configuration()
            k8s_client = client.api_client.ApiClient(configuration=k8s_config)
        else:
            k8s_client = config.new_client_from_config()
else:
    k8s_client = config.new_client_from_config()
dyn_client = DynamicClient(k8s_client)

# set up logger
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

def untar_data():
    # untar the required and registry data
    import tarfile
    basedir = tempfile.mkdtemp()
    tar = tarfile.open(os.path.join(os.path.dirname(__file__), '..', 'data', 'data.tgz'))
    tar.extractall(path=basedir)
    tar.close()
    return basedir

def find(pattern, path):
    # pylint: disable=unused-variable
    for root, dirs, files in os.walk(path):
        for f in files:
            if re.search(pattern, f) != None:
                return os.path.join(root, f)

def run(cmd):
    ret = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    logger.info("Command: %s, Returncode: %s" % (ret.args, ret.returncode))
    return(ret)

def check_call(func, args):
    ret = func(args)
    if ret.returncode != 0:
        logger.error("Command %s failed with Error: %s" % (args, ret.stderr.decode()), exc_info=1)
        sys.exit(ret.returncode)

def wait_for(operator, namespace):
    # exit after 600 seconds
    # pylint: disable=unused-variable
    for x in range(40):
        if run("kubectl rollout status deployment/%s-operator -n %s" % (operator, namespace)).returncode != 0:
            time.sleep(15)
        else:
            break
        
def check_installed(namespace):
    csv = dyn_client.resources.get(api_version='operators.coreos.com/v1alpha1', kind='ClusterServiceVersion')
    csv_list = csv.get(namespace=namespace)
    if csv_list is not None and csv_list.items != []:
        return ([x.metadata.name for x in csv_list.items])
    return None
        
def get_installed_csv(namespace, operator):
    csv = dyn_client.resources.get(api_version='operators.coreos.com/v1alpha1', kind='ClusterServiceVersion')
    csv_list = csv.get(namespace=namespace)
    for x in csv_list.items:
        if x.metadata.name.startswith(operator):
            return (x)
    return None

def is_operator_installed(namespace, package_name): # TBD: add csv version
    csv = get_csv(namespace, package_name)
    if csv is not None:
        operator = csv.currentCSV
        csv = dyn_client.resources.get(api_version='operators.coreos.com/v1alpha1', kind='ClusterServiceVersion')
        csv_list = csv.get(namespace=namespace)
        return (True in [x.metadata.name.startswith(operator) for x in csv_list.items])
    return (False)

def get_csv(namespace, package_name):
    pm = dyn_client.resources.get(api_version='packages.operators.coreos.com/v1', kind='PackageManifest')
    pm_list = pm.get(namespace=namespace)
    for x in pm_list.items:
        if x.metadata.name == package_name:
            # return channel[0] for now
            return (x.status.channels[0])
    return None

def get_applications(namespace, package_name, logpath='./openaihub-applications.log', loglevel='INFO', openshift=False, csv=None):
    logger.setLevel(loglevel.upper())
    logger.addHandler(logging.FileHandler(logpath))
    if csv is None:
        csv = get_csv(namespace, package_name)
    if csv is not None:
        apps = [{"kind" : x.kind, "name" : x.name} for x in csv.currentCSVDesc.customresourcedefinitions.owned]
        return (apps)

def install_operator_internal(namespace, package_name):
    pm = dyn_client.resources.get(api_version='packages.operators.coreos.com/v1', kind='PackageManifest')
    pm_list = pm.get(namespace=namespace)
    for x in pm_list.items:
        if x.metadata.name == package_name:
            basedir = untar_data()
            subscription_path = os.path.join(basedir, 'src/registry/subscription')
            y = yaml.safe_load(open(os.path.join(subscription_path, 'template.yaml')))
            y['spec']['channel'] = x.status.channels[0].name
            y['spec']['name'] = x.status.packageName
            y['spec']['source'] = x.status.catalogSource
            y['metadata']['name'] = package_name
            subs = dyn_client.resources.get(kind='Subscription')
            subs.create(body=y)
            # remove temp
            shutil.rmtree(basedir, ignore_errors=True)

def install_application(namespace, package_name, application, logpath, loglevel, openshift, operator_version=None, custom_resource=None):
    logger.setLevel(loglevel.upper())
    logger.addHandler(logging.FileHandler(logpath))

    # if operator is not installed, install it to 'operators' namespace
    if not is_operator_installed("operators", package_name):
        install_operator_internal("operators", package_name)

    # install application
    csv = get_csv(namespace, package_name)
    logger.info("### ClusterServiceVersion for the application: %s..." % str(csv)[:120])
    op_apps = get_applications(namespace, package_name, csv=csv)
    logger.info("### applications in this package: %s" % str(op_apps))
    if op_apps is None or not application in [x['kind'] for x in op_apps]:
        # error
        logger.error("Error: application %s is not found in the package." % application)
        exit(1)

    # app_crd = next(x for x in op_apps if x['kind'] == 'SparkCluster')['name']
    crs = dyn_client.resources.get(kind=application)
    logger.info("### CustomResourceDefinition for the application: %s" % str(crs))
    if custom_resource is None:
        for x in yaml.safe_load(csv.currentCSVDesc.annotations['alm-examples']):
            if x['kind'] == application:
                x['metadata']['namespace'] = namespace
                crs.create(body=x)
    else:
        crs.create(body=yaml.safe_load(open(custom_resource)))
    logger.info("### application is created, check cluster pod and event for status: %s" % str(crs.get(namespace=namespace).items))
    return

def uninstall_application(namespace, application, name, logpath, loglevel, openshift):
    logger.setLevel(loglevel.upper())
    logger.addHandler(logging.FileHandler(logpath))

    apps = dyn_client.resources.get(kind=application)
    if not name in [x.metadata.name for x in apps.get(namespace=namespace).items]:
        logger.error("### Application %s/%s does not exist in namespace %s" % (application, name, namespace))
        exit(1)
    apps.delete(namespace=namespace, name=name)
    logger.info("### application is deleted, check cluster logs for status.")
    return

def install_operator(operator, subscription_file, logpath, loglevel, openshift):
    logger.setLevel(loglevel.upper())
    logger.addHandler(logging.FileHandler(logpath))

    basedir = untar_data()
    subscription_path = os.path.join(basedir, 'src/registry/subscription')

    steps = 3 if subscription_file == '' else 2

    # check whether the operator is registered
    step = 1
    logger.info("### %s/%s ### Check if the operator is registered..." % (step, steps))
    check_call(run, "kubectl get packagemanifest %s" % operator)

    # generate subscription file if not provided
    if subscription_file == '':
        subscription_file = os.path.join(subscription_path, operator + ".yaml")
        run("sed 's/OPERATOR/%s/g' %s/template.yaml > %s" % (operator, subscription_path, subscription_file))

        # retrieve details of this operator
        run("kubectl get packagemanifest %s -o yaml > %s/%s.package.yaml" % (operator, subscription_path, operator))
        package_yaml = yaml.safe_load(open("%s/%s.package.yaml" % (subscription_path, operator)))
        channel = package_yaml['status']['channels'][0]['name']
        package_name = package_yaml['status']['packageName']
        source = package_yaml['status']['catalogSource']
        run("sed -i %s 's/CHANNEL/%s/' %s" % ("''" if platform.system() == 'Darwin' else '', channel, subscription_file))
        run("sed -i %s 's/PACKAGE/%s/' %s" % ("''" if platform.system() == 'Darwin' else '', package_name, subscription_file))
        run("sed -i %s 's/SOURCE/%s/' %s" % ("''" if platform.system() == 'Darwin' else '', source, subscription_file))

        step += 1
        logger.info("### %s/%s ### Generate the subscription file..." % (step, steps))

    # install the operator
    step += 1
    logger.info("### %s/%s ### Install the operator..." % (step, steps))
    
    # create ConfigMap to set the kubectl client version for operators
    if run("kubectl get configmap openaihub-install-config -n operators").returncode != 0:
        kube_version = run("kubectl version --short|grep Server|awk '{ print $3;exit}'|cut -d'+' -f1").stdout.decode().rstrip()
        check_call(run, "kubectl create configmap openaihub-install-config --from-literal=KUBECTL_VERSION=%s -n operators" % kube_version)

    check_call(run, "kubectl apply -f %s" % subscription_file)

    # remove temp
    shutil.rmtree(basedir, ignore_errors=True)

    logger.info("Done.")

    return CompletedOperator(operator, 0)

class CompletedOperator:
    def __init__(self, operator_name, returncode):
        self.operator_name = operator_name
        self.returncode = returncode

def register(path, operator, logpath, loglevel, openshift):
    logger.setLevel(loglevel.upper())
    logger.addHandler(logging.FileHandler(os.path.join(logpath, "openaihub-%s.log" % operator)))

    basedir = untar_data()
    kaniko_path = os.path.join(basedir, "src/registry/kaniko")

    steps = 8

    # unpack operator tgz files to src/registry/operators
    step = 1
    logger.info("### %s/%s ### Unpack operator tgz..." % (step, steps))
    operator_path = os.path.join(kaniko_path, "operators", operator)
    os.makedirs(operator_path, exist_ok=True)
    tf = tarfile.open(os.path.join(path, operator + ".tgz"), "r:gz")
    tf.extractall(operator_path)

    # search for clusterserviceversion yaml file and get operator name
    csv_yaml = find("clusterserviceversion.yaml", operator_path)
    if csv_yaml == None:
        logger.error("Error: the file %s/%s.tgz does not contain valid operator." % (path, operator))
        sys.exit(1)
    csv_parsed = yaml.safe_load(open(csv_yaml))
    operator_name = csv_parsed['spec']['install']['spec']['deployments'][0]['name']

    # create context.tgz
    step += 1
    logger.info("### %s/%s ### Create build-context..." % (step, steps))
    kaniko_tgz = os.path.join(basedir, "kaniko.tgz")
    tf = tarfile.open(kaniko_tgz, "w:gz")
    tf.add(os.path.join(kaniko_path, "Dockerfile"), arcname="Dockerfile")
    tf.add(os.path.join(kaniko_path, "operators"), arcname="operators")
    tf.close()

    # create docker-config ConfigMap
    step += 1
    logger.info("### %s/%s ### Create docker config..." % (step, steps))
    if run("kubectl get configmap docker-config").returncode != 0:
        check_call(run, "kubectl create configmap docker-config --from-file=%s/config.json" % kaniko_path)

    # modify kaniko.yaml with operator destination
    step += 1
    kaniko_pod = "kaniko-" + operator
    logger.info("### %s/%s ### Create kaniko pod..." % (step, steps))
    run("sed -i %s 's/IMAGETAG/docker.io\/ffdlops\/%s-catalog:v0.0.1/' %s/kaniko.yaml" % ("''" if platform.system() == 'Darwin' else '', operator, kaniko_path))
    run("sed -i %s 's/OPERATOR/%s/' %s/kaniko.yaml" % ("''" if platform.system() == 'Darwin' else '', operator, kaniko_path))

    # create kaniko pod
    check_call(run, "kubectl apply -f %s/kaniko.yaml" % kaniko_path)

    # wait for the pod to be ready
    time.sleep(60)

    # copy build context to kaniko container
    step += 1
    logger.info("### %s/%s ### Set up kaniko job..." % (step, steps))
    run("kubectl cp %s %s:/tmp/context.tar.gz -c kaniko-init" % (kaniko_tgz, kaniko_pod))
    run("kubectl exec %s -c kaniko-init -- tar -zxf /tmp/context.tar.gz -C /kaniko/build-context" % kaniko_pod)
    run("kubectl exec %s -c kaniko-init -- touch /tmp/complete" % kaniko_pod)

    # now wait for the image to be built and ready
    step += 1
    logger.info("### %s/%s ### Wait for the image to be ready..." % (step, steps))
    # pylint: disable=unused-variable
    for x in range(40):
        if run("kubectl get pod/%s|grep %s|awk '{ print $3;exit}'" % (kaniko_pod, kaniko_pod)).stdout.decode() != "Completed\n" :
            time.sleep(15)
        else:
            break

    # delete the kaniko pod
    step += 1
    logger.info("### %s/%s ### Delete the kaniko pod..." % (step, steps))
    run("kubectl delete -f %s/kaniko.yaml" % kaniko_path)

    # generate catalog source yaml
    step += 1
    logger.info("### %s/%s ### Deploy the catalog..." % (step, steps))
    run("sed -i %s 's/REPLACE_OPERATOR/%s/' %s/catalogsource.yaml" % ("''" if platform.system() == 'Darwin' else '', operator, kaniko_path))
    run("sed -i %s 's/REPLACE_IMAGE/docker.io\/ffdlops\/%s-catalog:v0.0.1/' %s/catalogsource.yaml" % ("''" if platform.system() == 'Darwin' else '', operator, kaniko_path))

    # deploy the catalog
    check_call(run, "kubectl apply -f %s/catalogsource.yaml" % kaniko_path)

    # wait until the operator is showing in the packagemanifest
    # pylint: disable=unused-variable
    for x in range(40):
        if run("kubectl get packagemanifest %s" % operator_name).returncode != 0 :
            time.sleep(15)
        else:
            break

    # remove temp
    shutil.rmtree(basedir, ignore_errors=True)

    logger.info("Done.")

    return CompletedOperator(operator_name, 0)

def install(namespace, storage, logpath, loglevel, openshift):
    logger.setLevel(loglevel.upper())
    logger.addHandler(logging.FileHandler(os.path.join(logpath, "openaihub-install.log")))
    
    basedir = untar_data()

    steps = 16 if storage == "nfs" else 15

    # prereq: helm must be installed already
    # init helm tiller service account
    step = 1
    logger.info("### %s/%s ### Init helm tiller..." % (step, steps))
    run("kubectl apply -f %s/src/requirement/helm-tiller.yaml" % basedir)
    run("helm init --service-account tiller --upgrade")

    catalog_path = os.path.join(basedir, "src/registry/catalog_source")
    subscription_path = os.path.join(basedir, "src/registry/subscription")
    cr_path = os.path.join(basedir, "src/registry/cr_samples")
    patch_path = os.path.join(basedir, "src/patch")

    # install OLM
    step += 1
    logger.info("### %s/%s ### Install OLM if not installed..." % (step, steps))
    olm_operator_status = run("kubectl rollout status deployment/olm-operator -n olm").returncode
    catalog_operator_status = run("kubectl rollout status deployment/catalog-operator -n olm").returncode
    if olm_operator_status != 0 or catalog_operator_status != 0:
        olm_version = "0.11.0"
        import wget
        wget.download("https://github.com/operator-framework/operator-lifecycle-manager/releases/download/%s/install.sh" % olm_version, out="%s/install.sh" % basedir)
        run("bash %s/install.sh %s" % (basedir, olm_version))
        wait_for("olm", "olm")
        wait_for("catalog", "olm")
        
        # TODO: investigate the memory increase problem in OLM and provide proper fix, for now, limit the memory
        check_call(run, "kubectl patch deployment olm-operator --patch \"$(cat %s/olm-patch.yaml)\" -n olm" % patch_path)
        check_call(run, "kubectl patch deployment catalog-operator --patch \"$(cat %s/catalog-patch.yaml)\" -n olm" % patch_path)

        # install olm-console
        run("kubectl apply -f %s/src/requirement/olm-console.yaml" % basedir)
    else:
        logger.info("OLM already exists.")

    # add openaihub catalog
    step += 1
    logger.info("### %s/%s ### Add OpenAIHub operators catalog..." % (step, steps))
    check_call(run, "kubectl apply -f %s/openaihub.catalogsource.yaml" % catalog_path)
    # pylint: disable=unused-variable
    for x in range(40):
        if run("kubectl get packagemanifest|grep OpenAIHub|wc -l").stdout.decode().lstrip().rstrip() != "5":
            time.sleep(15)
        else:
            break

    # create namespace
    step += 1
    logger.info("### %s/%s ### Create namespace and add cluster admin..." % (step, steps))
    if run("kubectl get namespace %s" % namespace).returncode != 0:
        if openshift:
            check_call(run, "oc new-project %s" % namespace)
        else:
            check_call(run, "kubectl create namespace %s" % namespace)

    # add cluster-admin to default service account for registration and installation of other operators
    if run("kubectl get clusterrolebinding add-on-cluster-admin-openaihub").returncode != 0:
        if openshift:
            check_call(run, "oc adm policy add-cluster-role-to-user cluster-admin -z default")
        else:
            check_call(run, "kubectl create clusterrolebinding add-on-cluster-admin-openaihub --clusterrole=cluster-admin --serviceaccount=%s:default" % namespace)

    # create ConfigMap to set the kubectl client version for operators
    if run("kubectl get configmap openaihub-install-config -n operators").returncode != 0:
        kube_version = run("kubectl version --short|grep Server|awk '{ print $3;exit}'|cut -d'+' -f1").stdout.decode().rstrip()
        check_call(run, "kubectl create configmap openaihub-install-config --from-literal=KUBECTL_VERSION=%s -n operators" % kube_version)

    # special handling for openshift
    if openshift:
        run("oc adm policy add-scc-to-user privileged -z default")
        run("oc adm policy add-scc-to-user anyuid -z ambassador")
        run("oc adm policy add-scc-to-user anyuid -z default")
        run("oc adm policy add-scc-to-group anyuid system:authenticated")
        run("oc adm policy add-scc-to-group privileged system:serviceaccounts:kubeflow")

    # create jupyterlab operator
    step += 1
    logger.info("### %s/%s ### Deploy Jupyterlab operator..." % (step, steps))
    check_call(run, "kubectl apply -f %s/%s-operator.yaml" % (subscription_path, "jupyterlab"))

    # wait until jupyterlab operator is available
    step += 1
    logger.info("### %s/%s ### Wait until Jupyterlab operator is available..." % (step, steps))
    wait_for("jupyterlab", "operators")

    # create jupyterlab cr
    step += 1
    logger.info("### %s/%s ### Create Jupyterlab deployment..." % (step, steps))
    check_call(run, "kubectl apply -f %s/openaihub_v1alpha1_%s_cr.yaml -n %s" % (cr_path, "jupyterlab", namespace))

    # switch default storageclass to nfs-dynamic
    if not openshift:
        if storage == "nfs":
            step += 1
            logger.info("### %s/%s ### Wait for nfs-dynamic storageclass to be ready and set as default..." % (step, steps))
            # pylint: disable=unused-variable
            for x in range(40):
                if run("kubectl get storageclass |grep nfs-dynamic").stdout.decode() == '':
                    time.sleep(15)
                else:
                    break
            run("kubectl patch storageclass ibmc-file-bronze -p '{\"metadata\": {\"annotations\":{\"storageclass.kubernetes.io/is-default-class\":\"false\"}}}'")
            check_call(run, "kubectl patch storageclass nfs-dynamic -p '{\"metadata\": {\"annotations\":{\"storageclass.kubernetes.io/is-default-class\":\"true\"}}}'")

    # create pipelines operator
    step += 1
    logger.info("### %s/%s ### Deploy Pipelines operator..." % (step, steps))
    check_call(run, "kubectl apply -f %s/%s-operator.yaml" % (subscription_path, "pipelines"))

    # wait until pipelines operator is available
    step += 1
    logger.info("### %s/%s ### Wait until Pipelines operator is available..." % (step, steps))
    wait_for("pipelines", "operators")

    # create pipelines cr
    step += 1
    logger.info("### %s/%s ### Create Pipelines deployment..." % (step, steps))
    check_call(run, "kubectl apply -f %s/openaihub_v1alpha1_%s_cr.yaml -n %s" % (cr_path, "pipelines", namespace))

    if openshift:
        # pylint: disable=unused-variable
        for x in range(80):
            if run("oc get pods -o=jsonpath='{range .items[*]}{@.metadata.name}{\" \"}{@.status.phase}{\"\\n\"}' |grep argo-ui|cut -d' ' -f2").stdout.decode().rstrip() != "Running" :
                time.sleep(15)
            else:
                break
        run("oc adm policy add-scc-to-user anyuid -z pipeline-runner")
        run("oc adm policy add-cluster-role-to-user cluster-admin -z pipeline-runner")
        
        run("oc get clusterrole argo -o yaml > %s/argo.yaml" % patch_path)
        argo_patch(os.path.join(patch_path, "argo.yaml"))
        run("oc apply -f %s/argo.yaml" % patch_path)

        run("oc get deployment minio -o yaml > %s/minio.yaml" % patch_path)
        run("sed -i '/subPath: minio/d' %s/minio.yaml" % patch_path)
        run("oc apply -f %s/minio.yaml" % patch_path)

    # create openaihub operator
    step += 1
    logger.info("### %s/%s ### Deploy OpenAIHub operator..." % (step, steps))
    check_call(run, "kubectl apply -f %s/%s-operator.yaml" % (subscription_path, "openaihub"))

    # wait until openaihub operator is available
    step += 1
    logger.info("### %s/%s ### Wait until OpenAIHub operator is available..." % (step, steps))
    wait_for("openaihub", "operators")

    # create openaihub cr
    step += 1
    logger.info("### %s/%s ### Create OpenAIHub deployment..." % (step, steps))
    check_call(run, "kubectl apply -f %s/openaihub_v1alpha1_%s_cr.yaml -n %s" % (cr_path, "openaihub", namespace))

    # special handling for openshift
    if openshift:
        # pylint: disable=unused-variable
        for x in range(80):
            if run("oc get pods -o=jsonpath='{range .items[*]}{@.metadata.name}{\" \"}{@.status.phase}{\"\\n\"}' |grep openaihub-ui|cut -d' ' -f2").stdout.decode().rstrip() != "Running" :
                time.sleep(15)
            else:
                break

        public_ip = os.getenv("PUBLIC_IP")
        run("oc get deployment openaihub-ui -o yaml > %s/openaihub-ui.yaml" % patch_path)
        run("sed -i 's/<none>/%s/g' %s/openaihub-ui.yaml" % (public_ip, patch_path))
        run("oc apply -f %s/openaihub-ui.yaml" % patch_path)

    # create kubeflow operator
    step += 1
    logger.info("### %s/%s ### Deploy Kubeflow operator..." % (step, steps))
    check_call(run, "kubectl apply -f %s/%s-operator.yaml" % (subscription_path, "kubeflow"))

    # wait until kubeflow operator is available
    step += 1
    logger.info("### %s/%s ### Wait until Kubeflow operator is available..." % (step, steps))
    wait_for("kubeflow", "operators")

    # give permssion for kubeflow-operator
    if openshift:
        run("oc adm policy add-cluster-role-to-user cluster-admin -z kubeflow-operator -n operators")

    # create kubeflow cr
    step += 1
    logger.info("### %s/%s ### Create Kubeflow deployment..." % (step, steps))
    check_call(run, "kubectl apply -f %s/openaihub_v1alpha1_%s_cr.yaml -n %s" % (cr_path, "kubeflow", namespace))

    # update clusterrole
    if openshift:
        # pylint: disable=unused-variable
        for x in range(80):
            if run("oc get pods -o=jsonpath='{range .items[*]}{@.metadata.name}{\" \"}{@.status.phase}{\"\\n\"}' |grep studyjob-controller|cut -d' ' -f2").stdout.decode().rstrip() != "Running" :
                time.sleep(15)
            else:
                break        
        run("oc get clusterrole studyjob-controller -o yaml > %s/studyjob.yaml" % patch_path)
        studyjob_patch(os.path.join(patch_path, "studyjob.yaml"))
        run("oc apply -f %s/studyjob.yaml" % patch_path)

    # remove temp
    shutil.rmtree(basedir, ignore_errors=True)

    logger.info("Done.")

def argo_patch(path):
  y = yaml.safe_load(open(path))
  del y["metadata"]
  y["metadata"] = dict()
  y["metadata"]["labels"] = dict()
  y["metadata"]["labels"]["app"] = "argo"
  y["metadata"]["name"] = "argo"
  for x in y["rules"]:
    if "pods" in x["resources"]:
      x["verbs"].append('delete')
    elif "workflows" in x["resources"]:
      x["resources"].append('workflows/finalizers')
  yaml.dump(y, open(path,'w'), default_flow_style=False)

def studyjob_patch(path):
  y = yaml.safe_load(open(path))
  del y["metadata"]
  y["metadata"] = dict()
  y["metadata"]["name"] = "studyjob-controller"
  for x in y["rules"]:
    if "jobs" in x["resources"]:
      x["resources"].append('jobs/finalizers')
    elif "tfjobs" in x["resources"]:
      x["resources"].append('tfjobs/finalizers')
      x["resources"].append('pytorchjobs/finalizers')
  yaml.dump(y, open(path,'w'), default_flow_style=False)

__all__ = ["install", 
           "install_operator", 
           "register", 
           "install_application", 
           "uninstall_application",
           "get_applications"]
