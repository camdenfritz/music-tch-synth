import pygame
import numpy as np
import sounddevice as sd

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Synthesizer")

note_frequencies = {
    pygame.K_a: [261.63, "sine"],  # C4
    pygame.K_s: [293.66, "sine"],  # D4
    pygame.K_d: [329.63, "sine"],  # E4
    pygame.K_f: [349.23, "sine"],  # F4
    pygame.K_g: [392.00, "sine"],  # G4
    pygame.K_h: [440.00, "sine"],  # A4
    pygame.K_j: [493.88, "sine"],  # B4
    pygame.K_k: [523.25, "sine"],  # C5
    pygame.K_l: [587.33, "sine"],  # D5
    pygame.K_SEMICOLON: [659.25, "sine"],  # E5
    pygame.K_q: [261.63, "square"],  # C4
    pygame.K_w: [293.66, "square"],  # D4
    pygame.K_e: [329.63, "square"],  # E4
    pygame.K_r: [349.23, "square"],  # F4
    pygame.K_t: [392.00, "square"],  # G4
    pygame.K_y: [440.00, "square"],  # A4
    pygame.K_u: [493.88, "square"],  # B4
    pygame.K_i: [523.25, "square"],  # C5
    pygame.K_o: [587.33, "square"],  # D5
    pygame.K_p: [659.25, "square"],  # E5
    pygame.K_z: [261.63, "triangle"],  # C4
    pygame.K_x: [293.66, "triangle"],  # D4
    pygame.K_c: [329.63, "triangle"],  # E4
    pygame.K_v: [349.23, "triangle"],  # F4
    pygame.K_b: [392.00, "triangle"],  # G4
    pygame.K_n: [440.00, "triangle"],  # A4
    pygame.K_m: [493.88, "triangle"],  # B4
    pygame.K_COMMA: [523.25, "triangle"],  # C5
    pygame.K_PERIOD: [587.33, "triangle"],  # D5
    pygame.K_SLASH: [659.25, "triangle"],  # E5
}

global_amplitude = 0.5
global_freq_adjustment = 1.0
global_effects_freq_adjustment = global_freq_adjustment

# Synthesizer parameters
sample_rate = 44100
stream = sd.OutputStream(samplerate=sample_rate, channels=1, blocksize=512)
stream.start()

# Active notes and wave type
active_notes = {}
current_wave_type = "sine"


def draw_waveform(screen, wave, color=(255, 255, 255)):
    wave_height = screen.get_height()
    wave_width = screen.get_width()
    max_amplitude = np.max(np.abs(wave)) or 1
    normalized_wave = (wave / max_amplitude) * (wave_height / 2)  # Normalize and scale
    mid_height = wave_height // 2

    for i in range(len(wave) - 1):
        x1 = i * wave_width / len(wave)
        y1 = mid_height + normalized_wave[i]
        x2 = (i + 1) * wave_width / len(wave)
        y2 = mid_height + normalized_wave[i + 1]
        pygame.draw.line(screen, color, (x1, y1), (x2, y2))


def generate_wave(freq, wave_type="sine", amplitude=0.5, max_length=0):
    adjusted_freq = freq * global_freq_adjustment
    periods = 5
    duration = periods / adjusted_freq
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    if wave_type == "sine":
        wave = amplitude * np.sin(2 * np.pi * adjusted_freq * t)
    elif wave_type == "square":
        wave = amplitude * np.sign(np.sin(2 * np.pi * adjusted_freq * t))
    elif wave_type == "triangle":
        wave = (
            amplitude
            * 2
            * np.abs(2 * (t * adjusted_freq - np.floor(0.5 + t * adjusted_freq)))
            - 1
        )

    # Pad wave if shorter than the max_length
    if len(wave) < max_length:
        wave = np.pad(wave, (0, max_length - len(wave)), "constant")

    return wave


# Function to mix waves
def mix_waves(waves):
    if waves:
        mixed_wave = np.sum(waves, axis=0)
        max_amp = np.max(np.abs(mixed_wave))
        # Normalized and pervents clipping
        if max_amp > 1:
            mixed_wave /= max_amp
        return mixed_wave
    else:
        min_freq = min(f[0] for f in note_frequencies.values())
        return np.zeros(int(sample_rate * (1 / min_freq)))


running = True
active_notes = {}

is_long_increase_active = False
long_increase_rate = 1.01  # Rate of frequency increase

is_wobble_active = False
wobble_rate = 0.01  # Speed of wobble
wobble_amount = 1.05  # Range of wobble
wobble_direction = 1  # Wobble direction

while running:
    # Update max_length if there are active notes
    max_length = 0
    if active_notes:
        max_length = max(
            int(sample_rate * (5 / min(freq[0] for freq in active_notes.values()))), 1
        )

    # Generate and mix waves if there are active notes
    screen.fill((0, 0, 0))

    if is_long_increase_active:
        global_freq_adjustment *= long_increase_rate
        if (
            global_freq_adjustment - global_effects_freq_adjustment > 2
        ):  # Reset if it gets too high
            global_freq_adjustment = global_effects_freq_adjustment

    # Apply wobble effect
    if is_wobble_active:
        global_freq_adjustment *= 1 + wobble_direction * wobble_rate
        if (
            global_freq_adjustment > wobble_amount
            or global_freq_adjustment < 1 / wobble_amount
        ):
            wobble_direction *= -1

    if max_length > 0 and active_notes:
        waves = [
            generate_wave(freq[0], freq[1], global_amplitude, max_length)
            for freq in active_notes.values()
        ]
        mixed_wave = mix_waves(waves)
        stream.write(mixed_wave.astype(np.float32))
        draw_waveform(screen, mixed_wave)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in note_frequencies:
                active_notes[event.key] = note_frequencies[event.key]
            elif event.key == pygame.K_UP:
                global_amplitude = min(global_amplitude + 0.1, 1.0)
            elif event.key == pygame.K_DOWN:
                global_amplitude = max(global_amplitude - 0.1, 0.0)
            elif event.key == pygame.K_RIGHT:
                global_freq_adjustment *= 1.05
            elif event.key == pygame.K_LEFT:
                global_freq_adjustment /= 1.05
            elif event.key == pygame.K_1:
                is_long_increase_active = not is_long_increase_active

            # Toggle wobble effect
            elif event.key == pygame.K_2:
                is_wobble_active = not is_wobble_active

            elif event.key == pygame.K_0:
                global_freq_adjustment = 1.0  # Reset frequency

        elif event.type == pygame.KEYUP:
            if event.key in active_notes:
                del active_notes[event.key]

    pygame.display.flip()


stream.stop()
pygame.quit()
