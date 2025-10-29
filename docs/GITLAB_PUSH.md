# GitLab push instructions
# Replace GITLAB_URL and REPO_PATH with your values.

git init
git add .
git commit -m "Initial commit: angi_data_pipeline"
# create a new project on GitLab via UI or API, then:
git remote add origin git@gitlab.com:<your-username>/angi_data_pipeline.git
git branch -M main
git push -u origin main

# If using GitLab API to create project (curl example):
# curl --header "PRIVATE-TOKEN: <your_token>" -X POST "https://gitlab.com/api/v4/projects?name=angi_data_pipeline"
