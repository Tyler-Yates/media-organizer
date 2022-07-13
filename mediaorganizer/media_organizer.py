import os
import shutil
from datetime import datetime

import exifread

from mediaorganizer.file_util import is_image, is_video


class MediaOrganizer:
    def __init__(self, input_path: str, pictures_output_path: str, copy_files: bool, dry_run: bool,
                 date_taken_only: bool):
        self.input_path = input_path
        self.pictures_output_path = pictures_output_path
        self.copy_files = copy_files
        self.dry_run = dry_run
        self.date_taken_only = date_taken_only
        # TODO support videos

    def process_input_directory(self):
        for root, dirs, files in os.walk(self.input_path):
            for file in files:
                absolute_file_path = os.path.join(root, file)
                relative_file_path = os.path.join(root, file).replace(self.input_path, "").lstrip(os.path.sep)
                self.process_file(absolute_file_path, relative_file_path)

    def process_file(self, absolute_file_path: str, relative_file_path: str):
        if is_image(absolute_file_path):
            print(f"\nProcessing image {absolute_file_path}...")
            file_year = str(self._get_file_year(absolute_file_path))
            print(f"File year: {file_year}")
            if relative_file_path.startswith(file_year + os.path.sep):
                new_file_path = os.path.join(self.pictures_output_path, relative_file_path)
            else:
                new_file_path = os.path.join(self.pictures_output_path, str(file_year), relative_file_path)

            if self.dry_run:
                print(f"Would move file to {new_file_path}")
            else:
                if os.path.exists(new_file_path):
                    print(f"File {new_file_path} already exists. Skipping.")

                file_directory = os.path.dirname(new_file_path)
                os.makedirs(file_directory, exist_ok=True)

                if self.copy_files:
                    print(f"Copying file to {new_file_path}")
                    shutil.copy(absolute_file_path, new_file_path)
                else:
                    print(f"Moving file to {new_file_path}")
                    shutil.move(absolute_file_path, new_file_path)
        elif is_video(absolute_file_path):
            # TODO support video
            pass
        else:
            print(f"Ignoring file {absolute_file_path}")

    def _get_file_year(self, absolute_file_path: str):
        with open(absolute_file_path, mode='rb') as input_file:
            tags = exifread.process_file(input_file)
            date_taken = tags.get('EXIF DateTimeOriginal', None)

        if date_taken:
            date_taken = datetime.strptime(str(date_taken), '%Y:%m:%d %H:%M:%S')
            return date_taken.year

        if self.date_taken_only:
            return "UNKNOWN"

        modified_time = datetime.utcfromtimestamp(os.path.getmtime(absolute_file_path))
        creation_time = datetime.utcfromtimestamp(os.path.getctime(absolute_file_path))
        oldest_time = min(modified_time, creation_time)
        return oldest_time.year
