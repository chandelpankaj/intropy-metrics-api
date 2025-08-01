# Project Decisions and Future Work

## What I Focused On

### 1. **Robust Data Loading & Deduplication**
- **Why?** Data integrity is the backbone of any metrics system. I made sure to:
  - Clean and validate data using Pandas for better quality control.
  - Prevent duplicate records with careful row-level deduplication.
  - Handle missing values and type conversions gracefully to avoid data corruption.

### 3. **Configuration Management**
- **Why?** Hardcoded values are risky and inflexible.
- **Implementation:**
  - Moved all sensitive and environment-specific settings to `.env` files.
  - Used `pydantic-settings` to load and validate configurations safely.

### 4. **Error Handling & Logging**
- **Why?** Good error handling saves hours of debugging.
- **Approach:**
  - Set up structured logging to make troubleshooting easier.
  - Created custom exceptions for different types of errors.
  - Made sure all errors follow a consistent format.

---

## Next Steps (If I Had More Time)

### 1. **Testing**
- Write thorough tests for all API endpoints using `pytest`.
- Add integration tests for database operations.
- Test end-to-end user flows to catch edge cases.

### 2. **Performance Tuning**
- Add indexes to speed up database queries.
- Implement caching for frequently accessed data.

### 3. **Security**
- Add JWT authentication for API access.
- Implement rate limiting to prevent abuse.

### 4. **Monitoring**
- Track API performance with Prometheus.

### 5. **Deployment**
- Automate testing and deployment with GitHub Actions.
- Use Docker for consistent environments.

