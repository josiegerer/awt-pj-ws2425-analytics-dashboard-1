# vue-dashboard

## Navigate to the frontend
cd frontend

## Project setup & install node_modules
```
npm install
npm install @vue/cli-service 
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).






Token Generation and Encoding: The token is generated and encoded on the server side when the user logs in. The server includes the user's role and other relevant information in the token.

Token Storage: The client receives the token and stores it in local storage or cookies.

Token Decoding: In the fetchUserName method, the token is fetched from local storage and decoded using the jwt-decode library. The user's role and other information are extracted from the decoded token.

Role-Based Redirection: Based on the extracted role, the user is redirected to the appropriate dashboard using the redirectBasedOnRole method.
