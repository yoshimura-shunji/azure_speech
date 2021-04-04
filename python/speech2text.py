import argparse
import azure.cognitiveservices.speech as speechsdk
import json
import logging
import os
import time

logger = logging.getLogger(__name__)
logging.basicConfig(level='INFO')

CONFIG_FILE = os.path.join(
    os.path.dirname(__file__),
    'config.json'
)


def get_config():
    with open(CONFIG_FILE) as f:
        config = json.load(f)
    return config


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    parser.add_argument('output_file')
    args = parser.parse_args()
    return args


def get_phrase_list(phrase_list_file):
    with open(phrase_list_file) as f:
        phrase_list = f.readlines()
    phrase_list = [x.strip() for x in phrase_list]
    return phrase_list


def recognize_from_file(input_file, config):
    speech_config = speechsdk.SpeechConfig(
        subscription=config['subscription'],
        region=config['region'],
        speech_recognition_language=config['speech_recognition_language']
    )
    if config['enable_dictation']:
        speech_config.enable_dictation()
    audio_config = speechsdk.AudioConfig(
        filename=input_file
    )
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config,
        audio_config=audio_config
    )

    try:
        if config['phrase_list_file']:
            phrase_list = get_phrase_list(config['phrase_list_file'])
            phrase_list_grammar = speechsdk.PhraseListGrammar.from_recognizer(
                speech_recognizer
            )
            for phrase in phrase_list:
                logger.info('Adding phrase to grammer: {}'.format(phrase))
                phrase_list_grammar.addPhrase(phrase)
    except KeyError:
        logger.info('No phrase_list_file info found in config file')
    except IOError as e:
        logger.exception(e)

    done = False
    recognized_events = []

    def stop_cb(evt):
        logger.info('CLOSING on {}'.format(evt))
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done = True

    def save_events(evt):
        logger.info('RECOGNIZED: {}'.format(evt))
        recognized_events.append(evt)

    speech_recognizer.recognizing.connect(
        lambda evt: logger.debug('RECOGNIZING: {}'.format(evt))
    )
    speech_recognizer.recognized.connect(save_events)
    speech_recognizer.session_started.connect(
        lambda evt: logger.info('SESSION STARTED: {}'.format(evt))
    )
    speech_recognizer.session_stopped.connect(
        lambda evt: logger.info('SESSION STOPPED {}'.format(evt))
    )
    speech_recognizer.canceled.connect(
        lambda evt: logger.info('CANCELED {}'.format(evt))
    )

    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)

    logger.info(
        'number of recognized events: {}'.format(
            len(recognized_events)
        )
    )
    return recognized_events


def main():
    args = parse_args()

    input_file = args.input_file
    output_file = args.output_file

    config = get_config()

    if not os.path.exists(input_file):
        logger.error('file not exist: {}'.format(input_file))
        raise IOError

    evts = recognize_from_file(input_file, config)
    results = [x.result.text for x in evts]
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(results))


if __name__ == '__main__':
    main()
