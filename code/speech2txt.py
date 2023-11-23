import srt
import time
import datetime
from google.cloud import speech_v1p1beta1 as speech


def long_running_recognize(sample_rate, channels, language_code, storage_uri):

    start_time = datetime.datetime.now()
    print("Transcribing... {} ".format(storage_uri))
    client = speech.SpeechClient()

    encoding = speech.RecognitionConfig.AudioEncoding.FLAC

    config = {
        "enable_word_time_offsets": True,
        "enable_automatic_punctuation": True,
        "sample_rate_hertz": sample_rate,
        "language_code": language_code,
        "encoding": encoding,
        "audio_channel_count": channels,
        #"enable_word_confidence": True
    }
    if language_code == 'en-US':
        config["use_enhanced"] = True
        config["model"] = "video"

    audio = {"uri": storage_uri}

    try:
        operation = client.long_running_recognize(
            request={
                "config": config,
                "audio": audio,
            }
        )
        response = operation.result(timeout=3600)

        subs = []

        for result in response.results:
            subs = break_sentences(subs, result.alternatives[0])
    except Exception as e:
        print(f"ERROR while transcribing {storage_uri}: ", e)
    spent_time = str(datetime.datetime.now() - start_time)
    print(f"Transcrbed with Time {spent_time}, {storage_uri}")
    return subs


def break_sentences(subs, alternative, max_chars=30, max_time=10):
    firstword = True
    charcount = 0
    idx = len(subs) + 1
    content = ""
    inter_count = 0
    for w in alternative.words:
        inter_count += 1
        if firstword:
            start_time = w.start_time.seconds
            start_hhmmss = time.strftime('%H:%M:%S', time.gmtime(start_time))
            start_ms = int(w.start_time.microseconds / 1000)
            start = start_hhmmss + "," + str(start_ms)
        end_time = w.end_time.seconds
        end_hhmmss = time.strftime('%H:%M:%S', time.gmtime(end_time))
        end_ms = int(w.end_time.microseconds / 1000)
        end = end_hhmmss + "," + str(end_ms)
        delta_time = end_time - start_time

        if w.word.find("|"):
            wd = w.word.split("|")[0]

        else:
            wd = w.word
        charcount += len(wd)
        content += " " + wd.strip()

        if ("." in wd or "!" in wd or "?" in wd or
                charcount > max_chars or
                ("," in wd and not firstword) or
                delta_time > max_time):
            subs.append(srt.Subtitle(index=idx,
                                     start=srt.srt_timestamp_to_timedelta(start),
                                     end=srt.srt_timestamp_to_timedelta(end),
                                     content=srt.make_legal_content(content)))
            firstword = True
            idx += 1
            content = ""
            charcount = 0
        else:
            firstword = False
            if inter_count == len(alternative.words):
                subs.append(srt.Subtitle(index=idx,
                                         start=srt.srt_timestamp_to_timedelta(start),
                                         end=srt.srt_timestamp_to_timedelta(end),
                                         content=srt.make_legal_content(content)))
    return subs


def write_srt(out_file, language_code, subs):
    srt_file = f"{out_file}.{language_code}.srt"
    print("Writing subtitles to: {}".format(srt_file))
    with open(srt_file, 'w') as f:
        f.writelines(srt.compose(subs))
    return


def write_txt(out_file, language_code, subs):
    txt_file = f"{out_file}.{language_code}.txt"
    print("Writing text to: {}".format(txt_file))
    with open(txt_file, 'w') as f:
        for s in subs:
            f.write(s.content.strip() + "\n")
    return


def speech2txt(sample_rate, channels, language_code, storage_uri, out_file):
    subs = long_running_recognize(sample_rate, channels, language_code, storage_uri)
    write_srt(out_file, language_code, subs)
    write_txt(out_file, language_code, subs)
    return

