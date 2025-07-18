import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from config.config_loader import load_config

class ModelLoader:
    def __init__(self):
        """Initialize the model loader and load environment variables."""
        load_dotenv()
        self._validate_env()
        self.config = load_config(r"config\config.yaml")
        self.model_name = self.config['llm']['model_name']
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

    def _validate_env(self):
        """Validate that the required environment variables are set."""
        required_vars = ["OPENAI_API_KEY"]
        missing = [var for var in required_vars if not os.getenv(var)]
        if missing:
         raise EnvironmentError(f"Missing environment variables: {missing}")
        

    def load_model(self):
       return ChatOpenAI(
          model_name = self.model_name,
          openai_api_key = self.openai_api_key
       )

     

















#(self.config = load_config() : load_config() is a function defined in another file:from config.config_loader import load_config)
# self.model_name = self.config['llm']['model_name']
#This is not an argument passed from somewhere.This is extracting the value "gpt-4" from the loaded config.

#self.openai_api_key = os.getenv("OPENAI_API_KEY")
#This reads from your environment variables.It is not coming from config.yaml but from .env or system environment.

##these are not arguments passed into __init__() — they are references to configuration data, loaded from a file (config.yaml) and environment variables.