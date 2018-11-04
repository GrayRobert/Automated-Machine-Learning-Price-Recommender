import axios from 'axios'
const API_URL = 'http://localhost:8000'
export class APIService{

    constructor(){
        //empty constructor
    }

    // Get request to test API TODO: Write UNIT test
    //qs = query string to be passed in
    predictPrice(qs) {
        const url = `${API_URL}/predict/price?${qs}`;
        return axios.get(url).then(response => response.data);
    }

    trainModel(qs) {
        const url = `${API_URL}/train/model?${qs}`;
        return axios.get(url).then(response => response.data);
    }

    uploadFile(formData) {
        const url = `${API_URL}/upload/training_data.csv`;

        return axios.put(url, formData,
            )
        // get data
        .then(response => response.data)
    }

}



