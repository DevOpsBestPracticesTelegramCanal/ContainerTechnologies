# 📰 Container Technologies News - September 2025

**Сводка новостей по контейнерным технологиям за September 2025**

## 📊 Статистика месяца

- **Всего новостей:** 95
- **Новости по безопасности:** 24
- **Релизы с версиями:** 66
- **Основные категории:** cicd, docker, edge, kubernetes, microvm, monitoring, networking, podman, runtime, security, service-mesh, storage, webassembly

## 🔥 Важные новости (приоритет 5)

### Announcing Changed Block Tracking API support (alpha)
- **Источник:** Kubernetes Blog
- **Категория:** kubernetes
- **Дата:** 2025-09-25
- **Ссылка:** [Announcing Changed Block Tracking API support (alp...](https://kubernetes.io/blog/2025/09/25/csi-changed-block-tracking/)

<p>We're excited to announce the alpha support for a <em>changed block tracking</em> mechanism. This enhances
the Kubernetes storage ecosystem by providing an efficient way for
<a href="https://kubern...

---

### Kubernetes v1.34: Pod Level Resources Graduated to Beta
- **Источник:** Kubernetes Blog
- **Категория:** kubernetes
- **Дата:** 2025-09-22
- **Ссылка:** [Kubernetes v1.34: Pod Level Resources Graduated to...](https://kubernetes.io/blog/2025/09/22/kubernetes-v1-34-pod-level-resources/)

<p>On behalf of the Kubernetes community, I am thrilled to announce that the Pod Level Resources feature has graduated to Beta in the Kubernetes v1.34 release and is enabled by default! This significa...

---

### Kubernetes v1.34: Recovery From Volume Expansion Failure (GA)
- **Источник:** Kubernetes Blog
- **Категория:** kubernetes
- **Дата:** 2025-09-19
- **Ссылка:** [Kubernetes v1.34: Recovery From Volume Expansion F...](https://kubernetes.io/blog/2025/09/19/kubernetes-v1-34-recover-expansion-failure/)

<p>Have you ever made a typo when expanding your persistent volumes in Kubernetes? Meant to specify <code>2TB</code>
but specified <code>20TiB</code>? This seemingly innocuous problem was kinda hard t...

---

### Kubernetes v1.34: DRA Consumable Capacity
- **Источник:** Kubernetes Blog
- **Категория:** kubernetes
- **Дата:** 2025-09-18
- **Ссылка:** [Kubernetes v1.34: DRA Consumable Capacity...](https://kubernetes.io/blog/2025/09/18/kubernetes-v1-34-dra-consumable-capacity/)

<p>Dynamic Resource Allocation (DRA) is a Kubernetes API for managing scarce resources across Pods and containers.
It enables flexible resource requests, going beyond simply allocating <em>N</em> numb...

---

### Kubernetes v1.34: Pods Report DRA Resource Health
- **Источник:** Kubernetes Blog
- **Категория:** kubernetes
- **Дата:** 2025-09-17
- **Ссылка:** [Kubernetes v1.34: Pods Report DRA Resource Health...](https://kubernetes.io/blog/2025/09/17/kubernetes-v1-34-pods-report-dra-resource-health/)

<p>The rise of AI/ML and other high-performance workloads has made specialized hardware like GPUs, TPUs, and FPGAs a critical component of many Kubernetes clusters. However, as discussed in a <a href=...

---

### Kubernetes v1.34: Moving Volume Group Snapshots to v1beta2
- **Источник:** Kubernetes Blog
- **Категория:** kubernetes
- **Дата:** 2025-09-16
- **Ссылка:** [Kubernetes v1.34: Moving Volume Group Snapshots to...](https://kubernetes.io/blog/2025/09/16/kubernetes-v1-34-volume-group-snapshot-beta-2/)

<p>Volume group snapshots were <a href="https://kubernetes.io/blog/2023/05/08/kubernetes-1-27-volume-group-snapshot-alpha/">introduced</a>
as an Alpha feature with the Kubernetes 1.27 release and move...

---

### Kubernetes v1.34: Decoupled Taint Manager Is Now Stable
- **Источник:** Kubernetes Blog
- **Категория:** kubernetes
- **Дата:** 2025-09-15
- **Ссылка:** [Kubernetes v1.34: Decoupled Taint Manager Is Now S...](https://kubernetes.io/blog/2025/09/15/kubernetes-v1-34-decoupled-taint-manager-is-now-stable/)

<p>This enhancement separates the responsibility of managing node lifecycle and pod eviction into two distinct components.
Previously, the node lifecycle controller handled both marking nodes as unhea...

---

### Kubernetes v1.34: Autoconfiguration for Node Cgroup Driver Goes GA
- **Источник:** Kubernetes Blog
- **Категория:** kubernetes
- **Дата:** 2025-09-12
- **Ссылка:** [Kubernetes v1.34: Autoconfiguration for Node Cgrou...](https://kubernetes.io/blog/2025/09/12/kubernetes-v1-34-cri-cgroup-driver-lookup-now-ga/)

<p>Historically, configuring the correct cgroup driver has been a pain point for users running new
Kubernetes clusters. On Linux systems, there are two different cgroup drivers:
<code>cgroupfs</code> ...

---

### Kubernetes v1.34: Mutable CSI Node Allocatable Graduates to Beta
- **Источник:** Kubernetes Blog
- **Категория:** kubernetes
- **Дата:** 2025-09-11
- **Ссылка:** [Kubernetes v1.34: Mutable CSI Node Allocatable Gra...](https://kubernetes.io/blog/2025/09/11/kubernetes-v1-34-mutable-csi-node-allocatable-count/)

<p>The <a href="https://kep.k8s.io/4876">functionality for CSI drivers to update information about attachable volume count on the nodes</a>, first introduced as Alpha in Kubernetes v1.33, has graduate...

---

### Kubernetes v1.34: Use An Init Container To Define App Environment Variables
- **Источник:** Kubernetes Blog
- **Категория:** kubernetes
- **Дата:** 2025-09-10
- **Ссылка:** [Kubernetes v1.34: Use An Init Container To Define ...](https://kubernetes.io/blog/2025/09/10/kubernetes-v1-34-env-files/)

<p>Kubernetes typically uses ConfigMaps and Secrets to set environment variables,
which introduces additional API calls and complexity,
For example, you need to separately manage the Pods of your work...

---

## 📋 По категориям

### CICD (8 новостей)

- **[v3.1.8...](https://github.com/argoproj/argo-cd/releases/tag/v3.1.8)** *ArgoCD Releases* - 2025-09-30
- **[v3.0.19...](https://github.com/argoproj/argo-cd/releases/tag/v3.0.19)** *ArgoCD Releases* - 2025-09-30
- **[v3.2.0-rc2...](https://github.com/argoproj/argo-cd/releases/tag/v3.2.0-rc2)** *ArgoCD Releases* - 2025-09-30
- **[v2.14.20...](https://github.com/argoproj/argo-cd/releases/tag/v2.14.20)** *ArgoCD Releases* - 2025-09-30
- **[v2.7.0...](https://github.com/fluxcd/flux2/releases/tag/v2.7.0)** *Flux Releases* - 2025-09-30

### DOCKER (3 новостей)

- **[v28.5.0-rc.1...](https://github.com/moby/moby/releases/tag/v28.5.0-rc.1)** *Docker Releases* - 2025-09-25
- **[v2.0.0-beta.0: moby 2.0.0-beta.0...](https://github.com/moby/moby/releases/tag/v2.0.0-beta.0)** *Docker Releases* - 2025-09-06
- **[moby client/v0.1.0-beta.0...](https://github.com/moby/moby/releases/tag/client%2Fv0.1.0-beta.0)** *Docker Releases* - 2025-09-05

### EDGE (10 новостей)

- **[v1.34.1+k3s1...](https://github.com/k3s-io/k3s/releases/tag/v1.34.1%2Bk3s1)** *K3s Releases* - 2025-09-24
- **[v1.33.5+k3s1...](https://github.com/k3s-io/k3s/releases/tag/v1.33.5%2Bk3s1)** *K3s Releases* - 2025-09-24
- **[v1.32.9+k3s1...](https://github.com/k3s-io/k3s/releases/tag/v1.32.9%2Bk3s1)** *K3s Releases* - 2025-09-24
- **[v1.31.13+k3s1...](https://github.com/k3s-io/k3s/releases/tag/v1.31.13%2Bk3s1)** *K3s Releases* - 2025-09-24
- **[v1.30.14-rc3+k3s3...](https://github.com/k3s-io/k3s/releases/tag/v1.30.14-rc3%2Bk3s3)** *K3s Releases* - 2025-09-17

### KUBERNETES (30 новостей)

- **[Namespaces: A Step-By-Step Guide to Kubernetes Isolation...](https://thenewstack.io/namespaces-a-step-by-step-guide-to-kubernetes-isolation/)** *The New Stack K8s* - 2025-09-29
- **[kubectl cp: Copying Files to and From Kubernetes Pods...](https://thenewstack.io/kubectl-cp-copying-files-to-and-from-kubernetes-pods/)** *The New Stack K8s* - 2025-09-27
- **[Announcing Changed Block Tracking API support (alpha)...](https://kubernetes.io/blog/2025/09/25/csi-changed-block-tracking/)** *Kubernetes Blog* - 2025-09-25
- **[Top 10 Kubernetes Deployment Errors: Causes and Fixes (And T...](https://thenewstack.io/top-10-kubernetes-deployment-errors-causes-and-fixes-and-tips/)** *The New Stack K8s* - 2025-09-24
- **[Kubernetes v1.34: Pod Level Resources Graduated to Beta...](https://kubernetes.io/blog/2025/09/22/kubernetes-v1-34-pod-level-resources/)** *Kubernetes Blog* - 2025-09-22

### MICROVM (2 новостей)

- **[Kata Containers 3.21.0...](https://github.com/kata-containers/kata-containers/releases/tag/3.21.0)** *Kata Containers Releases* - 2025-09-24
- **[Firecracker v1.13.1...](https://github.com/firecracker-microvm/firecracker/releases/tag/v1.13.1)** *Firecracker Releases* - 2025-09-01

### MONITORING (7 новостей)

- **[12.2.0...](https://github.com/grafana/grafana/releases/tag/v12.2.0)** *Grafana Releases* - 2025-09-24
- **[12.1.2...](https://github.com/grafana/grafana/releases/tag/v12.1.2)** *Grafana Releases* - 2025-09-23
- **[12.0.5...](https://github.com/grafana/grafana/releases/tag/v12.0.5)** *Grafana Releases* - 2025-09-23
- **[11.6.6...](https://github.com/grafana/grafana/releases/tag/v11.6.6)** *Grafana Releases* - 2025-09-23
- **[11.5.9...](https://github.com/grafana/grafana/releases/tag/v11.5.9)** *Grafana Releases* - 2025-09-23

### NETWORKING (2 новостей)

- **[1.16.15...](https://github.com/cilium/cilium/releases/tag/1.16.15)** *Cilium Releases* - 2025-09-22
- **[1.17.8...](https://github.com/cilium/cilium/releases/tag/1.17.8)** *Cilium Releases* - 2025-09-22

### PODMAN (2 новостей)

- **[v5.6.2...](https://github.com/containers/podman/releases/tag/v5.6.2)** *Podman Releases* - 2025-09-30
- **[v5.6.1...](https://github.com/containers/podman/releases/tag/v5.6.1)** *Podman Releases* - 2025-09-04

### RUNTIME (5 новостей)

- **[containerd 2.2.0-beta.0...](https://github.com/containerd/containerd/releases/tag/v2.2.0-beta.0)** *containerd Releases* - 2025-09-18
- **[v1.34.0...](https://github.com/cri-o/cri-o/releases/tag/v1.34.0)** *CRI-O Releases* - 2025-09-10
- **[v1.33.4...](https://github.com/cri-o/cri-o/releases/tag/v1.33.4)** *CRI-O Releases* - 2025-09-02
- **[v1.32.8...](https://github.com/cri-o/cri-o/releases/tag/v1.32.8)** *CRI-O Releases* - 2025-09-02
- **[v1.31.12...](https://github.com/cri-o/cri-o/releases/tag/v1.31.12)** *CRI-O Releases* - 2025-09-02

### SECURITY (10 новостей)

- **[v0.67.0...](https://github.com/aquasecurity/trivy/releases/tag/v0.67.0)** *Trivy Releases* - 2025-09-30
- **[v1.9.0...](https://github.com/open-policy-agent/opa/releases/tag/v1.9.0)** *OPA Releases* - 2025-09-26
- **[Malicious NPM packages: Are you exposed?...](https://www.sysdig.com/blog/malicious-npm-packages-are-you-exposed)** *Sysdig Blog* - 2025-09-25
- **[How runtime insights power every cloud security use case...](https://www.sysdig.com/blog/how-runtime-insights-power-every-cloud-security-use-case)** *Sysdig Blog* - 2025-09-22
- **[AI for SOC teams: 5 cloud security prompts to start your day...](https://www.sysdig.com/blog/ai-for-soc-teams-5-cloud-security-prompts-to-start-your-day-with-sysdig-sage)** *Sysdig Blog* - 2025-09-19

### SERVICE-MESH (4 новостей)

- **[edge-25.9.4...](https://github.com/linkerd/linkerd2/releases/tag/edge-25.9.4)** *Linkerd Releases* - 2025-09-25
- **[edge-25.9.3...](https://github.com/linkerd/linkerd2/releases/tag/edge-25.9.3)** *Linkerd Releases* - 2025-09-18
- **[edge-25.9.2...](https://github.com/linkerd/linkerd2/releases/tag/edge-25.9.2)** *Linkerd Releases* - 2025-09-12
- **[Istio 1.27.1...](https://github.com/istio/istio/releases/tag/1.27.1)** *Istio Releases* - 2025-09-03

### STORAGE (8 новостей)

- **[Longhorn v1.9.2...](https://github.com/longhorn/longhorn/releases/tag/v1.9.2)** *Longhorn Releases* - 2025-09-24
- **[Longhorn v1.10.0-rc4...](https://github.com/longhorn/longhorn/releases/tag/v1.10.0-rc4)** *Longhorn Releases* - 2025-09-23
- **[Longhorn v1.9.2-rc2...](https://github.com/longhorn/longhorn/releases/tag/v1.9.2-rc2)** *Longhorn Releases* - 2025-09-22
- **[Longhorn v1.10.0-rc3...](https://github.com/longhorn/longhorn/releases/tag/v1.10.0-rc3)** *Longhorn Releases* - 2025-09-18
- **[Longhorn v1.9.2-rc1...](https://github.com/longhorn/longhorn/releases/tag/v1.9.2-rc1)** *Longhorn Releases* - 2025-09-11

### WEBASSEMBLY (4 новостей)

- **[v37.0.1: Release Wasmtime 37.0.1 (#11738)...](https://github.com/bytecodealliance/wasmtime/releases/tag/v37.0.1)** *Wasmtime Releases* - 2025-09-23
- **[v37.0.0: Release Wasmtime 37.0.0 (#11724)...](https://github.com/bytecodealliance/wasmtime/releases/tag/v37.0.0)** *Wasmtime Releases* - 2025-09-20
- **[WasmEdge 0.15.0...](https://github.com/WasmEdge/WasmEdge/releases/tag/0.15.0)** *WasmEdge Releases* - 2025-09-10
- **[WasmEdge 0.14.1...](https://github.com/WasmEdge/WasmEdge/releases/tag/0.14.1)** *WasmEdge Releases* - 2025-09-10

## 🔒 Безопасность

- **[v0.67.0](https://github.com/aquasecurity/trivy/releases/tag/v0.67.0)**
  *Trivy Releases* - 2025-09-30
  <h2><a href="https://github.com/aquasecurity/trivy/discussions/9550">👉 Trivy v0.67.0 release notes (click here)</a></h2>
<h2>⬇️ Download Trivy</h2>
<u...

- **[v1.9.0](https://github.com/open-policy-agent/opa/releases/tag/v1.9.0)**
  *OPA Releases* - 2025-09-26
  <p>This release contains a mix of new features, performance improvements, and bugfixes. Notably:</p>
<ul>
<li>Compile API extensions ported from EOPA<...

- **[edge-25.9.4](https://github.com/linkerd/linkerd2/releases/tag/edge-25.9.4)**
  *Linkerd Releases* - 2025-09-25
  <h2>What's Changed</h2>
<ul>
<li>build(deps): bump tokio-rustls from 0.26.2 to 0.26.3 by <a class="user-mention notranslate" href="https://github.com/...

- **[Longhorn v1.9.2](https://github.com/longhorn/longhorn/releases/tag/v1.9.2)**
  *Longhorn Releases* - 2025-09-24
  <h2>Longhorn v1.9.2 Release Notes</h2>
<p>Longhorn 1.9.2 introduces several improvements and bug fixes that are intended to improve system quality, re...

- **[Kata Containers 3.21.0](https://github.com/kata-containers/kata-containers/releases/tag/3.21.0)**
  *Kata Containers Releases* - 2025-09-24
  <h2>Survey</h2>
<p>Please take the Kata Containers survey:</p>
<ul>
<li><a href="https://openinfrafoundation.formstack.com/forms/kata_containers_user_...

## 🚀 Релизы

- **v5.6.2** - `v5.6.2`
  *Podman Releases* - [v5.6.2...](https://github.com/containers/podman/releases/tag/v5.6.2)

- **v3.1.8** - `v3.1.8`
  *ArgoCD Releases* - [v3.1.8...](https://github.com/argoproj/argo-cd/releases/tag/v3.1.8)

- **v3.0.19** - `v3.0.19`
  *ArgoCD Releases* - [v3.0.19...](https://github.com/argoproj/argo-cd/releases/tag/v3.0.19)

- **v3.2.0-rc2** - `v3.2.0`
  *ArgoCD Releases* - [v3.2.0-rc2...](https://github.com/argoproj/argo-cd/releases/tag/v3.2.0-rc2)

- **v2.14.20** - `v2.14.20`
  *ArgoCD Releases* - [v2.14.20...](https://github.com/argoproj/argo-cd/releases/tag/v2.14.20)

- **v0.67.0** - `v0.67.0`
  *Trivy Releases* - [v0.67.0...](https://github.com/aquasecurity/trivy/releases/tag/v0.67.0)

- **v2.7.0** - `v2.7.0`
  *Flux Releases* - [v2.7.0...](https://github.com/fluxcd/flux2/releases/tag/v2.7.0)

- **v1.9.0** - `v1.9.0`
  *OPA Releases* - [v1.9.0...](https://github.com/open-policy-agent/opa/releases/tag/v1.9.0)

- **edge-25.9.4** - `25.9.4`
  *Linkerd Releases* - [edge-25.9.4...](https://github.com/linkerd/linkerd2/releases/tag/edge-25.9.4)

- **v28.5.0-rc.1** - `v28.5.0`
  *Docker Releases* - [v28.5.0-rc.1...](https://github.com/moby/moby/releases/tag/v28.5.0-rc.1)

## 📡 Источники (26)

ArgoCD Releases, CRI-O Releases, Cilium Releases, Cosign Releases, Docker Releases, Firecracker Releases, Flux Releases, Grafana Releases, Istio Releases, Jaeger Releases, K3s Releases, Kata Containers Releases, Kubernetes Blog, Kubernetes Releases, Linkerd Releases, Longhorn Releases, OPA Releases, OpenEBS Releases, Podman Releases, Sysdig Blog, Tekton Releases, The New Stack K8s, Trivy Releases, WasmEdge Releases, Wasmtime Releases, containerd Releases

---

*Автоматически сгенерировано системой сбора новостей*  
*Последнее обновление: 2025-10-31 13:07*
