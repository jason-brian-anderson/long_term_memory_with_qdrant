# Chatbot Memory Extension

## Purpose
Enhance bot engagement by enabling memory retention across conversations.

## Functionality
Utilizes [Qdrant vector database](https://qdrant.tech/) within a Docker container to store/retrieve previous user interactions. Workflow:

1. **Vector Generation:** Converts new user input into vector embedding.
2. **Vector Storage:** Stores vector in vector database, in a bot-named collection.
3. **Collection Creation:** Creates the bot-named collection if non-existent.
4. **Memory Retrieval:** Retrieves related past comments using recent comment's embedding cosine similarities.

## Installation

- Relocate:
   - `docker-compose.yml`: Launches Ooba server and Qdrant database.
   - `.env`: Specify Docker data persistence locations.

- Optionally, adjust memory retrieval count via panel slider (max 10).

Initiate with:

```bash
docker-compose up
```

Build Ooba Docker image if needed:

```bash
docker-compose up --build
```

## Usage
Each bot maintains individual memory. Duplicate bot settings for a new version with a distinct name (e.g., _bot2_) to create a new collection.

## Future
Exploring event-driven coding and Gradio for potential enhancements like dropdown feature for memory sharing between bots and raw result display in panel. Could also add vdb configs into gui. Currently, view raw results by sending conversation to notebook.
