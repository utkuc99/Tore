# Try subtitle analysis

import os
import io
from google.cloud import videointelligence_v1 as videointelligence

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'backend_api/hopeful-ally-350713-ae076300eb06.json'


def subtitle_analysis(videoCode):

    path = videoCode + ".mp3"
    with io.open(path, "rb") as movie:
        input_content = movie.read()

    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.Feature.SPEECH_TRANSCRIPTION]

    config = videointelligence.SpeechTranscriptionConfig(
        language_code="tr-TR", enable_automatic_punctuation=True
    )
    video_context = videointelligence.VideoContext(speech_transcription_config=config)

    operation = video_client.annotate_video(
        request={
            "features": features,
            "input_content": input_content,
            "video_context": video_context,
        }
    )

    print("\nProcessing video for speech transcription.")

    result = operation.result(timeout=1800)

    # There is only one annotation_result since only
    # one video is processed.
    array = []
    annotation_results = result.annotation_results[0]
    for speech_transcription in annotation_results.speech_transcriptions:

        # The number of alternatives for each transcription is limited by
        # SpeechTranscriptionConfig.max_alternatives.
        # Each alternative is a different possible transcription
        # and has its own confidence score.
        for alternative in speech_transcription.alternatives:
            print("Alternative level information:")

            print("Transcript: {}".format(alternative.transcript))
            print("Confidence: {}\n".format(alternative.confidence))

            print("Word level information:")
            for word_info in alternative.words:
                word = word_info.word
                start_time = word_info.start_time
                end_time = word_info.end_time
                print(
                    "\t{}s - {}s: {}".format(
                        start_time.seconds + start_time.microseconds * 1e-6,
                        end_time.seconds + end_time.microseconds * 1e-6,
                        word,
                    )
                )
                array2 = []
                array2.append(start_time.seconds + start_time.microseconds * 1e-6)
                array2.append(end_time.seconds + end_time.microseconds * 1e-6)
                array.append(array2)

            print("array: " + str(array))

    otherSegments = []
    for i in range(0, len(array) - 1):
        segment = []
        segment.append(array[i][1])
        segment.append(array[i + 1][0])
        otherSegments.append(segment);

    print("Segments without subtitle : " + str(otherSegments))
    return otherSegments