import requests
from lxml import html
from lxml.etree import tostring
from youtube_transcript_api import YouTubeTranscriptApi

#Totally useless file tbh
def get_video_captions(video_id):

	CAPTION_URL = 'https://www.diycaptions.com/php/get-automatic-captions-as-txt.php?id='+video_id+'&language=asr'

	captionPage = requests.get(CAPTION_URL)
	captionTree = html.fromstring(captionPage.content)
	caption = captionTree.xpath('//div[@contenteditable="true"]/text()')

	return(str(caption))

if (__name__ == '__main__'):
	video_id='EuPSibuIKIg'
	transcript_data = YouTubeTranscriptApi.get_transcript(video_id)

	text_list = []
	for trans_dict in transcript_data:
		text_list.append(trans_dict['text'])

	caption_text = "".join(text_list)
	print(caption_text)



