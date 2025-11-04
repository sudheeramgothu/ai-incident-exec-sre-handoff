import random, time, subprocess

racks = ["R12", "R14", "R18"]
clusters = ["east-app-cluster", "west-db-cluster", "north-ai-cluster"]

for i in range(3):
    rack = random.choice(racks)
    cluster = random.choice(clusters)
    print(f"Simulating incident {i+1}: rack {rack}, cluster {cluster}")
    subprocess.run([
        "python", "collector.py",
        "--event", "Auto-generated fault",
        "--rack", rack,
        "--cluster", cluster,
        "--cooling_temp_c", str(random.randint(80, 95))
    ])
    time.sleep(2)
