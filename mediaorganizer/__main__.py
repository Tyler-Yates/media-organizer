import json

from mediaorganizer.media_organizer import MediaOrganizer


def main():
    with open("config.json", mode='r') as config_file:
        json_config = json.load(config_file)
        media_organizer = MediaOrganizer(
            input_path=json_config["input_path"],
            pictures_output_path=json_config["pictures_output_path"],
            copy_files=bool(json_config["copy_files"]),
            dry_run=bool(json_config["dry_run"]),
            date_taken_only=bool(json_config["date_taken_only"])
        )

    media_organizer.process_input_directory()


if __name__ == '__main__':
    main()
