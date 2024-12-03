import { BASE_API_URL, uuid } from "./Common";
import axios from 'axios';

// Create an axios instance with base configuration
const api = axios.create({
    baseURL: BASE_API_URL
});
// Add request interceptor to include session ID in headers
api.interceptors.request.use((config) => {
    const sessionId = localStorage.getItem('userSessionId');
    if (sessionId) {
        config.headers['X-Session-ID'] = sessionId;
    }
    return config;
}, (error) => {
    return Promise.reject(error);
});

const DataService = {
    Init: function () {
        // Any application initialization logic comes here
    },
    GetUser: () => {
        if (typeof window !== "undefined") {
            const storedUser = localStorage.getItem('userId');
            if (storedUser) {
                // Remove JSON.parse since userId is stored as a plain string
                return storedUser;
            }
        }
        return null;
    },
    GetPantry: async function (user_id) {
        return await api.get(BASE_API_URL + "/pantry/" + user_id);
    },
    GetChats: async function (model, limit) {
        return await api.get(BASE_API_URL + "/" + model + "/chats?limit=" + limit);
    },
    GetChat: async function (model, chat_id) {
        return await api.get(BASE_API_URL + "/" + model + "/chats/" + chat_id);
    },
    StartChatWithLLM: async function (model, message) {
        return await api.post(BASE_API_URL + "/" + model + "/chats/", message);
    },

    ContinueChatWithLLM: async function (model, chat_id, message) {
        return await api.post(BASE_API_URL + "/" + model + "/chats/" + chat_id, message);
    },
    GetChatMessageImage: function (model, image_path) {
        return BASE_API_URL + "/" + model + "/" + image_path;
    },
    GetRecipeRecommendation: async function (body) {
        return await api.post(BASE_API_URL + "/recipes/get_recs", body);
    },
    GetUserHistoryRecs: async function (user_id) {
        return await api.get(BASE_API_URL + "/user/" + user_id + "/history/recommendations");
    },
    UpdateUserHistory: async function (user_id, data) {
        console.log("data is ", data)
        return await api.post(BASE_API_URL + "/user/" + user_id + "/history", data);
    },
    UploadRecipe: async function(data) {
        return await api.post(BASE_API_URL + "/recipes/upload-recipe", data);
    },
    GetUserPreferences: async function(userId) {
        return await api.get(`${BASE_API_URL}/recipes/user-preferences/${userId}`);
    },

    ToggleFavoriteRecipe: async function(userId, recipeName) {
        return await api.post(`${BASE_API_URL}/recipes/toggle-favorite`, {
            user_id: userId,
            recipe_title: recipeName
        });
    }
}

export default DataService;
