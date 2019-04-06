import source.engine as game_engine
from source.engine_except import EngineError


def main():
    try:
        engine = game_engine.Engine()
        engine.launch()
        engine.run()
    except EngineError as error:
        print('An error has occurred. Error message: {}'.format(error.message))
        with open('logger', 'w') as log:
            log.write(error.message + '\n' + error.details)


if __name__ == '__main__':
    main()
