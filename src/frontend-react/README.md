
### Initial Setup
1. Navigate to the React frontend directory:
```bash
cd ac215_PrepPal/src/frontend-react
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

> Note: Make sure the API service container and the llm-rag container are running for full functionality
### Pages
- Home Page: About section and Log in/Sign up buttons (`src/app/page.jsx`)
- Pantry: text input to update pantry (`src/app/pantry/page.jsx`)
- Recipe Recommendation Page (`src/app/preppal/page.jsx`)
    - Filters for generating recommendations
    - Chat area for further customizations and questions about recommendations
- Log in Page (`src/app/login/page.jsx`)
- Sign up Page ((`src/app/signup/page.jsx`))

### Data Services
- Data Service (`src/services/DataService.js`)
- Connects frontend to all backend APIs using `axios`


---
## Docker Cleanup

### Make sure we do not have any running containers and clear up an unused images
* Run `docker container ls`
* Stop any container that is running
* Run `docker system prune`
* Run `docker image ls`

### Testing
- Refer to this [file](testing.md) for instructions of how to manually run the unit tests for the Frontend functionality.
