# Python Synthesizer

A simple synthesizer application built in Python using Pygame and Sounddevice. It allows users to play different waveform sounds (sine, square, triangle) using their computer keyboard.

## Prerequisites

- Python (preferably version 3.6 or higher)
- pip (Python package installer)

## Setup

1. **Clone the Repository (Optional)**
   If you have the synthesizer script (`synth.py`) as a standalone, you can skip this step. Otherwise, clone the repository containing the script to your local machine using:

   `git clone https://github.com/camdenfritz/music-tch-synth.git`

2. **Create a Virtual Environment**
   Navigate to the project directory (where `synth.py` is located) and create a virtual environment. This will keep the dependencies required for the project separate from your global Python installation.

   ```
   cd path/to/synth
   python -m venv venv
   ```

- On Windows, you may need to use `python3` instead of `python`.

3. **Activate the Virtual Environment**

- On Windows:
  ```
  .\venv\Scripts\activate
  ```
- On macOS/Linux:
  ```
  source venv/bin/activate
  ```

4. **Install Required Packages**
   Install the necessary Python packages using pip:

   `pip install -r requirments.txt`

## Running the Synthesizer

1. **Start the Synthesizer**
   Run the synthesizer script using Python:

   `python synth.py`

2. **Play Notes**

- Use the keyboard keys 'Q' to 'P' to play square waves
- Keys 'A' to ';' for sine waves
- Keys 'Z' to '/' for triangle waves

3. **Adjust Frequency and Amplitude**

- Use the UP and DOWN arrow keys to increase or decrease the amplitude.
- Use the RIGHT and LEFT arrow keys to adjust the frequency.

4. **Visualizing Waveforms**

- The application window displays the waveform of the currently played note or notes.

5. **Exiting the Synthesizer**

- To exit the synthesizer, simply close the Pygame window or press `CTRL+C` in your command-line interface.
