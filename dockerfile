# python version
FROM python:3.12.4-slim

# Set the working directory 
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

# expose port
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "--server.port=8501", "app.py"]