
### Initial Setup
1. Navigate to the React frontend directory:
```bash
cd cheese-app-v2/src/frontend-react
```

2. Start the development container:
```bash
sh docker-shell.sh
```

### Dependencies Installation
First time only: Install the required Node packages
```bash
npm install
```

### Launch Development Server
1. Start the development server:
```bash
npm run dev
```

2. View your app at: http://localhost:3000

> Note: Make sure the API service container is running for full functionality
### Review App
- Go to Home page
- Go to Newsletters, Podcasts - Review functionality
- Go to Chat Assistant. Try LLM, LLM + CNN, RAG chats

### Review App Code
- Open folder `frontend-react/src`

### Data Services
- Data Service (`src/services/DataService.js`)
- Review Data Service methods that connects frontend to all backend APIs

### App Pages
- Open folder `frontend-react/src/app`
- Review the main app pages
  - Home (`src/app/page.jsx`)
  - Newsletters (`src/app/newsletters/page.jsx`)
  - Podcasts (`src/app/podcasts/page.jsx`)
  - Chat Assistant (`src/app/chat/page.jsx`)

### App Components
- Open folder `frontend-react/src/components`
- Review components of the app
  - Layout for common components such as Header, Footer
  - Chat for all the chat components


---
## Docker Cleanup

### Make sure we do not have any running containers and clear up an unused images
* Run `docker container ls`
* Stop any container that is running
* Run `docker system prune`
* Run `docker image ls`

### Testing
- Refer to this [file](testing.md) for instructions of how to manually run the unit tests for the Frontend functionality.
