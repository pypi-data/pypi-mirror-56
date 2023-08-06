# apperator

Apperator aims to be the simplest way to deploy on Kubernetes.

## Why?

I keep copy pasting manifests and changing a few values to deploy most of my things.

Might as well pull these few parameters away.

## But I don't want to use another tool to manage my stuff!

That's understandable. You can use apperator to generate manifests and apply them yourself.

## Usage

With `apperator.yaml` being:

```
apiVersion: apperator.simone.sh/v1alpha1
Kind: app
metadata:
  name: nginx
  namespace: nginx-testy
spec:
  create_namespace: True
  services:
  - image: nginx:alpine
    ingress:
    - hostname: nginx-testy.simone.sh
      tls:
        host: '*.simone.sh'
        secretName: wildcard-simone-sh-tls
      targetPort: 80
```
#### Docker

`cat apperator.yaml | docker run --rm -t chauffer/apperator build > manifests.yaml`

#### Python

`pip install apperator`
