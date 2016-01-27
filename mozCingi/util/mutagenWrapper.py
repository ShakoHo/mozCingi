__author__ = 'shako'
import os
import random
from mutagen.mp3 import MP3


class MutagenWrapper(object):

    DEFAULT_MP3_TITLE_LENGTH = 30

    data_folder_name = ""
    output_folder_name = ""

    def mutate_audio_file_header(self, src_data_dir_path, dst_data_dir_path, mutate_gen_num):
        output_audio_file_path_list = []

        for audio_file_name in os.listdir(src_data_dir_path):
            audio_file_path = os.path.join(src_data_dir_path, audio_file_name)
            for new_file_no in xrange(1, mutate_gen_num):
                [base_name, ext_name] = audio_file_name.split(".")
                new_file_path = os.path.join(dst_data_dir_path,
                                             base_name + "_" + str(new_file_no) + "." + ext_name)
                try:
                    obj_mp3 = MP3(audio_file_path)
                    if "TIT1" in obj_mp3:
                        obj_mp3['TIT1'].text = self.generate_random_unistr()
                    else:
                        obj_mp3['TIT2'].text = self.generate_random_unistr()
                    try:
                        obj_mp3.save(new_file_path)
                        output_audio_file_path_list.append(new_file_path)
                    except:
                        pass

                except:
                    pass

        return output_audio_file_path_list

    def generate_random_unistr(self):
        return "".join([unichr(random.randint(1, 1114111)) for n in xrange(0, self.DEFAULT_MP3_TITLE_LENGTH)])

