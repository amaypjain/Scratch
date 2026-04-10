# Scratch
A highly modular, production-ready simulation of a **Context-Aware Nutritional Intelligence** platform built for a hackathon. It utilizes continuous passive data collection and Just-In-Time Adaptive Interventions (JITAI) based on the BJ Fogg Behavior Model to promote healthier eating habits.

## Architecture

This project strictly follows clean architecture via the separation of concerns:

- `src/models.py`: Data classes handling strict input typing and dynamic schemas for Profiles and Telemetry.
- `src/context_engine.py`: Data ingestion and analysis. Converts physiological/environmental markers into a "Vulnerability Score".
- `src/jitai_engine.py`: Dispatches psychological nudges based on context evaluation and predefined profile criteria.
- `tests/`: High-coverage unit tests leveraging `unittest`.

### Extensions for Production
Though this code acts as a conceptual simulation to demonstrate the platform logic locally, it is organized to quickly connect to external services:
- **Google Maps API**: Modify `src/context_engine.py` bounds checking to dynamically query real-life POI via coordinate lookups.
- **Firebase/Supabase**: Add integration in `src/models.py` or a dedicated DB layer to persist real users and continuous telemetry event buses.

## Setup Requirements

The project uses pure Python capabilities to stay incredibly lightweight. No external pip libraries are required to run the core simulation or test suite!

Requires **Python 3.7+**.

## Usage

Run the simulated ingestion pipeline and inference engine:
```bash
python main.py
```

### Running Tests
To verify all internal calculations, run the test suite:
```bash
python -m unittest discover -s tests
```

