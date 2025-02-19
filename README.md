# 8drtna Streamlit

A web application developed using Streamlit and Supabase to host the 8drtna model for audio transcription in both Algerian Darija and Kabyle dialects.

## Model Details

The 8drtna model was created by fine-tuning OpenAI's Whisper model to support transcription of Algerian Darija and Kabyle dialects. This fine-tuning process involved training the model on a curated dataset of audio recordings in these dialects, enhancing its accuracy and performance for these specific languages.

## Features

- **Real-time Audio Transcription**: Upload audio files and receive instant transcriptions in Algerian Darija and Kabyle.
- **User Authentication**: Secure login and registration powered by Supabase.
- **Dashboard**: Visualize and manage your transcription history.

## Installation

1. **Clone the Repository**:

     ```bash
    git clone https://github.com/marouaneoa/8drtna-Streamlit.git
    cd 8drtna-Streamlit
    ```  

2. **Install Dependencies**:

     ```bash
    pip install -r requirements.txt
    ```  

3. **Set Up Environment Variables**:

    Create a `.env` file in the root directory with the following content:

     ```
    SUPABASE_URL=your_supabase_url
    SUPABASE_KEY=your_supabase_key
    ```  

    Replace `your_supabase_url` and `your_supabase_key` with your actual Supabase project credentials.

## Usage

To start the application, run:


```bash
streamlit run app.py
```


This will launch the app in your default web browser.

## Project Structure


```
8drtna-Streamlit/
├── app.py          # Main application script
├── settings.py     # Configuration settings
├── pages/          # Directory containing sub-pages
├── requirements.txt# List of dependencies
└── README.md       # This readme file
```


## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.
