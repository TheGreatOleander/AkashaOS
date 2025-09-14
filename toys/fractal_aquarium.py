# toys/fractal_aquarium.py
"""
Fractal Aquarium - AkashaOS Toy

Interactive fractal fish aquarium:
- Spawn fish with SPACE
- Drag files in to feed fish and change their color/size/behavior
"""

import pygame, math, random, sys, os, hashlib, mimetypes
from PIL import Image

# ---------- Setup ----------
pygame.init()
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Fractal Aquarium")

# ---------- Helper Functions ----------
def entropy_color(path):
    """Generate a color from file entropy (first 4KB)."""
    try:
        with open(path, "rb") as f:
            data = f.read(4096)
        h = hashlib.sha256(data).hexdigest()
        return (int(h[0:2],16), int(h[2:4],16), int(h[4:6],16))
    except Exception:
        return (200,200,200)

# ---------- Fractal Fish ----------
class FractalFish:
    def __init__(self, entropy_seed=None):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.speed = random.uniform(0.5, 1.5)
        self.color = [random.randint(100,255) for _ in range(3)]
        self.phase = random.random() * math.pi
        self.size = random.randint(20, 60)
        self.entropy_seed = entropy_seed or random.random()
        self.behavior = "default"

    def update(self):
        self.x += math.cos(self.phase + self.entropy_seed) * self.speed
        self.y += math.sin(self.phase * 0.5 + self.entropy_seed) * self.speed
        self.phase += 0.02
        self.x %= WIDTH
        self.y %= HEIGHT
        self.color = [(c + random.randint(-2,2)) % 256 for c in self.color]

    def draw(self, surface):
        for i in range(120):
            t = i / 20.0
            dx = math.sin(t + self.phase) * self.size
            dy = math.cos(2*t + self.phase) * self.size/2
            px, py = int(self.x + dx), int(self.y + dy)
            pygame.draw.circle(surface, self.color, (px, py), 2)

    def feed(self, filepath):
        try:
            size = os.path.getsize(filepath)
            mime, _ = mimetypes.guess_type(filepath)

            # Empty file → Ghost
            if size == 0:
                self.color = [180, 220, 255]
                self.speed = 0.3
                self.size = 40
                self.behavior = "ghost"

            # Big/random file → Chaos
            elif size > 1000000:
                self.color = [random.randint(150,255) for _ in range(3)]
                self.speed = 3.0
                self.size = 70
                self.behavior = "chaos"

            # Text files → Calm
            elif mime and "text" in mime:
                self.color = [200, 150, 200]
                self.speed = 1.0
                self.size = 50
                self.behavior = "calm"

            # Images → Mimicry
            elif mime and "image" in mime:
                with Image.open(filepath) as img:
                    img = img.resize((1,1))
                    r,g,b = img.getpixel((0,0))
                self.color = [r,g,b]
                self.speed = 1.5
                self.size = 60
                self.behavior = "mimic"

            # Audio → Rhythm
            elif mime and ("audio" in mime or filepath.endswith((".mp3",".wav"))):
                self.color = [255,200,150]
                self.speed = 2.0
                self.size = 55
                self.behavior = "rhythm"

            # Other → Default
            else:
                self.color = list(entropy_color(filepath))
                self.size = 40 + (size % 60)
                self.behavior = "default"

        except Exception as e:
            print("Feeding error:", e)

# ---------- Starfield ----------
class Starfield:
    def __init__(self, count=200):
        self.stars = [(random.randint(0,WIDTH), random.randint(0,HEIGHT), random.randint(1,3)) for _ in range(count)]
    def draw(self, surface):
        for x,y,r in self.stars:
            pygame.draw.circle(surface, (100,100,200), (x,y), r)

# ---------- Main Loop ----------
def main():
    fish = [FractalFish() for _ in range(12)]
    stars = Starfield()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                fish.append(FractalFish())
            if event.type == pygame.DROPFILE:
                path = event.file
                random.choice(fish).feed(path)

        screen.fill((0,0,30))
        stars.draw(screen)

        for f in fish:
            f.update()
            f.draw(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
