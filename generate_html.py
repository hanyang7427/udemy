#!/usr/bin/env python
# srt to vtt:https://github.com/nwoltman/srt-to-vtt-cl

import os
import sys

target = sys.argv[1]

level_1 = [name for name in os.listdir(target) if os.path.isdir(os.path.join(target, name))]
level_1 = [name for name in level_1 if not name.startswith('.')]
level_1 = sorted(level_1)


def gen_level1_index(target=target,level_1=level_1):
	level1_template = '''
	<!DOCTYPE html>
	<html lang="en">

	<head>
	  <meta charset="UTF-8">
	  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=1">
	  <meta http-equiv="X-UA-Compatible" content="ie=edge">
	  <title>Contents</title>
	</head>

	<body>

	<div>
	  {}
	</div>

	</body>
	'''
	a_template = '<a href="http://192.168.1.250/Learn Website Hacking  Penetration Testing From Scratch/{}/index.html"><h4>{}</h4></a>\n'
	href = '\n'.join([a_template.format(i,i) for i in level_1])
	
	with open('./'+target+'/index.html','w') as f:
	    f.write(level1_template.format(href))


def srt2vtt(target=target):
	# 需要确保srt-vtt命令在同一目录
	os.system('./srt-vtt -v -r -q ' + target)


def gen_level2_index(target=target,level_1=level_1):
	level2_template = '''
	<!DOCTYPE html>
	<html lang="en">
	<head>
	  <meta charset="UTF-8">
	  <meta name="viewport" content="width=device-width, initial-scale=1.0">
	  <meta http-equiv="X-UA-Compatible" content="ie=edge">
	  <title>{title}</title>
	  <style type="text/css">
	    video {height}
	  </style>
	</head>
	<body>
	{divs}
	</body>
	'''
	div_template = '''
	<div>
	  <h3><p>{video_name}</p></h3>
	  <video controls>
	    <source src="{video_name}" type="video/mp4">
	    <track default="true" kind="subtitles" srclang="en" src="{vtt_name}" label="en">
	  </video>
	</div>
	'''

	for dir in level_1:
		c_dir = './'+target+'/'+dir
		video_names = [name for name in os.listdir(c_dir) if name.endswith('mp4')]
		video_names = sorted(video_names)
		vtt_names = [name for name in os.listdir(c_dir) if name.endswith('en.vtt')]
		vtt_names = sorted(vtt_names)
		divs_html = '\n'.join([div_template.format(video_name=video_name,vtt_name=vtt_name) for video_name,vtt_name in zip(video_names,vtt_names)])
		index_html = level2_template.format(divs=divs_html,title=dir,height='{height: 500px;}')
		with open(c_dir+'/index.html','w') as f:
			f.write(index_html)


if __name__ == '__main__':
	gen_level1_index()
	srt2vtt()
	gen_level2_index()


