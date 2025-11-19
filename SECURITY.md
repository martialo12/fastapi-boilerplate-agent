# Security Policy

## Supported Versions

We release patches for security vulnerabilities. Which versions are eligible for receiving such patches depends on the CVSS v3.0 Rating:

| Version | Supported          |
| ------- | ------------------ |
| 0.2.x   | :white_check_mark: |
| 0.1.x   | :x:                |
| < 0.1   | :x:                |

## Reporting a Vulnerability

We take the security of FastAPI Boilerplate Generator seriously. If you believe you have found a security vulnerability, please report it to us as described below.

### Please do NOT:

- Open a public GitHub issue
- Discuss the vulnerability in public forums or social media
- Exploit the vulnerability beyond what is necessary to demonstrate it

### Please DO:

1. **Email us directly** at: [martialo218@gmail.com](mailto:martialo218@gmail.com)
2. Include the following information:
   - Type of issue (e.g. SQL injection, XSS, code injection)
   - Full paths of source file(s) related to the issue
   - Location of the affected source code (tag/branch/commit or direct URL)
   - Step-by-step instructions to reproduce the issue
   - Proof-of-concept or exploit code (if possible)
   - Impact of the issue, including how an attacker might exploit it

### What to expect:

- **Initial Response**: We will acknowledge receipt of your vulnerability report within 48 hours
- **Assessment**: We will investigate and assess the severity of the issue
- **Fix Development**: We will work on a fix and keep you informed of progress
- **Disclosure**: Once a fix is available, we will:
  - Release a security advisory
  - Credit you for the discovery (unless you prefer to remain anonymous)
  - Notify users of the vulnerability and the fix

### Security Update Process:

1. The security team will investigate the report
2. A fix will be developed and tested
3. A new version will be released
4. A security advisory will be published
5. Users will be notified through:
   - GitHub Security Advisories
   - Release notes
   - Email notifications (for critical issues)

## Security Best Practices

When using FastAPI Boilerplate Generator:

### For Generator Users:

1. **OpenAI API Key Security**:
   - Never commit your `.env` file to version control
   - Use environment variables or secure secret management
   - Rotate API keys regularly
   - Monitor API usage for anomalies

2. **Generated Code Review**:
   - Review all generated code before deploying to production
   - Update dependencies to their latest secure versions
   - Configure proper authentication and authorization
   - Enable HTTPS in production

3. **Database Security**:
   - Change default database credentials immediately
   - Use strong passwords
   - Restrict database access by IP
   - Enable SSL/TLS for database connections
   - Regular backups

4. **Docker Security** (if using Docker):
   - Don't run containers as root
   - Keep base images updated
   - Scan images for vulnerabilities
   - Use minimal base images

### For Generated Projects:

1. **Environment Variables**:
   ```bash
   # Never commit secrets
   echo ".env" >> .gitignore
   ```

2. **Dependency Updates**:
   ```bash
   # Keep dependencies up to date
   pip install --upgrade pip
   pip list --outdated
   ```

3. **Security Headers**:
   ```python
   # Add security middleware in generated projects
   from fastapi.middleware.cors import CORSMiddleware
   from fastapi.middleware.trustedhost import TrustedHostMiddleware
   ```

4. **Input Validation**:
   - Use Pydantic models for all inputs
   - Validate and sanitize user input
   - Implement rate limiting

## Known Security Considerations

### Generated Code:

1. **Default Credentials**: Generated docker-compose files use default credentials. **CHANGE THESE** before deployment.

2. **CORS Settings**: Default CORS settings may be permissive. Configure appropriately for your environment.

3. **Debug Mode**: Ensure debug mode is disabled in production:
   ```python
   # In main.py, do NOT use in production:
   if __name__ == "__main__":
       import uvicorn
       uvicorn.run(app, debug=False)  # Debug should be False
   ```

4. **SQL Injection**: While using SQLAlchemy ORM provides protection, always use parameterized queries.

5. **Secret Management**: The generated `.env` file should never be committed. Use proper secret management in production (AWS Secrets Manager, Azure Key Vault, etc.).

## Security Checklist for Generated Projects

Before deploying a generated project to production:

- [ ] Changed all default passwords and secrets
- [ ] Configured CORS properly
- [ ] Disabled debug mode
- [ ] Updated all dependencies
- [ ] Implemented authentication and authorization
- [ ] Configured HTTPS/SSL
- [ ] Set up monitoring and logging
- [ ] Implemented rate limiting
- [ ] Configured security headers
- [ ] Set up database backups
- [ ] Restricted database access
- [ ] Implemented input validation
- [ ] Set up error handling (don't expose stack traces)
- [ ] Configured CSP (Content Security Policy)
- [ ] Set up WAF (Web Application Firewall) if needed

## Vulnerability Disclosure Timeline

- **Day 0**: Vulnerability reported
- **Day 1-2**: Initial assessment and acknowledgment
- **Day 3-7**: Investigation and fix development
- **Day 8-14**: Testing and validation
- **Day 15**: Security advisory and patch release
- **Day 30**: Full public disclosure (if applicable)

## Contact

For security issues: [martialo218@gmail.com](mailto:martialo218@gmail.com)

For general questions: [GitHub Discussions](https://github.com/martialo12/fastapi-boilerplate-agent/discussions)

## Attribution

We appreciate and acknowledge security researchers who report vulnerabilities responsibly. With your permission, we will credit you in:

- Security advisories
- Release notes
- Our security hall of fame (coming soon)

## Bug Bounty Program

We currently do not have a bug bounty program, but we deeply appreciate all security research done on our project.

---

**Thank you for helping keep FastAPI Boilerplate Generator and our users safe! 🔒**
