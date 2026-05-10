# 🚀 MEMBRA Deployment Checklist

## Pre-Deployment (Local Testing)

- [ ] Code pushed to main branch
- [ ] All files committed: `git status` is clean
- [ ] `.env.local` files not committed (in .gitignore)
- [ ] ModernChat component loads without errors
- [ ] Chat API responds to requests: `curl http://localhost:8000/health`
- [ ] Streaming works in local development

## Render Setup

- [ ] Render.com account created
- [ ] GitHub repository connected to Render
- [ ] Created 2 new Web Services:
  - [ ] `membra-web` (Node.js)
  - [ ] `membra-api` (Python)
- [ ] Created PostgreSQL database
  - [ ] Name: `membra-db`
  - [ ] User: `membra`
  - [ ] Auto-configured DATABASE_URL
- [ ] Created Redis instance
  - [ ] Name: `membra-redis`
  - [ ] Auto-configured REDIS_URL

## Environment Variables

**For membra-web service:**
- [ ] `NEXT_PUBLIC_API_URL` = `https://your-api-service.onrender.com`

**For membra-api service:**
- [ ] `DATABASE_URL` (auto-set)
- [ ] `REDIS_URL` (auto-set)
- [ ] `OPENAI_API_KEY` (optional, if using OpenAI)
- [ ] `DEBUG=false`

## Build Configuration

**Both Services:**
- [ ] Using `render-new.yaml` for configuration OR manual settings:

**Web Service (membra-web):**
- [ ] Build Command: `npm install && npm run build`
- [ ] Start Command: `npm start`
- [ ] Root Directory: `apps/web`
- [ ] Node Version: 20+

**API Service (membra-api):**
- [ ] Build Command: `pip install -r requirements.txt`
- [ ] Start Command: `uvicorn apps.api.main:app --host 0.0.0.0 --port $PORT`
- [ ] Root Directory: `.`
- [ ] Python Version: 3.10+

## Deployment

- [ ] Click "Deploy" on both services
- [ ] Watch build logs for errors
- [ ] Wait for services to become "Live" (green checkmark)
- [ ] Build should complete in 3-5 minutes

## Post-Deployment Testing

### API Service
- [ ] Health check passes: `curl https://your-api.onrender.com/health`
- [ ] API docs load: Visit `https://your-api.onrender.com/docs`
- [ ] Chat endpoint responds to test:
  ```bash
  curl -X POST https://your-api.onrender.com/api/v1/chat \
    -H "Content-Type: application/json" \
    -d '{"message":"test","user_id":"user_123"}'
  ```

### Web Service
- [ ] Page loads: Visit `https://your-web.onrender.com`
- [ ] Chat interface visible with welcome message
- [ ] Can type in message box
- [ ] "Send" button is clickable
- [ ] Response appears when sending message
- [ ] Suggestions appear below response
- [ ] Can click suggestions to send them

### Full Integration
- [ ] Message history shows all messages
- [ ] Streaming responses appear correctly
- [ ] Suggestions are clickable
- [ ] Loading state appears while waiting
- [ ] Error message appears if API unreachable
- [ ] Mobile version looks good on phone
- [ ] Dark theme displays correctly

## Monitoring

**Daily:**
- [ ] Check Render dashboard for errors
- [ ] Monitor response times
- [ ] Check error logs
- [ ] Verify services are "Live"

**Weekly:**
- [ ] Review database size
- [ ] Check Redis memory usage
- [ ] Analyze chat patterns
- [ ] Monitor API latency

## Performance Benchmarks

After deployment, verify:
- [ ] Time to First Byte: < 500ms
- [ ] Largest Contentful Paint: < 2s
- [ ] Streaming starts within: < 500ms
- [ ] API response time: < 1s
- [ ] Database queries: < 100ms

## Troubleshooting

### If services won't start:
- [ ] Check build logs for errors
- [ ] Verify Python/Node versions
- [ ] Check environment variables are set
- [ ] Verify database credentials

### If web can't connect to API:
- [ ] Check `NEXT_PUBLIC_API_URL` is set correctly
- [ ] Verify API service is running
- [ ] Check CORS in API (should be enabled)
- [ ] Check browser console for errors

### If database won't connect:
- [ ] Verify DATABASE_URL is set
- [ ] Check database is running
- [ ] Review Render database logs
- [ ] Check for firewall issues

### If streaming is slow:
- [ ] Check API container memory
- [ ] Monitor database connections
- [ ] Review concurrent requests
- [ ] Check Redis cache hit rate

## Scaling (if needed)

- [ ] Monitor database size
  - [ ] Backup strategy configured
  - [ ] Connection pool size appropriate
  
- [ ] Monitor Redis
  - [ ] Memory usage < 80%
  - [ ] Eviction policy set
  - [ ] TTL on keys configured

- [ ] Monitor CPU/Memory
  - [ ] API CPU usage < 80%
  - [ ] Web CPU usage < 80%
  - [ ] Consider upgrade if > 90%

## Security Checklist

- [ ] DEBUG=false in production
- [ ] CORS only allows known origins (if updated)
- [ ] Database password is strong
- [ ] Environment variables not logged
- [ ] HTTPS enabled (Render default)
- [ ] Rate limiting configured (if needed)

## Documentation

- [ ] README.md updated with deployment info
- [ ] DEPLOYMENT_GUIDE.md reviewed
- [ ] API documentation is accessible
- [ ] Team knows how to deploy updates

## Final Sign-Off

- [ ] All tests passing
- [ ] Performance acceptable
- [ ] Monitoring enabled
- [ ] Team trained on deployment
- [ ] Ready for production traffic

---

## Success! 🎉

When all items are checked, your MEMBRA deployment with reimagined LLM UI/UX is complete and running live!

**Next Steps:**
1. Share the deployed URL with your team
2. Gather user feedback
3. Monitor performance regularly
4. Plan future enhancements

**Need Help?**
- See `DEPLOYMENT_GUIDE.md` for detailed instructions
- Check `README_DEPLOYMENT.md` for quick reference
- Review API docs at `/docs` endpoint

Let's go! 🚀
