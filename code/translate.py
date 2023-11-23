from google.cloud import translate
import time
import datetime


def batch_translate_text(
    input_uri, output_uri_prefix, project_id, location, source_lang, target_lang
):

    start_time = datetime.datetime.now()
    # call batch translate against orig.txt
    client = translate.TranslationServiceClient()
    gcs_source = {"input_uri": input_uri}
    input_configs_element = {"gcs_source": gcs_source, "mime_type": "text/plain"}
    gcs_destination = {"output_uri_prefix": output_uri_prefix}
    output_config = {"gcs_destination": gcs_destination}
    parent = f"projects/{project_id}/locations/{location}"

    try:
        print("Translating...", input_uri)
        operation = client.batch_translate_text(
            request={
                "parent": parent,  # Required para
                "source_language_code": source_lang,
                "target_language_codes": [target_lang],  # Up to 10 language codes here.
                "input_configs": [input_configs_element],
                "output_config": output_config,
            }
        )

        response = operation.result(timeout=3600)
    except Exception as e:
        print(f"ERROR while translating {input_uri}: ", e)
    spent_time = str(datetime.datetime.now() - start_time)
    print(f"Translated Time: {spent_time}", input_uri, "Total Characters: {}".format(response.total_characters), u"Translated: {}".format(response.translated_characters))
    return

