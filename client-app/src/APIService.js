import axios from 'axios'
const API_URL = 'http://localhost:8000/api/v1'
export class APIService{

    constructor(){
        //empty constructor
    }

    // Get request to test API TODO: Write UNIT test
    //qs = query string to be passed in
    predictPrice(qs) {
        const url = `${API_URL}/model/predict?${qs}`;

        return axios.get(url)
        // get data
        .then(response => response.data);
    }

    trainModel(formData) {
        const url = `${API_URL}/model/train`;

        return axios.post(url, formData)
        // get data
        .then(response => response.data);
    }

    uploadFile(formData) {
        const url = `${API_URL}/file/upload/training_data.csv`;

        return axios.put(url, formData)
        // get data
        .then(response => response.data)
    }

    getModelTrainingHistory() {
        const url = `${API_URL}/model/traininghistory`;

        return axios.get(url)
        // get data
        .then(response => response.data);
    }

    deleteModel(modelID) {
        const url = `${API_URL}/model/delete/${modelID}`;

        return axios.delete(url)
        // get data
        .then(response => response.data);
    }

    loginUser(formData) {
        const url = `${API_URL}/rest-auth/login/`;

        return axios.post(url, formData)
        // get data
        .then(response => response.data)
        .catch(error => error.response.data)
    }

    logoutUser(formData) {
        const url = `${API_URL}/rest-auth/logout/`;

        return axios.post(url, formData)
        // get data
        .then(response => response.data)
        .catch(error => error.response.data)
    }

    resetPassword(formData) {
        const url = `${API_URL}/rest-auth/password/reset/`;

        return axios.post(url, formData)
        // get data
        .then(response => response.data)
        .catch(error => error.response.data)
    }

}



