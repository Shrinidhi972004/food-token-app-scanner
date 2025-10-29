#!/bin/bash

echo "🚀 Deploying Food Token Scanner to Kubernetes..."

kubectl apply -f k8s/namespace.yaml
echo "✅ Namespace created"

kubectl apply -f k8s/configmap.yaml
echo "✅ ConfigMap created"

kubectl apply -f k8s/pvc.yaml
echo "✅ PersistentVolumeClaims created"

kubectl apply -f k8s/deployment.yaml
echo "✅ Deployment created"

kubectl apply -f k8s/service.yaml
echo "✅ Service created"

kubectl apply -f k8s/nodeport-service.yaml
echo "✅ NodePort Service created"

kubectl apply -f k8s/hpa.yaml
echo "✅ HorizontalPodAutoscaler created"

echo ""
echo "🎉 Deployment completed!"
echo ""
echo "📋 Check status:"
echo "kubectl get pods -n food-token-scanner"
echo "kubectl get svc -n food-token-scanner"
echo ""
echo "🌐 Access the application:"
echo "NodePort: http://NODE_IP:30080"
echo ""
echo "📊 Monitor deployment:"
echo "kubectl logs -f deployment/food-token-scanner -n food-token-scanner"
