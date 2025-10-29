#!/bin/bash

echo "🗑️ Removing Food Token Scanner from Kubernetes..."

kubectl delete -f k8s/hpa.yaml
echo "✅ HorizontalPodAutoscaler deleted"

kubectl delete -f k8s/nodeport-service.yaml
echo "✅ NodePort Service deleted"

kubectl delete -f k8s/service.yaml
echo "✅ Service deleted"

kubectl delete -f k8s/deployment.yaml
echo "✅ Deployment deleted"

kubectl delete -f k8s/pvc.yaml
echo "✅ PersistentVolumeClaims deleted"

kubectl delete -f k8s/configmap.yaml
echo "✅ ConfigMap deleted"

kubectl delete -f k8s/namespace.yaml
echo "✅ Namespace deleted"

echo ""
echo "🎉 Cleanup completed!"
