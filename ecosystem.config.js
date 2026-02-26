module.exports = {
  apps: [
    {
      name: 'gmail-watcher',
      script: 'watchers/gmail_watcher.py',
      interpreter: 'python3',
      watch: false,
      autorestart: true,
      max_restarts: 10,
      min_uptime: '10s',
      error_file: 'AI_Employee_Vault/Logs/pm2-gmail-error.log',
      out_file: 'AI_Employee_Vault/Logs/pm2-gmail-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z'
    },
    {
      name: 'whatsapp-watcher',
      script: 'watchers/whatsapp_watcher.py',
      interpreter: 'python3',
      watch: false,
      autorestart: true,
      max_restarts: 10,
      min_uptime: '10s',
      error_file: 'AI_Employee_Vault/Logs/pm2-whatsapp-error.log',
      out_file: 'AI_Employee_Vault/Logs/pm2-whatsapp-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z'
    },
    {
      name: 'linkedin-watcher',
      script: 'watchers/linkedin_watcher.py',
      interpreter: 'python3',
      watch: false,
      autorestart: true,
      max_restarts: 10,
      min_uptime: '10s',
      error_file: 'AI_Employee_Vault/Logs/pm2-linkedin-error.log',
      out_file: 'AI_Employee_Vault/Logs/pm2-linkedin-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z'
    }
  ]
};
