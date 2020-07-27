import os
from ffmpy3 import FFmpeg

# conda install FFmpeg

source_folder = 'youtube_downloader/mp4'

dst_folder = 'youtube_downloader/wav'

filenames = os.listdir(source_folder)
num = len(filenames)
ii = 0
for i in range(0, num):
    print('now is:', i)
    changefile = source_folder+'/'+filenames[i]
    # print(changefile[-3:])
    if changefile[-4:] != '.mp4':
        continue
    outputfile = dst_folder+'/'+str(ii)+'.wav'
    ii += 1
    ff = FFmpeg(
        inputs={changefile: None},
        outputs={outputfile: '-y -vn -ar 44100 -ac 1 -ab 192 -f wav'}  # 1:2
    )
    # print(ff.cmd)
    ff.run()
