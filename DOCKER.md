# 🐳 Docker Deployment Guide

## Quick Start with Docker

### Prerequisites
- Docker installed on your system
- Docker Compose (optional, but recommended)

### Method 1: Using Docker Compose (Recommended)

1. **Set environment variables**
   ```bash
   export BOT_TOKEN="your_bot_token_here"
   export ADMIN_ID="your_admin_id_here"
   ```

2. **Start the bot**
   ```bash
   docker-compose up -d
   ```

3. **View logs**
   ```bash
   docker-compose logs -f
   ```

4. **Stop the bot**
   ```bash
   docker-compose down
   ```

### Method 2: Using Docker directly

1. **Build the image**
   ```bash
   docker build -t telegram-stars-bot .
   ```

2. **Run the container**
   ```bash
   docker run -d \
     --name telegram-bot \
     --restart unless-stopped \
     -e BOT_TOKEN="your_bot_token_here" \
     -e ADMIN_ID="your_admin_id_here" \
     -v $(pwd)/bot_database.json:/app/bot_database.json \
     telegram-stars-bot
   ```

3. **View logs**
   ```bash
   docker logs -f telegram-bot
   ```

4. **Stop the container**
   ```bash
   docker stop telegram-bot
   docker rm telegram-bot
   ```

## Managing the Bot

### Check if bot is running
```bash
docker ps | grep telegram
```

### Access container shell
```bash
docker exec -it telegram-bot /bin/bash
```

### View real-time logs
```bash
docker logs -f telegram-bot
```

### Restart the bot
```bash
docker restart telegram-bot
```

### Update the bot
1. Stop the container:
   ```bash
   docker-compose down
   ```

2. Pull latest changes:
   ```bash
   git pull
   ```

3. Rebuild and start:
   ```bash
   docker-compose up -d --build
   ```

## Backup and Restore

### Backup database
```bash
docker cp telegram-bot:/app/bot_database.json ./backup_$(date +%Y%m%d).json
```

### Restore database
```bash
docker cp ./backup_20240101.json telegram-bot:/app/bot_database.json
docker restart telegram-bot
```

## Troubleshooting

### Bot not starting
1. Check environment variables:
   ```bash
   docker exec telegram-bot env | grep BOT
   ```

2. View detailed logs:
   ```bash
   docker logs telegram-bot
   ```

### Database issues
1. Check if database file exists:
   ```bash
   docker exec telegram-bot ls -la /app/
   ```

2. Check permissions:
   ```bash
   docker exec telegram-bot ls -la bot_database.json
   ```

### Container keeps restarting
```bash
docker logs --tail 100 telegram-bot
```

## Production Deployment

### Using Docker Swarm

1. **Initialize swarm**
   ```bash
   docker swarm init
   ```

2. **Create secrets**
   ```bash
   echo "your_bot_token" | docker secret create bot_token -
   echo "your_admin_id" | docker secret create admin_id -
   ```

3. **Deploy stack**
   ```bash
   docker stack deploy -c docker-compose.yml telegram-bot
   ```

### Using Kubernetes

Create `deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: telegram-bot
spec:
  replicas: 1
  selector:
    matchLabels:
      app: telegram-bot
  template:
    metadata:
      labels:
        app: telegram-bot
    spec:
      containers:
      - name: telegram-bot
        image: telegram-stars-bot:latest
        env:
        - name: BOT_TOKEN
          valueFrom:
            secretKeyRef:
              name: bot-secrets
              key: bot-token
        - name: ADMIN_ID
          valueFrom:
            secretKeyRef:
              name: bot-secrets
              key: admin-id
        volumeMounts:
        - name: data
          mountPath: /app/data
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: bot-data
```

Deploy:
```bash
kubectl apply -f deployment.yaml
```

## Monitoring

### Resource usage
```bash
docker stats telegram-bot
```

### Disk usage
```bash
docker system df
```

### Clean up
```bash
docker system prune -a
```

## Security Best Practices

1. **Never hardcode secrets** - Use environment variables
2. **Run as non-root** - Add USER directive in Dockerfile
3. **Update regularly** - Keep base image and dependencies updated
4. **Scan for vulnerabilities**:
   ```bash
   docker scan telegram-stars-bot
   ```

5. **Use secrets management** - For production, use Docker secrets or Kubernetes secrets

## Performance Optimization

### Reduce image size
- Use multi-stage builds
- Remove unnecessary dependencies
- Use .dockerignore file

### Optimize resource limits
```yaml
services:
  telegram-bot:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

## Additional Tools

### Portainer (Web UI for Docker)
```bash
docker run -d -p 9000:9000 \
  --name portainer \
  --restart always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  portainer/portainer-ce
```

Access at: http://localhost:9000

### Watchtower (Auto-update containers)
```bash
docker run -d \
  --name watchtower \
  -v /var/run/docker.sock:/var/run/docker.sock \
  containrrr/watchtower \
  telegram-bot
```

---

🐳 Happy Dockerizing! ⭐️
