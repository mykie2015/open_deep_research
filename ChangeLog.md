# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- **configuration.py:**
  - Modified the `Configuration` class to explicitly load API keys from environment variables.
  - Added validation to ensure the `OPENAI_API_KEY` is provided.
- **utils.py:**
  - Updated `perplexity_search` to retrieve the API key using `Configuration.from_runnable_config()`.
  - Added `get_config_value` helper function to handle configurations for different providers.
- **graph.py:**
  - Updated `generate_report_plan` to use the `get_config_value` helper for model initialization, ensuring correct API keys and base URLs are used.

## [0.1.0] - 2025-02-22

- Initial version of the Open Deep Research project.