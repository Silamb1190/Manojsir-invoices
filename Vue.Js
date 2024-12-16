<template>
  <div id="app">
    <div class="upload-section">
      <h1>Document Parser</h1>
      <!-- File Upload -->
      <input type="file" @change="handleFileUpload" />
      <button v-if="uploadedFile" @click="submitFile" class="upload-btn">
        Parse Document
      </button>
    </div>

    <!-- Document Preview -->
    <div v-if="documentPreview" class="preview">
      <h3>Preview:</h3>
      <img :src="documentPreview" alt="Preview Image" class="preview-image" />
    </div>

    <!-- Display Parsed Data -->
    <div v-if="parsedData.length" class="parsed-data">
      <h2>Parsed Data</h2>
      <table>
        <thead>
          <tr>
            <th>Invoice Number</th>
            <th>Date</th>
            <th>Total Amount</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(data, index) in parsedData" :key="index">
            <td>{{ data.invoiceNumber }}</td>
            <td>{{ data.date }}</td>
            <td>{{ data.totalAmount }}</td>
          </tr>
        </tbody>
      </table>

      <!-- Export to CSV -->
      <vue-csv :data="parsedData" :fields="['invoiceNumber', 'date', 'totalAmount']" filename="parsed-invoice-data.csv">
        <button class="csv-btn">Export to CSV</button>
      </vue-csv>
    </div>

    <!-- Error Message -->
    <div v-if="errorMessage" class="error">
      <p>{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { VueCsv } from "vue-csv"; // Import vue-csv

export default {
  components: {
    VueCsv
  },
  data() {
    return {
      uploadedFile: null,
      documentPreview: null,
      parsedData: [],
      errorMessage: null
    };
  },
  methods: {
    // Handle file upload and set the document preview
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.uploadedFile = file;
        this.documentPreview = URL.createObjectURL(file);
      }
    },

    // Submit the uploaded file to the backend
    async submitFile() {
      const formData = new FormData();
      formData.append("file", this.uploadedFile);

      try {
        const response = await axios.post("http://localhost:5000/parse", formData, {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        });

        if (response.data.success) {
          this.parsedData = response.data.parsedData; // Example: invoiceNumber, date, totalAmount
        } else {
          this.errorMessage = "Failed to parse the document.";
        }
      } catch (error) {
        console.error("Error uploading file:", error);
        this.errorMessage = "An error occurred while processing the document.";
      }
    }
  }
};
</script>

<style scoped>
/* Basic styling */
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  margin-top: 50px;
}

.upload-section {
  margin-bottom: 20px;
}

.upload-btn,
.csv-btn {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  margin-top: 10px;
}

.upload-btn:hover,
.csv-btn:hover {
  background-color: #45a049;
}

.preview {
  margin-top: 20px;
}

.preview-image {
  max-width: 300px;
  margin: 0 auto;
}

.parsed-data {
  margin-top: 20px;
  text-align: left;
  max-width: 800px;
  margin: 20px auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

table th,
table td {
  padding: 8px;
  border: 1px solid #ddd;
}

.error {
  color: red;
  margin-top: 20px;
}
</style>
