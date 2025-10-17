# config.py

# This file holds configuration variables that are used across the project.
# Centralizing them here makes it easy to change key values without
# having to search through multiple files.

# MAX_CHARACTERS: Defines the maximum number of characters to read from a file.
# This is a safeguard to prevent the program from loading excessively large files
# into memory, which could cause performance issues or crashes.
MAX_CHARACTERS = 10000

# GEMINI_MODEL: Specifies the name of the Gemini model to be used by the agent.
# Centralizing it here allows for easy updates or switching between models.
GEMINI_MODEL = 'gemini-1.5-pro-latest'