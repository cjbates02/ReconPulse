from networkkit import DiscoveryEngine, DetectionEngine

if __name__ == '__main__':
    # sudo $(which python) app.py
    detection_engine = DetectionEngine('10.0.97.0/24')
    detection_engine.run()