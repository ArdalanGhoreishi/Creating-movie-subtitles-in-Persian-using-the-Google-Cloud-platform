# Creating-movie-subtitles-in-Persian-using-the-Google-Cloud-platform
An easy-to-use website designed for creating Persian subtitles for movies.

In this project, we employ an innovative adaptive load balancer to efficiently distribute workloads among the workers.

## Copyright
 Speech to text language code: https://cloud.google.com/speech-to-text/docs/languages

 Translate language code: https://cloud.google.com/translate/docs/languages

 Some Ideas for Implementation: https://github.com/OrganizationBin/trans_video_subs

## How to run?
1- install requirements ( google-cloud, google-cloud-speech>=1.2.0, google-cloud-translate>=2.0.0, srt>=3.0.0, google-cloud-storage>=1.33.0, ffmpy

2- open a terminal in the code directory

3- run load balancer => python3 LoadBalancer.py

4- run app.py => export FLASK_APP=app.py  => flask run

5- open your internet browser and try http://127.0.0.1:5000
