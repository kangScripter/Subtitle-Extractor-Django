import subprocess
import os,re
import platform
from pathlib import Path
from pymediainfo import MediaInfo
from .languages import language_code_converter,language_converter
from srt_to_vtt import srt_to_vtt # type: ignore
import urllib.parse

BASE_DIR = Path(__file__).resolve().parent.parent
# CCExtractorEXE = BASE_DIR / 'bin' / 'ccextractor.exe'
if platform.system() == "Windows":
     FFMPEG = BASE_DIR / 'bin' / 'ffmpeg.exe'
elif platform.system() == "Linux":
     FFMPEG = 'ffmpeg'
else:
    raise Exception("Os Not suppported")
class SubtitlesExtract():
 
    def __init__(self) -> None:

        pass
    
    def DeMux(self,file_name):
        DemuxedFile = file_name.replace(".mkv","_DeMuxed.mkv")
        cmd = [
            FFMPEG,
            "i",
            file_name,
            DemuxedFile    
        ]
        try:
            res = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            shell=True,
            timeout=60
        )
            if res.stdout:
                print(f"Result : {res.stdout}")
            if res.stderr:
                print(f"Error: {res.stderr}")
        except subprocess.TimeoutExpired:
            print(f"Result : {res.stdout}")
            print(f"Process timed out after 60 seconds.")
        except subprocess.CalledProcessError as e:
            print(e.returncode)
            print(e.output)
        return DemuxedFile
    
    def parseFile(self,file_name : str):
        language_list = []
        if not os.path.exists(file_name):
            raise FileNotFoundError
        mediainfo = MediaInfo.parse(file_name)
        for tracks in mediainfo.text_tracks:
            lang_code = tracks.language
            if not lang_code:
                lang_code = 'und'
            language = language_code_converter(lang_code)
            language_list.append(language)
        return language_list
    
    def runExtractor(self,file_name : str):
        file_name = urllib.parse.unquote(file_name)
        subtitles_files = []
        if not os.path.exists(file_name):
            raise FileNotFoundError
        languages = self.parseFile(file_name)
        file_dir = os.path.dirname(file_name)
        name = os.path.splitext(file_name)[0]
        # cmd = [
        #     CCExtractorEXE,
        #     file_name,
        #     '-out=webvtt',
        # ]

        cmd = [
            "ffmpeg", "-y","-i",
            file_name,
            "-c",
            "copy",
            # "-map",
            # "0:s",
            # output_path
        ]
        
        try:
            for idx,lang in enumerate(languages):
                output_path = os.path.join(file_dir, f"{name}_{lang}.srt")
                cmd.extend(["-map", f"0:s:{idx}",output_path])
                res = subprocess.run(
                    cmd,
                    # capture_output=True,
                    # text=True,
                    # check=True,
                    # shell=True,
                    )
                # if res.stdout:
                #     print(f"Result : {res.stdout}")
                
                # if res.stderr:
                #     print(f"Error: {res.stderr}")
        except subprocess.CalledProcessError as e:
            print(e.returncode)
            print(e.output)

        for file in os.listdir(file_dir):
            if file.endswith(".srt"):
                lang = file.split('_')[-1].split('.')[0]
                vtt_file = self.srt_to_vtt(file,file_dir)
                dict = {
                    "lang":lang,
                    "file":vtt_file,
                }
                subtitles_files.append(dict)
               
        return file_dir,subtitles_files
    
    def SrtToVTT(self,file_name,PATH):
        output_name = file_name.replace(".srt",".vtt")
        srt_to_vtt(os.path.join(PATH,file_name), os.path.join(PATH,output_name))
        return output_name
    
    def ConvertSrtToVTT(self,file_name,PATH):
        output_name = file_name.replace(".srt",".vtt")

        cmd = [
            FFMPEG,
            "-i",
            os.path.join(PATH,file_name),
            os.path.join(PATH,output_name)
        ]
        try:
            res = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            shell=True
        )
            if res.stdout:
                #  print(f"Result : {res.stdout}")
                pass
            if res.stderr:
                print(f"Error: {res.stderr}")
        except subprocess.CalledProcessError as e:
            print(e.returncode)
            print(e.output)
        return output_name
    
    def srt_to_vtt(self,srt_file,PATH):
        srt_file_path = os.path.join(PATH,srt_file)
        vtt_file_name = srt_file.replace(".srt",".vtt")
        vtt_file_path = os.path.join(PATH,vtt_file_name)
        
        with open(srt_file_path, 'r', encoding='utf-8') as srt_file:
            srt_lines = srt_file.readlines()

        vtt_content = "WEBVTT\n\n"
        skip_line = False
        for line in srt_lines:
            # Skip lines that are just numbers

            if re.match(r'^\d+$', line.strip()):
                skip_line = True
                continue

            # Convert timestamps from SRT to VTT format
            if '-->' in line:
                line = re.sub(r'(\d{2}):(\d{2}):(\d{2}),(\d{3})', r'\1:\2:\3.\4', line)
                skip_line = False

            # Only add lines that are not skipped
            if not skip_line:
                vtt_content += line

        # Write the VTT content to a new file
        with open(vtt_file_path, 'w', encoding='utf-8') as vtt_file:
            vtt_file.write(vtt_content)

        return vtt_file_name

    def clean(self,dir : Path,sub_list : list):
        for sub in sub_list:
            fp = os.path.join(dir,sub["file"])
            if os.path.exists(fp):
                try:
                    os.remove(fp)
                except PermissionError:
                    pass
class SearchQuery():
    def __init__(self,vtt_file,word) -> None:
        self.PATTERN = r"(\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3})\n(.*(?:\n(?!\d{2}:\d{2}:\d{2}\.\d{3} -->).*)*)"
        self.vtt_file = vtt_file
        self.word = word

    def parseFile(self):
        with open(self.vtt_file,'r',encoding='utf-8') as file:
            vtt_text = file.read()
        return vtt_text
    def search(self):
        vtt_text = self.parseFile()
        matches = re.findall(self.PATTERN, vtt_text)
        result = []
        for timestamp, subtitle in matches:
            if re.search(rf"\b{self.word}\b", subtitle, re.IGNORECASE):  # Search for the word (case-insensitive)
                start_time = self.convert_to_seconds(timestamp.split(".")[0])
                result.append({'timestamp': timestamp, 'subtitle': subtitle.strip(),'start_time':start_time})
        return result

    def convert_to_seconds(self,timestamp):
        hours, minutes, seconds = map(int, timestamp.split(':'))
        total_seconds = (hours * 3600) + (minutes * 60) + seconds
        return total_seconds

# obj = SearchQuery()
# res = obj.search(f"{BASE_DIR}/media/subtitles/test2_eng.vtt"," civilization")
# print(res)
# # subs = SubtitlesExtract()
# # subs.srt_to_vtt('test2_eng.srt',BASE_DIR / 'Samples' ) 
