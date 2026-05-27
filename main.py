from scraper.main import main

RUN_DEMO = False
MONGO_URI = "mongodb://localhost:27017/"

if __name__ == "__main__":
    main(mongo_uri=MONGO_URI, demo=RUN_DEMO)