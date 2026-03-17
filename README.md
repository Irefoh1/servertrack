# ⚡ ServerTrack — Serverless Infrastructure Inventory System

A cloud-native application for tracking and managing server infrastructure.
Built entirely with AWS serverless services. No servers to manage.

## Architecture

````
User → S3 (Static Site) → API Gateway → Lambda → DynamoDB
````

## AWS Services Used

- **DynamoDB** — NoSQL database for server inventory data
- **Lambda** — Serverless compute for CRUD API logic
- **API Gateway** — RESTful API endpoints
- **S3** — Static website hosting for the frontend
- **IAM** — Role-based access control for Lambda
- **CloudWatch** — Automatic logging for Lambda functions

## Features

- Full CRUD operations (Create, Read, Update, Delete)
- Dashboard with live server counts and status tracking
- Filter by environment (Production / Staging / Development)
- Serverless — scales automatically, pay only for what you use
- CORS-enabled API for frontend-backend communication

## API Endpoints

| Method | Endpoint              | Description        |
|--------|-----------------------|--------------------|
| GET    | /servers              | List all servers   |
| POST   | /servers              | Add a new server   |
| GET    | /servers/{server_id}  | Get a single server|
| PUT    | /servers/{server_id}  | Update a server    |
| DELETE | /servers/{server_id}  | Delete a server    |

## Deployment

Full deployment guide available in [DEPLOYMENT.md](DEPLOYMENT.md)

## Cleanup

To avoid charges, delete these resources when done:
1. S3 bucket (empty it first, then delete)
2. Lambda function
3. API Gateway
4. DynamoDB table
5. IAM role

## Author

Irefoh Anuwa
````

---

## What This Project Demonstrates

This project showcases your ability to work with serverless architecture design using managed AWS services with no servers to patch or maintain, DynamoDB table design with partition keys and on-demand capacity, Lambda function development with Python and the boto3 SDK handling full CRUD logic, API Gateway configuration with REST endpoints, path parameters, and CORS, S3 static website hosting as a cost-effective frontend delivery method, IAM security with least-privilege roles for Lambda, and CloudWatch integration for automatic logging and debugging. These are core skills that cloud engineering roles require.

---
