## Codeclimate status:
<a href="https://codeclimate.com/github/MisterFlicker/python-project-83/maintainability"><img src="https://api.codeclimate.com/v1/badges/46d6d0a63eea8c47fd64/maintainability" /></a>

## Description

Page Analyzer is a site that analyzes specified pages for SEO suitability similar to PageSpeed Insights.

## How to use

git@github.com:MisterFlicker/python-project-83.git

To install use: make install

To build use: make build

To package install use: make package-install

You need to make three tables in database - to do this, execute the code for creating tables specified in the root file **database.sql**.

Also you need to create an .env file in the root of the project, and write your environment variables there.  
```
# DATABASE_URL format: {provider}://{user}:{password}@{host}:{port}/{db}
# below you can see an example
DATABASE_URL = postgresql://someuser:somepassword@localhost:5432/database
SECRET_KEY = 'any character set for secret key'
```

After installing dependencies (root file **Makefile** can help with this) run command:  
`make run`

Deployed app: https://page-analyzer-00jp.onrender.com/
