import source.engine as game_engine
from source.engine_except import EngineError


def main():
    engine = game_engine.Engine()
    engine.launch()
    engine.run()


if __name__ == '__main__':
    main()
