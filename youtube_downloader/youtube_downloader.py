from pytube import YouTube
import _thread
import time

def YTdownload(url,i,count):
	yt = YouTube('http://youtube.com/watch?v='+url)
	yt.streams.filter(subtype='mp4').first().download('mp4/') #.filter(only_audio=True)
	count+=1
	print(i,': Finished!')
    
if __name__ == '__main__':
	global count
	count = 0
    
	ids=open("rerated_video_ids.txt", "r").readlines()

	num=len(ids)
	print('totally',num)
	for i in range(num):
		ids[i] = ids[i].strip('\n')

	for i in range(500,530):
		#print(i)
		_thread.start_new_thread(YTdownload,(ids[i],i,count,))
		time.sleep(7)

	print('all finished!-----------------')
	time.sleep(100)
	print('totally:',count)
