## For Chatbot
### Install environment
https://pytorch.org (Cài theo command trên trang chủ, chọn cấu hình tương thích)

### To download asr model (COMMAND)
cd chatbot/ASR/whisper/checkpoints_turbo
git clone https://huggingface.co/openai/whisper-large-v3-turbo

### To run demo (COMMAND)
cd chatbot
streamlit run gemini_role_with_syntax_extract_word.py