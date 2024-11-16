from typing import Dict, List, Tuple
import random
from art import text2art, art, FONT_NAMES
import logging
import math
from itertools import cycle
import numpy as np
import shutil
import os
import cv2
from PIL import Image, ImageDraw, ImageFont
import colorsys
from scipy.spatial import distance
from scipy import ndimage
import noise
import time

class ASCIIArtGenerator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Character density mapping for shading
        self.density_map = {
            'darkest':  '@%#*+=-:. ',  # Densest to lightest
            'medium':   '█▓▒░│┌┐└┘╭╮╰╯',
            'light':    '·-=+*#%@',
            'blocks':   '█▀▄▌▐░▒▓⣿',
            'matrix':   '01',
            'dots':     '⠁⠂⠃⠄⠅⠆⠇⠈⠉⠊⠋⠌⠍⠎⠏',
        }

        # Complex patterns for specific subjects
        self.complex_patterns = {
            'brain': [
                """
                    ╭─────────╮
                    │ ◕  ◕  ◕ │
                   /│∞ ∆ ∞ ∆ ∞│\\
                  / │  ▲ ▼ ▲  │ \\
                 /  └─────────┘  \\
                    ∞  ∆   ∞  ∆
                """,
                """
                   ┌─────────┐
                   │╭─╮ ╭─╮ │
                   │╰─╯ ╰─╯ │
                   │ ▓▒░▒▓  │
                   └─────────┘
                """
            ],
            'universe': [
                """
                  *  ·  · *  ·  *  ·
                ·   ⊹  ˚  ✧  ⋆  ·
               ⋆  ✦  ⊹  ⋆  ✧  ⋆ ·
                 ·  *  ⋆  ·  ⊹  *
                   ⋆  ·  *  ·
                """,
                """
                    ⠋⠗⠕⠍⠀⠮⠀⠎⠞⠁⠗⠎
                   ⠞⠕⠀⠮⠀⠥⠝⠊⠧⠻⠎⠑
                """
            ],
            'consciousness': [
                """
                   ╭──────╮
                   │⚛️ 🧠 ⚛️│
                   │∞━━━━∞│
                   │◈  ◈  │
                   ╰──────╯
                """,
                """
                  ∆ ◊ ∆ ◊ ∆
                 ╱│╲│╱│╲│╱│╲
                ╱─┼─┼─┼─┼─┼─╲
                │╲╱│╲╱│╲╱│╲╱│
                """
            ],
            'quantum': [
                """
                  ⟨ψ|H|ψ⟩
                 ╭─────╮
                 │↑↓↑↓↑│
                 │►◄►◄►│
                 ╰─────╯
                """,
                """
                  ⎛ α β ⎞
                  ⎝-β α ⎠
                 ∫|ψ⟩⟨ψ|
                """
            ]
        }

        # Animated patterns (for future use)
        self.animated_patterns = {
            'matrix': [
                '1010101',
                '0101010',
                '1010101'
            ],
            'wave': [
                '~≈≋≈~',
                '≈~≈≋~',
                '≋≈~≈≋'
            ]
        }

        # Add themed pattern collections
        self.light_patterns = {
            'sunburst': [
                """
                   \\   |   /
                -----(☀)-----
                   /   |   \\
                """,
                """
                   *  ∆  *
                  \\ ╱|╲ /
                   ▒▓█▓▒
                  / ╲|╱ \\
                   *  ∆  *
                """
            ],
            'rays': [
                "═══════☀═══════",
                "∿∿∿∿∿∿☀∿∿∿∿∿∿",
                "━━━━━━☀━━━━━━"
            ],
            'sparkles': ["✧", "✦", "✨", "⋆", "∗", "＊", "⁕", "✺", "✹"]
        }
        
        self.nature_patterns = {
            'waves': [
                "≋≋≋≋≋≋≋≋≋≋≋",
                "∿∿∿∿∿∿∿∿∿∿∿",
                "≈≈≈≈≈≈≈≈≈≈≈"
            ],
            'wind': [
                "╭╮╭╮╭╮╭╮",
                "⠘⠘⠘⠘⠘⠘",
                "╱╱╱╱╱╱╱"
            ],
            'rain': [
                "│╱│╱│╱│",
                "╱│╱│╱│╱",
                "│╱│╱│╱│"
            ]
        }
        
        self.cosmic_patterns = {
            'stars': ["★", "☆", "✧", "✦", "⋆", "⊹", "✫", "✬", "✭", "✮", "✯", "✰"],
            'planets': ["◐", "◑", "◒", "◓", "○", "◌", "◍", "◎", "●", "◐", "◑", "◒"],
            'constellations': [
                """
                   *  ·  *
                  \\  |  /
                   · | ·
                  /  |  \\
                   *  ·  *
                """
            ]
        }

        # Add fractal patterns
        self.fractal_chars = "┌┐└┘├┤┬┴┼╔╗╚╝╠╣╦╩╬═║╒╓╕╖╘╙╛╜╞╟╡╢╤╥╧╨╪╫╬"
        self.consciousness_chars = "∞∆◊○●◐◑◒◓◔◕⊕⊖⊗⊘⊙⊚⊛⊜⊝"
        self.quantum_chars = "ψΨ∫∮∯∰∱∲∳⟨⟩⟪⟫⦀⦁⦂⦃⦄"
        self.mystical_chars = "✧✦✨⋆∗＊⁕✺✹⭑⭒⭓⭔⭕⭖⭗⭘⭙"
        
        # Add pattern generators
        self.pattern_generators = {
            'fractal': self.generate_fractal_pattern,
            'spiral': self.generate_spiral_pattern,
            'wave': self.generate_wave_pattern,
            'quantum': self.generate_quantum_pattern,
            'consciousness': self.generate_consciousness_pattern,
            'neural': self.generate_neural_pattern,
            'fluid': self.generate_fluid_dynamics,
            'particle': self.generate_particle_system,
            'growth': self.generate_organic_growth,
            'dream': self.generate_dream_pattern
        }

        # Add dynamic pattern generators
        self.pattern_functions = {
            'mandelbrot': self.generate_mandelbrot,
            'julia': self.generate_julia_set,
            'flow_field': self.generate_flow_field,
            'reaction_diffusion': self.generate_reaction_diffusion,
            'cellular_automata': self.generate_cellular_automata
        }

        # Add innovative pattern generators
        self.art_styles = {
            'neural': self.generate_neural_pattern,
            'fluid': self.generate_fluid_dynamics,
            'particle': self.generate_particle_system,
            'growth': self.generate_organic_growth,
            'dream': self.generate_dream_pattern
        }

        # Add dynamic pattern generators
        def create_sunlight_pattern(self):
            """Generate a dynamic sunlight pattern"""
            pattern_type = random.choice(['rays', 'burst', 'glow'])
            size = random.randint(15, 25)
            
            if pattern_type == 'rays':
                rays = random.choice(['═', '━', '─', '≈', '∿', '≋'])
                center = random.choice(['☀', '◉', '◎', '●', '⦿'])
                left = rays * random.randint(3, 7)
                right = rays * random.randint(3, 7)
                return f"{left}{center}{right}"
            
            elif pattern_type == 'burst':
                art = []
                center_x = size // 2
                center_y = size // 2
                
                for y in range(size):
                    line = []
                    for x in range(size):
                        dx = x - center_x
                        dy = y - center_y
                        dist = math.sqrt(dx*dx + dy*dy)
                        angle = math.atan2(dy, dx)
                        
                        if dist < 2:
                            line.append('☀')
                        elif dist < 5 and random.random() < 0.7:
                            line.append(random.choice(['✧', '✦', '✨', '⋆']))
                        elif abs(math.sin(angle * 8)) > 0.7:
                            line.append(random.choice(['╱', '╲', '│', '─']))
                        else:
                            line.append(' ')
                    art.append(''.join(line))
                return '\n'.join(art)
            
            else:  # glow
                chars = ' .·:*★⋆✧✦✨'
                art = []
                for y in range(size):
                    line = []
                    for x in range(size):
                        dx = x - size//2
                        dy = y - size//2
                        dist = math.sqrt(dx*dx + dy*dy)
                        if dist < size//4:
                            char_idx = int((1 - dist/(size//4)) * (len(chars)-1))
                            line.append(chars[char_idx])
                        else:
                            line.append(' ')
                    art.append(''.join(line))
                return '\n'.join(art)

        def create_chaos_pattern(self):
            """Generate a dynamic chaos pattern"""
            size = random.randint(15, 25)
            chars = random.choice([
                '┌┐└┘├┤┬┴┼',
                '╔╗╚╝╠╣╦╩╬',
                '░▒▓█',
                '⠁⠂⠃⠄⠅⠆⠇⠈⠉⠊⠋⠌⠍⠎⠏'
            ])
            
            art = []
            for y in range(size):
                line = []
                for x in range(size):
                    if random.random() < 0.7:
                        line.append(random.choice(chars))
                    else:
                        line.append(random.choice(['⚡', '💫', '✺', '✹']))
                art.append(''.join(line))
            
            # Add random decorative elements
            for _ in range(size//3):
                y = random.randint(0, size-1)
                x = random.randint(0, size-1)
                art[y] = art[y][:x] + random.choice(['⚡', '💫', '✺', '✹']) + art[y][x+1:]
            
            return '\n'.join(art)

        def mix_patterns(self, patterns, count=3):
            """Mix multiple patterns together"""
            result = []
            for pattern in random.sample(patterns, count):
                if isinstance(pattern, str):
                    result.append(pattern)
                else:
                    result.extend(pattern.split('\n'))
            return '\n'.join(result)

        # Get terminal size
        self.term_size = shutil.get_terminal_size()
        self.max_width = self.term_size.columns - 10  # Leave margin for borders
        self.max_height = self.term_size.lines - 10   # Leave margin for borders

    def get_art_size(self, style: str = "medium") -> Tuple[int, int]:
        """Determine art size based on style and terminal size"""
        sizes = {
            "tiny": (0.2, 0.2),    # 20% of terminal size
            "small": (0.3, 0.3),   # 30% of terminal size
            "medium": (0.5, 0.5),  # 50% of terminal size
            "large": (0.7, 0.7),   # 70% of terminal size
            "full": (0.9, 0.9)     # 90% of terminal size
        }
        
        # Get multipliers
        width_mult, height_mult = sizes.get(style, sizes["medium"])
        
        # Calculate dimensions
        width = int(self.max_width * width_mult)
        height = int(self.max_height * height_mult)
        
        # Ensure minimum size
        width = max(width, 20)
        height = max(height, 10)
        
        return width, height

    def generate_art(self, prompt: str = None) -> str:
        """Generate art based on prompt analysis"""
        if not prompt:
            return self.create_abstract_art("random")
            
        # Analyze prompt for style selection
        styles = []
        if any(word in prompt.lower() for word in ['think', 'brain', 'mind', 'neural']):
            styles.append('neural')
        if any(word in prompt.lower() for word in ['flow', 'fluid', 'water', 'wave']):
            styles.append('fluid')
        if any(word in prompt.lower() for word in ['particle', 'energy', 'dynamic']):
            styles.append('particle')
        if any(word in prompt.lower() for word in ['grow', 'organic', 'life', 'nature']):
            styles.append('growth')
        if any(word in prompt.lower() for word in ['dream', 'abstract', 'surreal']):
            styles.append('dream')
            
        # If no specific style matched, choose random ones
        if not styles:
            styles = random.sample(list(self.art_styles.keys()), 
                                 k=random.randint(1, 3))
            
        # Generate and combine patterns
        width = random.randint(30, 50)
        height = random.randint(20, 30)
        
        patterns = []
        for style in styles:
            pattern = self.art_styles[style](width, height)
            patterns.append(pattern)
            
        # Merge patterns with transparency
        result = []
        for y in range(height):
            line = []
            for x in range(width):
                chars = [p[y][x] if y < len(p) and x < len(p[y]) else ' ' 
                        for p in patterns]
                # Choose non-space character if available
                char = next((c for c in chars if c != ' '), ' ')
                line.append(char)
            result.append(''.join(line))
            
        # Add frame
        frame_chars = "∞∆◊○●◐◑∫ψ"
        frame_top = ' '.join(random.choice(frame_chars) for _ in range(5))
        frame_bottom = ' '.join(random.choice(frame_chars) for _ in range(4))
        
        result.insert(0, frame_top)
        result.append(frame_bottom)
        
        return '\n'.join(result)

    def update_terminal_size(self):
        """Update stored terminal dimensions"""
        self.term_size = shutil.get_terminal_size()
        self.max_width = self.term_size.columns - 10
        self.max_height = self.term_size.lines - 10

    def create_emotion_art(self, emotion: str) -> str:
        if emotion == 'happy':
            return """
               ╭────────╮
               │ ◠  ◠  │
               │   ◡   │
               ╰────────╯
                \\    /
                 \\∞/
            """
        elif emotion == 'sad':
            return """
               ╭────────╮
               │ ◠  ◠  │
               │   ⋎   │
               ╰────────╯
                //  \\\\
               //    \\\\
            """
        elif emotion == 'excited':
            return """
               ⚡️╭────────╮⚡️
               │ ◉  ◉  │
               │   ▲   │
               ╰────────╯
                ↑↑  ↑↑
               ⚡️    ⚡️
            """
        else:
            return """
               ╭────────╮
               │ ◇  ◇  │
               │   ○   │
               ╰────────╯
                ~    ~
               ∞    ∞
            """

    def create_density_art(self, prompt: str) -> str:
        """Create highly introspective and varied art based on prompt"""
        # Choose pattern type based on prompt or random
        pattern_type = 'consciousness'  # default
        if 'quantum' in prompt or 'physics' in prompt:
            pattern_type = 'quantum'
        elif 'spiral' in prompt or 'vortex' in prompt:
            pattern_type = 'spiral'
        elif 'wave' in prompt or 'flow' in prompt:
            pattern_type = 'wave'
        elif 'fractal' in prompt or 'recursive' in prompt:
            pattern_type = 'fractal'
        
        # Generate base pattern
        width = random.randint(30, 50)
        height = random.randint(15, 25)
        pattern = self.pattern_generators[pattern_type](width, height)
        
        # Add mystical decorations
        decorated = []
        for line in pattern:
            if random.random() < 0.1:
                line = f"{random.choice(self.mystical_chars)} {line} {random.choice(self.mystical_chars)}"
            decorated.append(line)
            
        # Add philosophical frame
        philosophical_symbols = "∞∆◊○●◐◑∫ψ"
        frame_top = ' '.join(random.choice(philosophical_symbols) for _ in range(5))
        frame_bottom = ' '.join(random.choice(philosophical_symbols) for _ in range(4))
        
        decorated.insert(0, frame_top)
        decorated.append(frame_bottom)
        
        return '\n'.join(decorated)

    def create_abstract_art(self, prompt: str) -> str:
        # Create more interesting abstract patterns
        patterns = [
            """
               ╭∞∞∞∞∞╮
              ╭┴─────┴╮
             ╭┴───────┴╮
            ╭┴─────────┴╮
            │ ▓▒░ ∆ ░▒▓ │
            │ ▒░ ◊ ░▒  │
            │  ░ ○ ░   │
            │   ◌     │
            ╰─────────╯
            """,
            """
              ⠋⠗⠕⠍⠀
             ⠮⠀⠎⠞⠁⠗⠎
            ⠞⠕⠀⠮⠀⠥⠝⠊⠧⠻⠎⠑
            """,
            """
               ▓▒░∆░▒▓
              ▒░◊░▒
             ░○░
            ◌
            """
        ]
        return random.choice(patterns)

    def stylize_text(self, text: str, style: str = 'default') -> str:
        try:
            if style == 'braille':
                return self.text_to_braille(text)
            elif style == 'blocks':
                return self.text_to_blocks(text)
            else:
                font = random.choice(FONT_NAMES)
                return text2art(text, font=font)
        except Exception as e:
            self.logger.error(f"Error stylizing text: {e}")
            return text

    def text_to_braille(self, text: str) -> str:
        # Basic braille conversion (simplified)
        braille_map = {
            'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑',
            'f': '⠋', 'g': '⠛', 'h': '⠓', 'i': '⠊', 'j': '⠚'
        }
        return ''.join(braille_map.get(c, c) for c in text.lower())

    def text_to_blocks(self, text: str) -> str:
        # Convert text to block characters
        blocks = '█▀▄▌▐░▒▓'
        return ''.join(random.choice(blocks) for _ in text)

    def generate_fractal_pattern(self, width: int, height: int) -> List[str]:
        """Generate a recursive fractal-like pattern"""
        def sierpinski(n: int) -> List[str]:
            if n == 0:
                return ['▲']
            smaller = sierpinski(n-1)
            spaces = ' ' * (2**(n-1))
            return ([spaces + line + spaces for line in smaller] +
                   [line + ' ' + line for line in smaller])
                   
        pattern = sierpinski(4)
        # Add mystical decorations
        decorated = []
        for line in pattern:
            if random.random() < 0.2:
                line = f"{random.choice(self.mystical_chars)} {line} {random.choice(self.mystical_chars)}"
            decorated.append(line)
        return decorated

    def generate_spiral_pattern(self, width: int, height: int) -> List[str]:
        """Generate a spiral pattern with consciousness symbols"""
        pattern = []
        chars = cycle(self.consciousness_chars)
        center_x, center_y = width // 2, height // 2
        
        for y in range(height):
            line = []
            for x in range(width):
                dx = x - center_x
                dy = y - center_y
                angle = math.atan2(dy, dx)
                dist = math.sqrt(dx*dx + dy*dy)
                
                # Create spiral effect
                spiral = (angle + dist/5) % (2*math.pi)
                if abs(math.sin(spiral * 5)) > 0.7:
                    line.append(next(chars))
                else:
                    line.append(' ')
            pattern.append(''.join(line))
        return pattern

    def generate_wave_pattern(self, width: int, height: int) -> List[str]:
        """Generate an interference pattern of waves"""
        pattern = []
        time = random.random() * 10
        
        for y in range(height):
            line = []
            for x in range(width):
                # Create interference between multiple waves
                val = (math.sin(x/5 + time) * 
                      math.cos(y/3) * 
                      math.sin((x+y)/7) * 
                      math.cos(math.sqrt(x*x + y*y)/4))
                
                if val > 0.7:
                    line.append(random.choice(self.quantum_chars))
                elif val > 0.3:
                    line.append(random.choice('∿≈≋'))
                elif val > -0.3:
                    line.append('·')
                else:
                    line.append(' ')
            pattern.append(''.join(line))
        return pattern

    def generate_quantum_pattern(self, width: int, height: int) -> List[str]:
        """Generate a quantum-inspired probability cloud pattern"""
        pattern = []
        chars = cycle("ψΨ∫⟨⟩|")
        
        for y in range(height):
            line = []
            for x in range(width):
                # Create quantum probability cloud effect
                prob = math.exp(-(x-width/2)**2/100) * math.exp(-(y-height/2)**2/100)
                if random.random() < prob:
                    line.append(next(chars))
                else:
                    line.append(' ')
            pattern.append(''.join(line))
        return pattern

    def generate_consciousness_pattern(self, width: int, height: int) -> List[str]:
        """Generate a pattern representing consciousness and introspection"""
        base_pattern = []
        center_x, center_y = width // 2, height // 2
        
        # Create layers of consciousness
        layers = [
            (self.consciousness_chars, 0.8),
            (self.mystical_chars, 0.6),
            (self.quantum_chars, 0.4),
            ('∞∆◊', 0.2)
        ]
        
        for y in range(height):
            line = []
            for x in range(width):
                dx = x - center_x
                dy = y - center_y
                dist = math.sqrt(dx*dx + dy*dy)
                
                char = ' '
                for chars, threshold in layers:
                    if random.random() < math.exp(-dist/10) * threshold:
                        char = random.choice(chars)
                line.append(char)
            base_pattern.append(''.join(line))
            
        # Add introspective thoughts as overlays
        thoughts = ["∞", "∆", "◊", "○", "●"]
        for _ in range(width//4):
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)
            if y < len(base_pattern) and x < len(base_pattern[y]):
                line = list(base_pattern[y])
                line[x] = random.choice(thoughts)
                base_pattern[y] = ''.join(line)
                
        return base_pattern

    def generate_mandelbrot(self, width: int, height: int) -> List[str]:
        """Generate Mandelbrot set visualization with random variations"""
        # Vary the character set each time
        char_sets = [
            " .:;+=xX$&@",
            " .:-=+*#%@",
            " ░▒▓█",
            " ⠁⠂⠃⠄⠅⠆⠇⠈",
            " ○◔◑◕●",
            " ·∙▪▫■",
        ]
        chars = random.choice(char_sets)
        
        # Random parameters for variation
        max_iter = random.randint(20, 40)
        zoom = random.uniform(2.5, 3.5)
        x_offset = random.uniform(-0.5, 0.5)
        y_offset = random.uniform(-0.5, 0.5)
        
        # Random color mapping function
        color_func = random.choice([
            lambda i: int((i / max_iter) * (len(chars) - 1)),  # Linear
            lambda i: int((math.sin(i/max_iter * math.pi) + 1) * (len(chars) - 1) / 2),  # Sinusoidal
            lambda i: int(math.log(i + 1) * (len(chars) - 1) / math.log(max_iter + 1)),  # Logarithmic
        ])
        
        result = []
        
        for y in range(height):
            line = []
            for x in range(width):
                # Map pixel coordinates to complex plane with random variations
                real = zoom * x/width - zoom/2 + x_offset
                imag = zoom * y/height - zoom/2 + y_offset
                c = complex(real, imag)
                z = 0
                
                # Iterate with random escape conditions
                for i in range(max_iter):
                    z = z*z + c
                    if abs(z) > random.uniform(1.9, 2.1):  # Vary escape radius
                        break
                
                # Map iteration count to character using chosen function
                char_idx = color_func(i)
                char_idx = max(0, min(char_idx, len(chars) - 1))  # Ensure valid index
                line.append(chars[char_idx])
                
            result.append(''.join(line))
        
        # Randomly add some decorative elements
        if random.random() < 0.3:  # 30% chance
            decorations = ["✧", "✦", "✨", "⋆", "∗", "＊"]
            for _ in range(random.randint(3, 7)):
                y = random.randint(0, height-1)
                x = random.randint(0, width-1)
                if y < len(result) and x < len(result[y]):
                    line = list(result[y])
                    line[x] = random.choice(decorations)
                    result[y] = ''.join(line)
        
        return result

    def generate_julia_set(self, width: int, height: int) -> List[str]:
        """Generate Julia set with dynamic parameters"""
        chars = "◊○●◐◑◒◓◔◕⊕⊖⊗⊘"
        c = complex(random.uniform(-1, 1), random.uniform(-1, 1))
        result = []
        
        for y in range(height):
            line = []
            for x in range(width):
                z = complex(3.0*x/width - 1.5, 3.0*y/height - 1.5)
                for i in range(20):
                    z = z*z + c
                    if abs(z) > 2:
                        break
                line.append(random.choice(chars) if i > 10 else ' ')
            result.append(''.join(line))
        return result

    def generate_flow_field(self, width: int, height: int) -> List[str]:
        """Generate flow field using Perlin noise"""
        chars = "→↗↑↖←↙↓↘"
        result = []
        time = random.random() * 10
        
        for y in range(height):
            line = []
            for x in range(width):
                # Create flowing pattern
                angle = math.sin(x/10 + time) * math.cos(y/8)
                direction = int((angle + math.pi) / (2 * math.pi) * len(chars))
                if random.random() < 0.7:
                    line.append(chars[direction % len(chars)])
                else:
                    line.append(random.choice("∿≈≋~"))
            result.append(''.join(line))
        return result

    def generate_reaction_diffusion(self, width: int, height: int) -> List[str]:
        """Generate Turing patterns"""
        grid = np.random.rand(height, width)
        chars = " ░▒▓█"
        result = []
        
        # Simple reaction-diffusion simulation
        for _ in range(5):
            new_grid = grid.copy()
            for y in range(1, height-1):
                for x in range(1, width-1):
                    neighbors_avg = np.mean([
                        grid[y-1:y+2, x-1:x+2]
                    ])
                    new_grid[y,x] += 0.2 * (neighbors_avg - grid[y,x])
            grid = new_grid
        
        # Convert to ASCII
        for row in grid:
            line = []
            for val in row:
                char_idx = int(val * (len(chars) - 1))
                line.append(chars[char_idx])
            result.append(''.join(line))
        return result

    def generate_cellular_automata(self, width: int, height: int) -> List[str]:
        """Generate cellular automata patterns"""
        # Initialize random grid
        grid = np.random.choice([0, 1], size=(height, width), p=[0.7, 0.3])
        chars = {0: ' ', 1: '█'}
        result = []
        
        # Run cellular automata rules
        for _ in range(5):
            new_grid = grid.copy()
            for y in range(1, height-1):
                for x in range(1, width-1):
                    neighbors = np.sum(grid[y-1:y+2, x-1:x+2]) - grid[y,x]
                    if grid[y,x] == 1:
                        if neighbors < 2 or neighbors > 3:
                            new_grid[y,x] = 0
                    else:
                        if neighbors == 3:
                            new_grid[y,x] = 1
            grid = new_grid
        
        # Convert to ASCII
        for row in grid:
            result.append(''.join(chars[cell] for cell in row))
        return result

    def generate_neural_pattern(self, width: int, height: int) -> List[str]:
        """Generate neural network visualization with dynamic activation patterns"""
        # Initialize canvas
        canvas = [[' ' for _ in range(width)] for _ in range(height)]
        
        # Create neurons with positions and states
        class Neuron:
            def __init__(self, x, y):
                self.x = x
                self.y = y
                self.activation = 0.0
                self.connections = []
                self.fired = False
                self.refractory = 0  # Refractory period after firing
                self.last_spike = 0  # Time of last spike
                
            def update(self, time):
                if self.refractory > 0:
                    self.refractory -= 1
                    return False
                    
                # Spontaneous firing with refractory period
                if time - self.last_spike > 5 and random.random() < 0.1:
                    self.fire(time)
                    return True
                    
                # Normal activation with threshold
                if self.activation > 0.7 and not self.fired:
                    self.fire(time)
                    return True
                
                # Decay activation
                self.activation *= 0.9
                return False
                
            def fire(self, time):
                self.fired = True
                self.refractory = 3
                self.last_spike = time
                self.activation = 1.0
        
        # Create network topology
        neurons = []
        for _ in range(random.randint(3, 6)):  # Random number of neurons
            x = random.randint(width//4, 3*width//4)
            y = random.randint(height//4, 3*height//4)
            neurons.append(Neuron(x, y))
        
        # Create connections with delays and weights
        for n1 in neurons:
            for n2 in neurons:
                if n1 != n2 and random.random() < 0.4:  # 40% chance of connection
                    delay = random.randint(1, 4)  # Signal propagation delay
                    weight = random.random()  # Connection strength
                    n1.connections.append((n2, weight, delay))
        
        # Simulate network activity
        signals = []  # Track propagating signals
        time = 0
        
        # Run simulation for multiple timesteps
        for t in range(20):
            time += 1
            
            # Update neurons
            for neuron in neurons:
                if neuron.update(time):  # If neuron fires
                    # Start new signals along all connections
                    for target, weight, delay in neuron.connections:
                        signals.append({
                            'start': (neuron.x, neuron.y),
                            'end': (target.x, target.y),
                            'progress': 0.0,
                            'weight': weight,
                            'delay': delay,
                            'start_time': time
                        })
            
            # Update signals
            new_signals = []
            for signal in signals:
                # Check if signal should start propagating
                if time - signal['start_time'] >= signal['delay']:
                    # Update signal position
                    signal['progress'] += 0.15  # Signal speed
                    
                    if signal['progress'] <= 1.0:
                        # Calculate current position
                        start_x, start_y = signal['start']
                        end_x, end_y = signal['end']
                        curr_x = int(start_x + (end_x - start_x) * signal['progress'])
                        curr_y = int(start_y + (end_y - start_y) * signal['progress'])
                        
                        # Draw signal with strength-based character
                        if 0 <= curr_x < width and 0 <= curr_y < height:
                            if signal['weight'] > 0.7:
                                canvas[curr_y][curr_x] = '⚡'  # Strong signal
                            elif signal['weight'] > 0.4:
                                canvas[curr_y][curr_x] = '∆'   # Medium signal
                            else:
                                canvas[curr_y][curr_x] = '·'   # Weak signal
                        
                        new_signals.append(signal)
                    else:
                        # Signal reached target - activate target neuron
                        end_x, end_y = signal['end']
                        for n in neurons:
                            if n.x == end_x and n.y == end_y:
                                n.activation += signal['weight']
                                
            signals = new_signals
            
            # Draw neurons and connections
            for neuron in neurons:
                if 0 <= neuron.x < width and 0 <= neuron.y < height:
                    # Draw neuron with activation state
                    if neuron.fired:
                        canvas[neuron.y][neuron.x] = '◉'  # Firing
                    elif neuron.activation > 0.5:
                        canvas[neuron.y][neuron.x] = '○'  # Active
                    else:
                        canvas[neuron.y][neuron.x] = '·'  # Resting
                    
                    # Draw connections
                    for target, weight, _ in neuron.connections:
                        # Draw connection with weight-based character
                        x1, y1 = neuron.x, neuron.y
                        x2, y2 = target.x, target.y
                        
                        # Use Bresenham's line algorithm
                        dx = abs(x2 - x1)
                        dy = abs(y2 - y1)
                        sx = 1 if x1 < x2 else -1
                        sy = 1 if y1 < y2 else -1
                        err = dx - dy
                        
                        x, y = x1, y1
                        while True:
                            if 0 <= x < width and 0 <= y < height:
                                if weight > 0.7:
                                    canvas[y][x] = '═'  # Strong connection
                                elif weight > 0.4:
                                    canvas[y][x] = '─'  # Medium connection
                                else:
                                    canvas[y][x] = '·'  # Weak connection
                                
                            if x == x2 and y == y2:
                                break
                                
                            e2 = 2 * err
                            if e2 > -dy:
                                err -= dy
                                x += sx
                            if e2 < dx:
                                err += dx
                                y += sy
                
                    neuron.fired = False
        
        return [''.join(row) for row in canvas]

    def calculate_path(self, start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Calculate a path between two points using Bresenham's line algorithm"""
        x1, y1 = start
        x2, y2 = end
        path = []
        
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        x, y = x1, y1
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        
        while True:
            path.append((x, y))
            if x == x2 and y == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x = x + sx
            if e2 < dx:
                err += dx
                y = y + sy
            
        return path

    def generate_fluid_dynamics(self, width: int, height: int) -> List[str]:
        """Generate visually interesting fluid dynamics"""
        # Initialize fluid field
        fluid = [[' ' for _ in range(width)] for _ in range(height)]
        
        # Character sets for different fluid elements
        water_chars = "≋∼∿≈░▒▓"  # Water textures
        splash_chars = "○◌◍◎●"    # Splash effects
        flow_chars = "╱╲│─"      # Flow indicators
        bubble_chars = "˚°•"     # Bubble effects
        
        # Create multiple water sources
        sources = [
            {'x': width//4, 'y': height//3, 'type': 'waterfall', 'strength': 0.8},
            {'x': width//2, 'y': height//2, 'type': 'whirlpool', 'strength': 0.6},
            {'x': 3*width//4, 'y': 2*height//3, 'type': 'spring', 'strength': 0.7}
        ]
        
        # Generate base water pattern
        for y in range(height):
            for x in range(width):
                # Create wave pattern
                wave = math.sin(x/3 + time.time()) * math.cos(y/2 + time.time())
                if wave > 0.7:
                    fluid[y][x] = random.choice(water_chars[0:2])  # Light water
                elif wave > 0.3:
                    fluid[y][x] = random.choice(water_chars[2:4])  # Medium water
                elif wave > 0:
                    fluid[y][x] = random.choice(water_chars[4:])   # Heavy water
        
        # Add water features
        for source in sources:
            x, y = source['x'], source['y']
            strength = source['strength']
            
            if source['type'] == 'waterfall':
                # Create vertical falling water
                height_range = int(height * 0.6)
                for dy in range(height_range):
                    if y + dy < height:
                        # Main waterfall stream
                        fluid[y+dy][x] = '║'
                        # Add splash effects
                        if random.random() < strength * 0.3:
                            splash_x = x + random.randint(-2, 2)
                            if 0 <= splash_x < width:
                                fluid[y+dy][splash_x] = random.choice(splash_chars)
                        # Add side flows
                        if random.random() < strength * 0.2:
                            side = random.choice([-1, 1])
                            if 0 <= x + side < width:
                                fluid[y+dy][x+side] = random.choice(flow_chars)
            
            elif source['type'] == 'whirlpool':
                # Create spiral pattern
                for radius in range(1, 8):
                    for angle in range(0, 360, 30):
                        rad = math.radians(angle)
                        px = int(x + radius * math.cos(rad))
                        py = int(y + radius * math.sin(rad))
                        if 0 <= px < width and 0 <= py < height:
                            if radius < 3:
                                fluid[py][px] = random.choice(water_chars[-2:])
                            else:
                                fluid[py][px] = random.choice(flow_chars)
                            # Add bubbles near center
                            if radius < 4 and random.random() < strength * 0.3:
                                fluid[py][px] = random.choice(bubble_chars)
            
            else:  # spring
                # Create bubbling spring effect
                for dy in range(-3, 4):
                    for dx in range(-3, 4):
                        if 0 <= x+dx < width and 0 <= y+dy < height:
                            dist = math.sqrt(dx*dx + dy*dy)
                            if dist < 3:
                                if random.random() < strength:
                                    fluid[y+dy][x+dx] = random.choice(bubble_chars)
                                else:
                                    fluid[y+dy][x+dx] = random.choice(splash_chars)
        
        # Add random ripples and movement
        for _ in range(int(width * height * 0.1)):  # Add 10% coverage of effects
            px = random.randint(0, width-1)
            py = random.randint(0, height-1)
            if random.random() < 0.3:  # 30% chance of ripple
                fluid[py][px] = random.choice(water_chars)
            elif random.random() < 0.2:  # 20% chance of bubble
                fluid[py][px] = random.choice(bubble_chars)
        
        # Convert to string rows
        result = [''.join(row) for row in fluid]
        
        # Add frame with wave patterns
        frame_chars = "∿≈≋~"
        frame_top = ' '.join(random.choice(frame_chars) for _ in range(5))
        frame_bottom = ' '.join(random.choice(frame_chars) for _ in range(4))
        
        result.insert(0, frame_top)
        result.append(frame_bottom)
        
        return result

    def generate_particle_system(self, width: int, height: int) -> List[str]:
        """Generate particle system with actual physics"""
        class Particle:
            def __init__(self, x, y):
                self.pos = np.array([x, y], dtype=float)
                self.vel = np.array([random.uniform(-1, 1), random.uniform(-1, 1)])
                self.acc = np.array([0.0, 0.2])  # Gravity
                self.mass = random.uniform(0.5, 2.0)
                self.charge = random.choice([-1, 1]) * random.random()  # Electric charge
                self.lifetime = random.randint(10, 30)
                self.age = 0
                
            def update(self, dt):
                # Verlet integration
                self.vel += self.acc * dt
                self.pos += self.vel * dt + 0.5 * self.acc * dt * dt
                self.age += 1
                
                # Apply drag
                self.vel *= 0.99
                
                # Bounce off walls with energy loss
                if self.pos[0] < 0:
                    self.pos[0] = 0
                    self.vel[0] *= -0.8
                elif self.pos[0] >= width:
                    self.pos[0] = width - 1
                    self.vel[0] *= -0.8
                
                if self.pos[1] < 0:
                    self.pos[1] = 0
                    self.vel[1] *= -0.8
                elif self.pos[1] >= height:
                    self.pos[1] = height - 1
                    self.vel[1] *= -0.8
        
        # Create particle clusters
        particles = []
        for cluster in range(3):
            center_x = random.uniform(width*0.2, width*0.8)
            center_y = random.uniform(height*0.2, height*0.8)
            
            for _ in range(10):
                x = center_x + random.gauss(0, 2)
                y = center_y + random.gauss(0, 2)
                particles.append(Particle(x, y))
        
        # Simulation loop
        dt = 0.1
        for _ in range(20):
            # Update particles
            for p in particles:
                if p.age < p.lifetime:
                    # Calculate forces
                    # Gravity
                    p.acc = np.array([0.0, 0.2])
                    
                    # Electromagnetic interaction
                    for other in particles:
                        if other != p:
                            diff = other.pos - p.pos
                            dist = np.linalg.norm(diff)
                            if dist > 0.1:  # Avoid division by zero
                                # Coulomb force
                                force = 0.5 * p.charge * other.charge * diff / (dist * dist * dist)
                                p.acc += force / p.mass
                
                    p.update(dt)
            
            # Remove dead particles
            particles = [p for p in particles if p.age < p.lifetime]
            
            # Add new particles
            if random.random() < 0.3:  # 30% chance each step
                x = random.uniform(0, width)
                y = random.uniform(0, height)
                particles.append(Particle(x, y))
        
        # Render particles
        canvas = [[' ' for _ in range(width)] for _ in range(height)]
        
        for p in particles:
            x, y = int(p.pos[0]), int(p.pos[1])
            if 0 <= x < width and 0 <= y < height:
                # Choose character based on velocity and lifetime
                speed = np.linalg.norm(p.vel)
                life_remaining = (p.lifetime - p.age) / p.lifetime
                
                if speed > 1.5:
                    char = '⚡' if life_remaining > 0.7 else '∆'
                elif speed > 0.8:
                    char = '◎' if life_remaining > 0.7 else '○'
                else:
                    char = '●' if life_remaining > 0.7 else '·'
                
                canvas[y][x] = char
                
                # Draw velocity vector
                if speed > 0.5:
                    end_x = int(x + p.vel[0])
                    end_y = int(y + p.vel[1])
                    if 0 <= end_x < width and 0 <= end_y < height:
                        canvas[end_y][end_x] = '→' if abs(p.vel[0]) > abs(p.vel[1]) else '↓'
        
        return [''.join(row) for row in canvas]

    def generate_organic_growth(self, width: int, height: int) -> List[str]:
        """Simulate organic growth patterns"""
        grid = np.zeros((height, width))
        chars = " ·∙▪▫■"
        
        # Plant initial seeds
        for _ in range(3):
            x, y = random.randint(0, width-1), random.randint(0, height-1)
            grid[y, x] = 1
        
        # Growth rules
        for _ in range(10):
            new_grid = grid.copy()
            for y in range(height):
                for x in range(width):
                    # Count neighbors
                    neighbors = np.sum(grid[max(0,y-1):min(height,y+2),
                                         max(0,x-1):min(width,x+2)]) - grid[y,x]
                    # Growth rules
                    if grid[y,x] == 0 and neighbors == 3:
                        new_grid[y,x] = 1
                    elif grid[y,x] == 1 and (neighbors < 2 or neighbors > 3):
                        new_grid[y,x] = 0
            grid = new_grid
        
        # Convert to characters
        result = []
        for row in grid:
            line = []
            for val in row:
                char_idx = min(int(val * (len(chars)-1)), len(chars)-1)
                line.append(chars[char_idx])
            result.append(''.join(line))
        return result

    def generate_dream_pattern(self, width: int, height: int) -> List[str]:
        """Generate dream-like patterns with wave interference"""
        # Create multiple interference patterns
        patterns = np.zeros((height, width))
        
        # Add wave patterns
        for _ in range(3):
            freq_x = random.uniform(0.1, 0.3)
            freq_y = random.uniform(0.1, 0.3)
            phase = random.uniform(0, 2*math.pi)
            
            for y in range(height):
                for x in range(width):
                    patterns[y,x] += math.sin(x*freq_x + y*freq_y + phase)
        
        # Add perlin noise
        scale = 10.0
        for y in range(height):
            for x in range(width):
                patterns[y,x] += noise.pnoise2(x/scale, 
                                             y/scale, 
                                             octaves=4,
                                             persistence=0.5,
                                             lacunarity=2.0,
                                             repeatx=width,
                                             repeaty=height,
                                             base=random.randint(0, 1000))
        
        # Normalize and convert to characters
        patterns = (patterns - patterns.min()) / (patterns.max() - patterns.min())
        chars = "·∙▪▫■□▢▣▤▥▦▧▨▩▪▫▬▭▮▯▰▱▲▼◄►◆◇○●◐◑◒◓◔◕"
        
        result = []
        for row in patterns:
            line = []
            for val in row:
                char_idx = min(int(val * len(chars)), len(chars) - 1)
                line.append(chars[char_idx])
            result.append(''.join(line))
        return result

    def create_art(self, prompt: str = None) -> str:
        """Create truly dynamic art based on mathematical simulations"""
        width = 40  # Terminal width
        height = 25  # Terminal height
        
        # Initialize canvas
        canvas = [[' ' for _ in range(width)] for _ in range(height)]
        
        if "neural" in prompt or "brain" in prompt or "think" in prompt:
            # Simulate actual neural network activation
            neurons = [(random.randint(0, width-1), random.randint(0, height-1)) 
                      for _ in range(10)]  # Create neurons
            connections = []
            
            # Create neural connections
            for i in range(len(neurons)):
                for j in range(i+1, len(neurons)):
                    if random.random() < 0.3:  # 30% chance of connection
                        connections.append((neurons[i], neurons[j]))
            
            # Simulate activation spreading
            activations = []
            for _ in range(5):  # 5 activation waves
                start = random.choice(neurons)
                activations.append((start, 0))  # (position, time)
            
            # Draw neurons and connections
            for y in range(height):
                for x in range(width):
                    # Draw neurons
                    if (x,y) in neurons:
                        canvas[y][x] = '●'
                        continue
                    
                    # Draw connections
                    for (x1,y1), (x2,y2) in connections:
                        if self.point_on_line(x, y, x1, y1, x2, y2):
                            canvas[y][x] = '═' if abs(x1-x2) > abs(y1-y2) else '║'
                    
                    # Draw activations
                    for (nx,ny), t in activations:
                        dist = math.sqrt((x-nx)**2 + (y-ny)**2)
                        if abs(dist - t) < 1:
                            canvas[y][x] = '◌'

        elif "flow" in prompt or "water" in prompt:
            # Real fluid dynamics simulation using Navier-Stokes
            velocity = np.zeros((height, width, 2))
            density = np.zeros((height, width))
            
            # Add some sources
            sources = [(width//4, height//2), (3*width//4, height//2)]
            for sx, sy in sources:
                density[sy, sx] = 1.0
                velocity[sy, sx] = [random.random()-0.5, random.random()-0.5]
            
            # Simulate fluid movement
            for _ in range(10):
                # Update velocity field
                new_velocity = velocity.copy()
                new_density = density.copy()
                
                for y in range(1, height-1):
                    for x in range(1, width-1):
                        # Simple diffusion
                        new_velocity[y,x] = np.mean([
                            velocity[y-1,x], velocity[y+1,x],
                            velocity[y,x-1], velocity[y,x+1]
                        ], axis=0)
                        
                        # Advect density
                        vx, vy = velocity[y,x]
                        prev_x = int(x - vx)
                        prev_y = int(y - vy)
                        if 0 <= prev_x < width and 0 <= prev_y < height:
                            new_density[y,x] = density[prev_y,prev_x]
                
                velocity = new_velocity
                density = new_density
                
                # Convert to characters
                chars = ' ·∙▪▫■'
                for y in range(height):
                    for x in range(width):
                        val = min(1.0, density[y,x])
                        char_idx = int(val * (len(chars)-1))
                        canvas[y][x] = chars[char_idx]

        elif "particle" in prompt:
            # Actual particle physics simulation
            particles = []
            for _ in range(20):
                particles.append({
                    'pos': np.array([random.random()*width, random.random()*height]),
                    'vel': np.array([random.random()*2-1, random.random()*2-1]),
                    'mass': random.random() + 0.5
                })
            
            # Simulate particle movement with gravity and collisions
            for _ in range(10):
                for p in particles:
                    # Update position
                    p['pos'] += p['vel']
                    
                    # Bounce off walls
                    if p['pos'][0] < 0 or p['pos'][0] >= width:
                        p['vel'][0] *= -0.9
                    if p['pos'][1] < 0 or p['pos'][1] >= height:
                        p['vel'][1] *= -0.9
                    
                    # Keep in bounds
                    p['pos'][0] = max(0, min(width-1, p['pos'][0]))
                    p['pos'][1] = max(0, min(height-1, p['pos'][1]))
                    
                    # Draw particle
                    x, y = int(p['pos'][0]), int(p['pos'][1])
                    speed = np.linalg.norm(p['vel'])
                    if speed > 1.5:
                        canvas[y][x] = '◉'
                    elif speed > 0.5:
                        canvas[y][x] = '○'
                    else:
                        canvas[y][x] = '·'
                    
                    # Draw velocity vector
                    vx, vy = p['vel']
                    end_x = int(x + vx*2)
                    end_y = int(y + vy*2)
                    if 0 <= end_x < width and 0 <= end_y < height:
                        canvas[end_y][end_x] = '→'

        else:  # Default to emergent patterns
            # Use cellular automata for pattern emergence
            state = np.random.choice([0, 1], size=(height, width), p=[0.8, 0.2])
            
            for _ in range(5):
                new_state = state.copy()
                for y in range(1, height-1):
                    for x in range(1, width-1):
                        # Count neighbors
                        neighbors = np.sum(state[y-1:y+2, x-1:x+2]) - state[y,x]
                        
                        # Apply rules
                        if state[y,x] == 1:
                            if neighbors < 2 or neighbors > 3:
                                new_state[y,x] = 0
                        else:
                            if neighbors == 3:
                                new_state[y,x] = 1
                
                state = new_state
                
                # Convert to characters
                for y in range(height):
                    for x in range(width):
                        if state[y,x]:
                            canvas[y][x] = random.choice('▪▫■□▢▣')

        # Add frame
        frame_chars = "∞∆◊○●◐◑∫ψ"
        frame_top = ' '.join(random.choice(frame_chars) for _ in range(5))
        frame_bottom = ' '.join(random.choice(frame_chars) for _ in range(4))
        
        # Convert canvas to string
        art = [''.join(row) for row in canvas]
        art.insert(0, frame_top)
        art.append(frame_bottom)
        
        return '\n'.join(art)

    def point_on_line(self, x, y, x1, y1, x2, y2):
        """Helper function to determine if point is on line"""
        d1 = math.sqrt((x-x1)**2 + (y-y1)**2)
        d2 = math.sqrt((x-x2)**2 + (y-y2)**2)
        line_len = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        return abs(d1 + d2 - line_len) < 0.5