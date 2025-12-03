# 🚀 Deployment Guide - Anime Bot

## Local Deployment (Orzilik)

### Linux/macOS

1. **Setup**
```bash
python setup.py
```

2. **Start Bot**
```bash
python main.py
```

3. **Background Mode**
```bash
nohup python main.py > logs/bot.log 2>&1 &
```

4. **Check Running**
```bash
ps aux | grep "python main.py"
```

5. **Stop Bot**
```bash
pkill -f "python main.py"
```

## Docker Deployment

### Quick Start

1. **Build Image**
```bash
docker build -t anime-bot .
```

2. **Run Container**
```bash
docker run -d \
  --name anime-bot \
  -e TOKEN=YOUR_BOT_TOKEN \
  -v $(pwd)/anime_bot.db:/app/anime_bot.db \
  -v $(pwd)/logs:/app/logs \
  anime-bot
```

3. **Using Docker Compose**
```bash
cp .env.example .env
nano .env  # Edit and add TOKEN
docker-compose up -d
```

4. **View Logs**
```bash
docker logs -f anime-bot
```

5. **Stop Container**
```bash
docker-compose down
```

## VPS Deployment (Ubuntu)

### 1. Server Setup

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y python3.11 python3-pip git sqlite3
```

### 2. Clone Repository

```bash
cd /home/username
git clone https://github.com/yourusername/anime-bot.git
cd anime-bot
```

### 3. Setup Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Configure

```bash
cp .env.example .env
nano .env
# Edit TOKEN va ADMIN_IDS
```

### 5. Systemd Service Setup

Create `/etc/systemd/system/anime-bot.service`:

```ini
[Unit]
Description=Anime Telegram Bot
After=network.target

[Service]
Type=simple
User=username
WorkingDirectory=/home/username/anime-bot
Environment="PATH=/home/username/anime-bot/venv/bin"
ExecStart=/home/username/anime-bot/venv/bin/python main.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable service:
```bash
sudo systemctl enable anime-bot
sudo systemctl start anime-bot
sudo systemctl status anime-bot
```

## Heroku Deployment

### 1. Procfile Create

```
worker: python main.py
```

### 2. runtime.txt

```
python-3.11.0
```

### 3. Deploy

```bash
heroku login
heroku create your-anime-bot
heroku config:set TOKEN=YOUR_BOT_TOKEN
heroku config:set ADMIN_IDS=123456789
git push heroku main
```

### 4. Check Logs

```bash
heroku logs --tail
```

## AWS EC2 Deployment

### 1. Launch Instance

- AMI: Ubuntu 22.04 LTS
- Instance Type: t2.micro (free tier)

### 2. Security Group

Allow:
- SSH (22) from your IP
- Outbound: All

### 3. Connect

```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

### 4. Setup

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip git
git clone https://github.com/yourusername/anime-bot.git
cd anime-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env
```

### 5. Start

```bash
nohup python main.py > bot.log 2>&1 &
```

## DigitalOcean App Platform

### 1. app.yaml

```yaml
name: anime-bot
services:
- name: bot
  github:
    repo: yourusername/anime-bot
    branch: main
  build_command: pip install -r requirements.txt
  run_command: python main.py
  envs:
  - key: TOKEN
    scope: RUN_TIME
    value: ${TOKEN}
```

### 2. Deploy

```bash
doctl apps create --spec app.yaml
```

## Railway.app Deployment

### 1. Connect Repository

- Go to railway.app
- Create new project
- Connect GitHub repo

### 2. Configure

Add environment variables:
- TOKEN
- ADMIN_IDS

### 3. Deploy

Railway automatically deploys on push to main.

## Production Checklist

- [ ] TOKEN sozlandi
- [ ] ADMIN_IDS qo'shildi
- [ ] MANDATORY_CHANNELS sozlandi
- [ ] Database backup enabled
- [ ] Logs monitored
- [ ] Rate limiting enabled
- [ ] Error handling tested
- [ ] Admin panel tested
- [ ] Subscription check tested

## Monitoring

### Log Files

```bash
tail -f logs/bot.log
tail -f logs/admin.log
tail -f logs/errors.log
```

### Database Backup

```bash
# Manual backup
cp anime_bot.db backups/anime_bot_$(date +%Y%m%d_%H%M%S).db

# Automatic backup (cron)
0 2 * * * cp /path/to/anime_bot.db /path/to/backups/anime_bot_$(date +\%Y\%m\%d).db
```

### Health Check

```bash
curl -I http://localhost:8080/health
```

## Troubleshooting

### Bot not responding

1. Check logs
```bash
tail -f logs/bot.log
```

2. Check database
```bash
sqlite3 anime_bot.db "SELECT COUNT(*) FROM users;"
```

3. Restart
```bash
python setup.py
python main.py
```

### High CPU Usage

- Check for infinite loops
- Review rate limiting
- Check database queries

### Database Locked

```bash
# Check locks
lsof | grep anime_bot.db

# Restart process
pkill -f "python main.py"
python main.py
```

## Updates

### Pull Latest Code

```bash
git pull origin main
pip install -r requirements.txt
python setup.py
```

### Database Migration

```bash
python -c "from database import Database; Database().init_database()"
```

## Scaling

### Vertical Scaling

- Upgrade server resources
- Increase RAM/CPU

### Horizontal Scaling

- Use load balancer
- Multiple bot instances
- Shared database

## Performance Tips

1. Enable database indexing
2. Archive old logs
3. Clean old user history
4. Optimize queries
5. Use caching for frequent queries

## Security

- [ ] Change default admin ID
- [ ] Use strong passwords
- [ ] Enable HTTPS for APIs
- [ ] Regular backups
- [ ] Monitor access logs
- [ ] Update dependencies
- [ ] Use environment variables for secrets

## Costs Estimation

| Platform | Free Tier | Paid |
|----------|-----------|------|
| Heroku | 550 hours | $7-50/mo |
| Railway | $5 | $5+/mo |
| DigitalOcean | - | $4/mo |
| AWS EC2 | 1 year free | $5+/mo |
| VPS | - | $3-10/mo |

---

**Last Updated:** 2024
**Version:** 1.0.0
